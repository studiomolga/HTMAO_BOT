
#include "extrawindow.h"

void ExtraWindow::setup(){

}

void ExtraWindow::update(){

}

void ExtraWindow::draw(){
//    ofLogNotice(ofToString(ofGetWidth()));
    ofSetBackgroundColor(0);
    tex->drawSubsection(0, 0, 1920, 1080, 1920*wid, 0, 1920, 1080);
}

void ExtraWindow::setWid(int id){
    wid = id;
}

void ExtraWindow::setTexture(ofTexture * t){
    tex = t;
}
