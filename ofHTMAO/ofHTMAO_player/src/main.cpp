#include "ofMain.h"
#include "ofApp.h"
#include "extrawindow.h"
#include "ofAppGLFWWindow.h"

int main( )
{
    ofGLFWWindowSettings settings;

    // main window
    settings.setPosition(glm::vec2(0,0));
    settings.windowMode = OF_FULLSCREEN;
    settings.setGLVersion(4, 6);
    shared_ptr<ofAppBaseWindow> mainWindow = ofCreateWindow(settings);
    mainWindow->setVerticalSync(true);

    // window 1
    settings.setPosition(glm::vec2(1920,0));
    settings.windowMode = OF_FULLSCREEN;
    settings.setGLVersion(4, 6);
    settings.shareContextWith = mainWindow;
    shared_ptr<ofAppBaseWindow> window1 = ofCreateWindow(settings);
    window1->setVerticalSync(true);

    // window 2
    settings.setPosition(glm::vec2(3840,0));
    settings.windowMode = OF_FULLSCREEN;
    settings.setGLVersion(4, 6);
    settings.shareContextWith = mainWindow;
    shared_ptr<ofAppBaseWindow> window2 = ofCreateWindow(settings);
    window2->setVerticalSync(true);

    shared_ptr<ofApp> mainApp(new ofApp);
    shared_ptr<ExtraWindow> ew1App(new ExtraWindow);
    shared_ptr<ExtraWindow> ew2App(new ExtraWindow);
    mainApp->win1 = ew1App;
    mainApp->win2 = ew2App;

    ofRunApp(mainWindow, mainApp);
    ofRunApp(window1, ew1App);
    ofRunApp(window2, ew2App);
    ofRunMainLoop();
}
