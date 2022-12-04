# HTMAO BOT
## How to Make an Ocean Moirologist Bot. 

### Parts:
- Computer (see computer specs)
- Speakers. 
- 3 x TV Monitor - side monitors shall be under a slight angle
- 1x TV Monitor for displaying the algorithm *"working"* (optional)

### Computer specs:
- Processor: Intel i7 8 core
- Memory: 16GB minimum
- Videocard: at least nvidia gtx 1060/1070/1080 but for sure no AMD!
- Operating system: ubuntu 20.04 LTS https://releases.ubuntu.com/20.04.5/?_ga=2.227723037.1287600826.1670160231-2072636695.1669851777

- the nvidia drivers: press the 'window' key on the keyboard and in search option type: additional drivers. From there select the 'Nvidia driver 525 opem kernel tested' IF you have nvidia GEFORCE RTX. You might want to change your NVIDIA menu from 'on demand' to 'Performance mode'. Reboot. 


### Installation:
*openframeworks*
- download and install openframeworks
- download [openframeworks 0.11](https://github.com/openframeworks/openFrameworks/releases/download/0.11.2/of_v0.11.2_linux64gcc6_release.tar.gz) and unpack
- cd to: `cd [OF_FOLDER]/scripts/linux/ubuntu`
- run: `sudo ./install_dependencies.sh && sudo ./install_codecs.sh`

*python*
- `sudo apt update && sudo apt upgrade && sudo apt install liblo-dev`
- `sudo apt install python3-pip`
- `pip3 install numpy feedparser tensorflow==2.4.0 schedule pyliblo3`

_There might be an error_ 
(https://user-images.githubusercontent.com/1223253/205468621-fa46fbaf-7a90-46fa-8ec3-781076054446.png)


- `sudo apt install git`
then download project file:
- `git clone https://github.com/studiomolga/HTMAO_BOT.git`


*moirologist bot*
- move `ofHTMAO/ofHTMAO_player` to `[OF_FOLDER]/apps/myApps` in the OF folder
_(type in terminal `mv ofHTMAO/ofHTMAO_player [OF_FOLDER]/apps/myApps`)_
- move `ofHTMAO/ofxHPVPlayer` to `[OF_FOLDER]/addons` in the OF folder
- _(type in terminal `mv ofHTMAO/ofxHPVPlayer ofHTMAO/ofxHPVPlayer`)_
- cd to ofHTMAO_player folder  and run `make` to compile the application
- download and put in correct place the video files, `[OF_FOLDER]/apps/myApps/ofHTMAO_player/bin/data/movies`, the external drive will be provided


### Autostart on boot:
- put the correct paths in either the `three_screens.sh` or `four_screens.sh`, both found in the scripts folder
- press the windows key once and type startup, you will find the application `Startup Applications`, open it and add one of the two script files there
- reboot, and it should run
