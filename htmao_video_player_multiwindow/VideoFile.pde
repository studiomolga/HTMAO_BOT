class VideoFile {
  Movie movie;
  String path;
  int totalFrames;
  int currFrame;
  boolean isPlaying;
  PImage black;
  
  VideoFile(PApplet parent, String _path){
    path = _path;
    
    movie = new Movie(parent, path);
    movie.play();
    black = createImage(movie.width, movie.height, RGB);
    delay(100);
    totalFrames = getFramesTotal();
    println("width: " + movie.width + " height: " + movie.height + " total frames: " + totalFrames);
    
    movie.pause();
    movie.jump(0);
    
    isPlaying = false;
  }
  
  PImage getFrame() {
    currFrame = getFrameCurrent();
    if(isPlaying){
      if(currFrame < totalFrames){
        PImage frame;
        frame = movie.get(0, 0, movie.width, movie.height);
        return frame;
      } else {
        isPlaying = false;
        return black;
      }
    } else {
      return black;
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
}
