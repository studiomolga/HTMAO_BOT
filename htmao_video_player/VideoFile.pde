class VideoFile {
  Movie movie;
  String path;
  int totalFrames;
  int currFrame;
  PVector displayDim;
  boolean isPlaying;
  
  VideoFile(PApplet parent, String _path){
    path = _path;
    
    movie = new Movie(parent, path);
    movie.play();
    delay(100);
    totalFrames = getFramesTotal();
    displayDim = getDimensions();
    println("width: " + movie.width + " height: " + movie.height + " total frames: " + totalFrames + " dimensions: " + displayDim);
    
    movie.pause();
    movie.jump(0);
    
    isPlaying = false;
  }
  
  void draw() {
    currFrame = getFrameCurrent();
    if(isPlaying){
      if(currFrame < totalFrames){
        float yOffset = (height - displayDim.y) / 2;
        image(movie, 0, yOffset, displayDim.x, displayDim.y);
      } else {
        isPlaying = false;
      }
    } else {
      background(0);
    }
  }
  
  void play() {
    if(!isPlaying){
      movie.play();
      isPlaying = true;
    }
  }
  
  boolean isPlaying(){
    return isPlaying;
  }
  
  int getFramesTotal() {
    return int(movie.duration() * movie.frameRate);
  }
  
  int getFrameCurrent() {
    return int(movie.time() * movie.frameRate);
  }
  
  PVector getDimensions() {
    PVector dim = new PVector(width, ((float)width / (float)movie.width) * (float)movie.height); 
    return dim;
  }
}
