import oscP5.*;
import processing.video.*;

import java.util.Arrays;

class PWindow extends PApplet {
  int id;
  PImage frame;

  PWindow(int _id) {
    super();
    id = _id;
    PApplet.runSketch(new String[] {this.getClass().getSimpleName()}, this);
  }

  void settings() {
    fullScreen(P3D, id);
  }

  void setup() {
    background(0);
    noCursor();
  }

  void setFrame(PImage f) {
    frame = f;
  }

  void draw() {
    if (frame != null) {
      PVector dim = new PVector(width, ((float)(width) / (float)frame.width) * (float)frame.height); 
      float yOffset = (height - dim.y) / 2;
      image(frame, 0, yOffset, dim.x, dim.y);
    }
  }
}

static final Boolean IS_FULLSCREEN = true;
static final String[] PATHS = {"videos/neg/", "videos/neutral/", "videos/pos/"};
static final int OSC_PORT = 10000;                    
static final String OSC_ADDRESS = "/htmao/play";

PWindow win[];
int numWindows = 3;
Movie movie;

OscP5 oscP5;
String videos[][];
PVector currVideo;

void setup() {
  win = new PWindow[numWindows];
  for (int i = 0; i < win.length; i++) {
    win[i] = new PWindow(i+1);
  }

  oscP5 = new OscP5(this, OSC_PORT);

  currVideo = new PVector(0, 0);
  videos = new String[3][3];
  for (int i = 0; i < PATHS.length; i++) {
    String folderPath = sketchPath() + "/data/" + PATHS[i];
    File[] paths = listFiles(folderPath);
    for (int j = 0; j < paths.length; j++) {
      File f = paths[j];
      String video = f.getAbsolutePath();
      videos[i][j] = video;
    }
  }
  loadMovie(currVideo);
}

File[] listFiles(String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {
    File[] files = file.listFiles();
    java.util.Arrays.sort(files);
    return files;
  } else {
    return null;
  }
}

void draw() {
  PImage frame = createImage(movie.width, movie.height, RGB);;
  if(getFrameCurrent() < getFramesTotal()){
    frame = movie.get(0, 0, movie.width, movie.height); 
  }
  
  for (int i = 0; i < win.length; i++) {
    int fWidth = frame.width/3;
    win[i].setFrame(frame.get(fWidth * i, 0, frame.width, frame.height));
  }
}

void loadMovie(PVector v){
  movie = new Movie(this, videos[(int)v.x][(int)v.y]);
  movie.play();
}

void oscEvent(OscMessage msg) {
  if (msg.addrPattern().equals(OSC_ADDRESS)) {
    int cat = msg.get(0).intValue();
    int vid = msg.get(1).intValue();
    println("category: " + cat + " video: " + vid);

    currVideo.x = cat;
    currVideo.y = vid;
    loadMovie(currVideo);
  }
}

void movieEvent(Movie m) {
  m.read();
}

int getFramesTotal() {
  return int(movie.duration() * movie.frameRate);
}

int getFrameCurrent() {
  return int(movie.time() * movie.frameRate);
}
