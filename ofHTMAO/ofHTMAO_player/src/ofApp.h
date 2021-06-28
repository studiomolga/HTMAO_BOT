#pragma once

#include "ofMain.h"
#include "ofxHPVPlayer.h"
#include "ofxOsc.h"
#include "extrawindow.h"

#define VIDEOS_PATH "movies"
#define OSC_PORT 10000

class ofApp : public ofBaseApp
{
public:
    void setup();
    void update();
    void draw();
    void exit();

    struct paths_t {
        string video;
        string audio;
    };

    vector<vector<paths_t>> paths;
    void loadDirs();
    void loadMovie(paths_t path);

    void keyPressed(int key);

    ofxHPVPlayer hpvPlayer;
    ofSoundPlayer soundPlayer;
    ofxOscReceiver receiver;

    shared_ptr<ExtraWindow> win1;
    shared_ptr<ExtraWindow> win2;
};
