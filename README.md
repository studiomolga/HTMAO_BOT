# HTMAO BOT
## How to Make an Ocean Moirologist Bot. 

### Parts:
- Computer (see computer specs)
- Speakers. 
- 3 x TV Monitor - side monitors shall be under a slight angle
- 1x TV Monitor for displaying the algorithm *"working"*

### Computer specs:
- Processor: Intel i7 8 core
- Memory: 16GB minimum
- Videocard: at least nvidia gtx 1060/1070/1080 but for sure no AMD!
- Operating system: ubuntu with the nvidia drivers installed and working


### Installation:
*project files*
- `git clone https://github.com/studiomolga/HTMAO_BOT.git`

*openframeworks*
- download and install openframeworks
- download [openframeworks 0.11](https://github.com/openframeworks/openFrameworks/releases/download/0.11.2/of_v0.11.2_linux64gcc6_release.tar.gz) and unpack
- cd to: `cd [OF_FOLDER]/scripts/linux/ubuntu`
- run: `sudo ./install_dependencies.sh && sudo ./install_codecs.sh`
- move `ofHTMAO/ofHTMAO_player` to `[OF_FOLDER]/apps/myApps` in the OF folder
- move `ofHTMAO/ofxHPVPlayer` to `[OF_FOLDER]/addons` in the OF folder
- cd to ofHTMAO_player folder  and run `make` to compile the application
- download and put in correct place the video files, `[OF_FOLDER]/apps/myApps/ofHTMAO_player/bin/data/movies`, links will be provided

*python*
- `sudo apt update && sudo apt upgrade && sudo apt install liblo-dev`
- `pip3 install numpy feedparser tensorflow==2.4.0 schedule pyliblo3`
- `git clone https://github.com/studiomolga/HTMAO_BOT.git`


### Autostart on boot:
- *some guide to auto starting on boot*
