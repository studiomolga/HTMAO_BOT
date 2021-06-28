#pragma once

#include "ofMain.h"

class ExtraWindow: public ofBaseApp {
public:
    void setup();
    void update();
    void draw();

    void setWid(int id);
    void setTexture(ofTexture * t);

    int wid;
    ofTexture * tex;
};

