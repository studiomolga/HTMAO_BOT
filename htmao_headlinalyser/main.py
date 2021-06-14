import os
import sys
from time import sleep
import numpy as np
import feedparser
import liblo
# import matplotlib.pyplot as plt
import re
import string
import tensorflow as tf
from datetime import datetime
import schedule
import random

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

TRIGGER_TIMES = [5, 20, 35, 50]
OSC_PORT = 10000
URLS = [
    'https://www.theguardian.com/uk/environment/rss',
    'http://feeds.bbci.co.uk/news/uk/rss.xml'
]

AUTOTUNE = tf.data.AUTOTUNE
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_PATH, 'headline_sentiment')
TRAIN_PATH = os.path.join(DATASET_PATH, 'train')
NEGATIVE = 0
NEUTRAL = 1
POSITIVE = 2
BATCH_SIZE = 32
SEED = 42
MAX_FEATURES = 5000
SEQUENCE_LENGTH = 100
EPOCHS = 100
EMBEDDING_DIM = 16


def pprint(txt):
    now = datetime.now()
    print('{} | {}'.format(now, txt))


class Feed:
    def __init__(self, url):
        self.url = url
        self.ids = []

    def update(self):
        feed = feedparser.parse(self.url)['entries']
        new_articles = []

        for article in feed:
            if article['id'] not in self.ids:
                self.ids.append(article['id'])
                new_articles.append(article)

        return new_articles


class Headline:
    def __init__(self, txt, pred_val, pred_label):
        self.txt = txt
        self.pred_val = pred_val
        self.pred_label = pred_label

    def __repr__(self):
        return '{}, {}, {}'.format(self.txt, self.pred_val, self.pred_label)


class HeadlineStore:
    def __init__(self, urls, pred_model):
        self.urls = urls
        self.model = pred_model
        self.headlines = []
        self.used_ids = []

        self.feeds = [Feed(url) for url in self.urls]

    def update(self):
        pprint('updating headline store')

        if len(self.used_ids) == len(self.headlines):
            self.used_ids = []

        for feed in self.feeds:
            new_articles = feed.update()
            titles = [article['title'] for article in new_articles]
            for title in titles:
                prediction = self.model.predict(np.array([title]))
                pred_val = np.amax(prediction[0])
                pred_label = np.where(prediction[0] == pred_val)[0][0]

                headline = Headline(title, pred_val, pred_label)
                self.headlines.append(headline)

                if pred_label == POSITIVE:
                    txt = '{} is positive: {}'.format(title, pred_val)
                elif pred_label == NEUTRAL:
                    txt = '{} is neutral: {}'.format(title, pred_val)
                elif pred_label == NEGATIVE:
                    txt = '{} is negative: {}'.format(title, pred_val)

                pprint('adding headline to store: {}'.format(txt))

    def get_rand_headline(self):
        index = 0

        while index in self.used_ids:
            index = random.randint(0, len(self.headlines) - 1)

        self.used_ids.append(index)
        pprint("used headline id's: {}".format(self.used_ids))

        return self.headlines[index]


def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    return tf.strings.regex_replace(stripped_html, '[%s]' % re.escape(string.punctuation), '')


def create_vectorize_layer():
    vec_layer = TextVectorization(standardize=custom_standardization,
                                  max_tokens=MAX_FEATURES,
                                  output_mode='int',
                                  output_sequence_length=SEQUENCE_LENGTH)

    return vec_layer


def create_model():
    mdl = tf.keras.Sequential([layers.Embedding(MAX_FEATURES + 1, EMBEDDING_DIM),
                               layers.Dropout(0.2),
                               layers.GlobalAveragePooling1D(),
                               layers.Dropout(0.2),
                               layers.Dense(3)])

    mdl.compile(loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                optimizer='adam',
                metrics=tf.metrics.SparseCategoricalAccuracy())

    return mdl


def train():
    def vectorize_text(text, label):
        text = tf.expand_dims(text, -1)
        return vectorize_layer(text), label

    raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory('headline_sentiment/train',
                                                                      batch_size=BATCH_SIZE,
                                                                      validation_split=0.2,
                                                                      subset='training',
                                                                      seed=SEED)

    raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory('headline_sentiment/train',
                                                                    batch_size=BATCH_SIZE,
                                                                    validation_split=0.2,
                                                                    subset='validation',
                                                                    seed=SEED)

    print("Label 0 corresponds to", raw_train_ds.class_names[0])
    print("Label 1 corresponds to", raw_train_ds.class_names[1])
    print("Label 2 corresponds to", raw_train_ds.class_names[2])

    vectorize_layer = create_vectorize_layer()

    # Make a text-only dataset (without labels), then call adapt
    train_text = raw_train_ds.map(lambda x, y: x)
    vectorize_layer.adapt(train_text)

    train_ds = raw_train_ds.map(vectorize_text)
    val_ds = raw_val_ds.map(vectorize_text)

    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    checkpoint_dir = os.path.join(BASE_PATH, 'checkpoints/cp-{epoch:04d}.ckpt')

    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_dir,
                                                     save_weights_only=True,
                                                     verbose=1)
    callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, mode='min')

    model = create_model()
    model.summary()

    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=[callback, cp_callback])

    export_model = tf.keras.Sequential([
        vectorize_layer,
        model,
        layers.Activation('sigmoid')
    ])

    export_model.compile(
        loss=losses.SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
    )

    # examples = [
    #     "Don't believe hydrogen and nuclear hype – they can’t get us to net zero carbon by 2050",
    #     "‘Reading the writing on the wall’: why Wall Street is acting on the climate crisis",
    #     "New US vehicles must be electric by 2030 to meet climate goals – report",
    #     "Ministers watering down green pledges post-Brexit, study finds"
    # ]

    # print(export_model.predict(examples))

    return export_model


def send_headline(store, target):
    store.update()
    headline = store.get_rand_headline()
    pprint('selected headline: {}'.format(headline))

    movie_id = 0
    if headline.pred_val <= 0.67:
        movie_id = 0
    elif 0.67 < headline.pred_val < 0.83:
        movie_id = 1
    elif headline.pred_val > 0.83:
        movie_id = 2

    if headline.pred_label == POSITIVE:
        pprint('using video: {} from the positive category'.format(movie_id))
    elif headline.pred_label == NEUTRAL:
        pprint('using video: {} from the neutral category'.format(movie_id))
    elif headline.pred_label == NEGATIVE:
        pprint('using video: {} from the negative category'.format(movie_id))

    liblo.send(target, '/htmao/play', int(headline.pred_label), movie_id)


if __name__ == '__main__':
    model = train()
    headline_store = HeadlineStore(URLS, model)

    try:
        osc_target = liblo.Address('127.0.0.1', OSC_PORT)
    except liblo.AddressError as err:
        pprint('!!!!!!!!! COULD NOT OPEN OSC PORT, check whether your localhost is on 127.0.0.1'.format(str(err)))
        osc_target = None
        sys.exit()

    for trigger_time in TRIGGER_TIMES:
        if 0 <= trigger_time < 60:
            schedule.every().hour.at(":{:02d}".format(trigger_time)).do(send_headline, headline_store, osc_target)
        else:
            pprint('!!!!!!!! USED INVALID TRIGGER TIME, please only use numbers in the range 0-59')
            sys.exit()

    while True:
        schedule.run_pending()
        sleep(1)
