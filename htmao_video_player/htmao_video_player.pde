import oscP5.*;
import processing.video.*;

import java.util.Arrays;

static final Boolean IS_FULLSCREEN = false;
static final String[] PATHS = {"videos/neg/", "videos/neutral/", "videos/pos/"};
static final int OSC_PORT = 10000;                    
static final String OSC_ADDRESS = "/htmao/play";

OscP5 oscP5;
VideoFile[][] videos;
PVector currVideo;

void settings(){
  if(IS_FULLSCREEN){
    fullScreen();
  } else {
    size(800, 480);
  }
}

void setup() {
  background(0);
  
  oscP5 = new OscP5(this, OSC_PORT);
  
  currVideo = new PVector(0, 0);
  videos = new VideoFile[3][3];
  for(int i = 0; i < PATHS.length; i++){
    String folderPath = sketchPath() + "/data/" + PATHS[i];
    File[] paths = listFiles(folderPath);
    for(int j = 0; j < paths.length; j++){
      File f = paths[j];
      VideoFile video = new VideoFile(this, f.getAbsolutePath());
      videos[i][j] = video; 
    }
  }
}

void draw() {
  videos[(int)currVideo.x][(int)currVideo.x].draw();
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

void oscEvent(OscMessage msg) {
  if(msg.addrPattern().equals(OSC_ADDRESS)){
    int cat = msg.get(0).intValue();
    int vid = msg.get(1).intValue();
    println("category: " + cat + " video: " + vid);
    
    if(!videos[(int)currVideo.x][(int)currVideo.x].isPlaying()){
      currVideo.x = cat;
      currVideo.y = vid;
      videos[(int)currVideo.x][(int)currVideo.x].play();
    }
  }  
}

void movieEvent(Movie m) {
  m.read();
}
