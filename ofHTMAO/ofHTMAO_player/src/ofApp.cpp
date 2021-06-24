#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup()
{
    ofHideCursor();
    HPV::InitHPVEngine();

    hpvPlayer.init(HPV::NewPlayer());

    loadDirs();

    // listen on the given port
    ofLogNotice("listening for osc messages on port " + ofToString(OSC_PORT));
    receiver.setup(OSC_PORT);
}

//--------------------------------------------------------------
void ofApp::update()
{
    while(receiver.hasWaitingMessages()){
        // get the next message
        ofxOscMessage m;
        receiver.getNextMessage(m);

        if(m.getAddress() == "/htmao/play"){
            int cat = m.getArgAsInt(0);
            int vid = m.getArgAsInt(1);

            //temporary for a single movie per category
            if(vid > paths[cat].size() - 1) {
                vid = paths[cat].size() - 1;
            }

            if(!soundPlayer.isPlaying()){
                ofLogNotice("playing category: " + ofToString(cat) + " and video: " + ofToString(vid));
                ofLogNotice(paths[cat][vid].video + "," + paths[cat][vid].audio);
                loadMovie(paths[cat][vid]);
            }
        }
    }

    if(soundPlayer.isPlaying()){
        hpvPlayer.seekToPos(soundPlayer.getPosition());
    }

    HPV::Update();
}

//--------------------------------------------------------------
void ofApp::draw()
{
    ofBackground(0);

    if(soundPlayer.isPlaying()){
        hpvPlayer.draw(0,0,ofGetWidth(), ofGetHeight());
    }
}

//--------------------------------------------------------------
void ofApp::loadDirs() {
    // populate paths
    ofDirectory dir(VIDEOS_PATH);
    dir.listDir();
    dir.sort();

    for(int i = 0; i < dir.size(); i++){
        ofDirectory label(dir.getPath(i));
        if(label.isDirectory()){
            vector<paths_t> ps;
            label.listDir();
            label.sort();
            for(int j = 0; j < label.size(); j++){
                ofDirectory movie(label.getPath(j));
                movie.listDir();
                paths_t p;
                vector<ofFile> files = movie.getFiles();
                for(int k = 0; k < files.size(); k++){
                    if(files[k].getExtension() == "hpv") {
                        p.video = files[k].getAbsolutePath();
                        ofLogNotice("adding video path: " + p.video);
                    }

                    if(files[k].getExtension() == "wav") {
                        p.audio = files[k].getAbsolutePath();
                        ofLogNotice("adding audio path: " + p.audio);
                    }
                }
                ps.push_back(p);
            }
            paths.push_back(ps);
        }
    }
}


void ofApp::loadMovie(paths_t path) {
    ofLogNotice("loading new video: " + path.video);
    ofLogNotice("loading new audio: " + path.audio);
    ofLogNotice("hpvPlayer has already been initialised: " + ofToString(hpvPlayer.isInitialized()));
    ofLogNotice("soundPlayer has already been initialised: " + ofToString(soundPlayer.isLoaded()));

    if(hpvPlayer.isInitialized()){
        hpvPlayer.stop();
//        hpvPlayer.close();

        HPV::DestroyHPVEngine();

        hpvPlayer = ofxHPVPlayer();

        HPV::InitHPVEngine();

        hpvPlayer.init(HPV::NewPlayer());
    }

    if(soundPlayer.isLoaded()){
        soundPlayer.unload();
    }

    if (hpvPlayer.load(path.video))
    {
        hpvPlayer.setLoopState(OF_LOOP_NONE);
        hpvPlayer.play();
        hpvPlayer.setPaused(true);

        if (hpvPlayer.getFrameRate() > 60)
        {
            ofSetVerticalSync(false);
            ofSetFrameRate(120);
        }
        else
        {
            ofSetVerticalSync(true);
        }
    }

    if (soundPlayer.load(path.audio))
    {
        soundPlayer.play();
        soundPlayer.setLoop(false);
    }

    ofLogNotice("new video duration: " + ofToString(hpvPlayer.getDuration()));
}

//--------------------------------------------------------------
void ofApp::exit()
{
    receiver.stop();
    HPV::DestroyHPVEngine();
    ofShowCursor();
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key)
{
    if(!soundPlayer.isPlaying()){
        int cat_id;
        int movie_id;
        if (key == 'a')         // pick a random movie from negative category
        {
            cat_id = 0;
            movie_id = int(floor(ofRandom(paths[cat_id].size())));
            loadMovie(paths[cat_id][movie_id]);
        }
        else if (key == 's')    // pick a random movie from the neutral category
        {
            cat_id = 1;
            movie_id = int(floor(ofRandom(paths[cat_id].size())));
            loadMovie(paths[cat_id][movie_id]);
        } else if(key == 'd') { // pich a random movie from the positive category
            cat_id = 2;
            movie_id = int(floor(ofRandom(paths[cat_id].size())));
            loadMovie(paths[cat_id][movie_id]);
        }
    }

}
