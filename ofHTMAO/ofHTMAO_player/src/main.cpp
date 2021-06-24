#include "ofMain.h"
#include "ofApp.h"

int main( )
{
    ofGLFWWindowSettings settings;

    settings.decorated = false;
    settings.windowMode = OF_FULLSCREEN;
    settings.multiMonitorFullScreen = true;
    settings.setGLVersion(4, 6);

    ofCreateWindow(settings);
    ofRunApp(new ofApp());
}
