# pdrcrd

## Description
A combined docker image for the unified deployment of **[itsToggle's](https://github.com/itsToggle)** projects -- **[plex_debrid](https://github.com/itsToggle/plex_debrid)** and **[rclone_RD](https://github.com/itsToggle/rclone_RD)**


## Features
 - Bind-mounts rclone_RD to the host
 - RealDebrid API Key passed to rclone_rd and plex_debrid from docker-compose
 - rclone_RD config automatically generated
 - rclone_RD flags passed from docker-compose
 - Fuse.conf allow_other applied within the container vs. the host
 - Plex server values passed to plex_debrid settings.json from docker-compose
 - Automatic update of plex_debrid to the latest version

## Docker Hub
A prebuilt image is hosted on [docker hub](https://hub.docker.com/r/iampuid0/pdrcrd) 


## Docker-compose
```
services:
  pdrcrd:
    container_name: pdrcrd
    image: iampuid0/pdrcrd:latest  #image name you assigned with docker build using the dockerfile or pull pre-built image from iampuid0/pdrcrd:latest
    stdin_open: true # docker run -i
    tty: true        # docker run -t    
    volumes:
      - your/host/path/config:/config # rclone.conf & settings.json will both be here on the host CAUTION: rclone.conf is overwritten upon start/restart of the container
      - your/host/path/log:/log # logs will be here on the host
      - your/host/path/mnt:/data:shared #rclone mount will be here on the host  
    environment:
      - TZ=America/New_York
      - RD_API_KEY=yourrealdebridapikey
      - RCLONE_MOUNT_NAME=yourmountname
      - RCLONE_LOG_LEVEL=INFO
      - RCLONE_LOG_FILE=/log/logfilename.txt  
      - RCLONE_DIR_CACHE_TIME=10s #optional, but recommended as default
#      - RCLONE_CACHE_DIR=/cache #optional
#      - RCLONE_VFS_CACHE_MODE=full #optional
#      - RCLONE_VFS_CACHE_MAX_SIZE=100G #optional
#      - RCLONE_VFS_CACHE_MAX_AGE=1h #optional
#      - RCLONE_DIR_PERMS=777 #optional, not functional in beta
#      - RCLONE_FILE_PERMS=777 #optional, not functional in beta
#      - RCLONE_UMASK= #optional, not functional in beta
      - PLEX_USER=yourplexusername  #required 
      - PLEX_TOKEN=yourplextoken  #required - see link for detail https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
      - PLEX_ADDRESS=http://localhost:32400 #required - format must include http:// and have no trailing characters after 32400 e.g / 
#       - SHOW_MENU=false  #optional - if used, value must be true or false -- default is true
#       - PD_LOGFILE=true  #optional - if used, value must be true or false -- default is false
#       - AUTO_UPDATE=WeHadABabyItsABoy   #optional - uncommenting will enable auto update to the latest version of plex_debrid locally in the container. No values are required.
#       - AUTO_UPDATE_INTERVAL=24 #optional - if used, value must be an integer -- default is 24 hours
    devices:
      - /dev/fuse:/dev/fuse:rwm
    cap_add:
      - SYS_ADMIN     
    security_opt:
      - apparmor:unconfined    
      - no-new-privileges
#    restart: unless-stopped
```

## Docker Build

### Docker CLI

```
docker build -t yourimagename https://github.com/I-am-PUID-0/pdrcrd.git
```

### Portainer

Download the repo files

<img src="https://user-images.githubusercontent.com/36779668/228725571-d0084e89-05c9-4bf5-bea5-6b7cd0e996b4.png" width="250" height="250">


Select "+ Build a new image"

<img src="https://user-images.githubusercontent.com/36779668/228723889-f49af0d0-12f0-4837-8c59-6aa64921723b.png" width="550" height="30">


Specify your image name

<img src="https://user-images.githubusercontent.com/36779668/228724192-feb82409-f5c0-46b3-a6dc-5d8c9b0f093c.png" width="550" height="250">


Select "Web editor" and paste the contents of the Dockerfile inside the field

<img src="https://user-images.githubusercontent.com/36779668/228724344-6c9de02b-c4bd-4573-9223-6b14d5e9f2ae.png" width="550" height="250">


Select the identified files 

<img src="https://user-images.githubusercontent.com/36779668/228724346-6a2e5641-ff31-4de2-98bc-f17b37bd60f2.png" width="550" height="100">

Select "Build the image"

<img src="https://user-images.githubusercontent.com/36779668/228724347-a6911a5f-40ee-4f02-982f-cc0d977d5b3b.png" width="150" height="100">

Confirm the image is successfully built

<img src="https://user-images.githubusercontent.com/36779668/228724348-20ee3562-167e-47fb-b503-5b7ce1642b5b.png" width="250" height="100">


## Install script for Ubuntu and/or WSL
Whether starting with a clean install of Ubuntu (22.04 LTS tested), an established Docker setup on Ubuntu, or following the [Windows Setup Guide (Docker/WSL)](https://discord.com/channels/1090745199891861524/1091543927842148452 ) , this script will walk the user through a prompted installation of Docker and/or pdrcrd. For users utilizing WSL, a prompt is also provided post setup that allows the user to open the newly mounted rclone_RD directory inside the Windows explore of the host machine. 

Paste the below into your Ubuntu CLI. 
```curl -o pdrcrd_ubuntu_install.sh https://raw.githubusercontent.com/I-am-PUID-0/pdrcrd/master/Ubuntu/pdrcrd_ubuntu_install.sh  && chmod +x pdrcrd_ubuntu_install.sh```



Then paste the following: 
```./pdrcrd_ubuntu_install.sh```



Follow the prompts and enjoy 🙂


NOTE: Testing has not been performed on any distros other than Ubuntu 22.04 LTS and WSL 2 on Windows 11. If you experience any issues, please post them on GitHub. https://github.com/I-am-PUID-0/pdrcrd/issues 

## Automatic Updates

If you would like to enable automatic updates, you can do so by uncommenting the AUTO_UPDATE variable in your docker-compose.yml file. This will automatically update plex_debrid to the latest version on startup and at the interval specified by AUTO_UPDATE_INTERVAL. No values are required for AUTO_UPDATE.

The default value for AUTO_UPDATE_INTERVAL is 24 hours. If you would like to change this, you can do so by uncommenting the AUTO_UPDATE_INTERVAL variable in your docker-compose.yml file and setting the value to the number of hours you would like to wait between updates.

The automatic update is performed by comparing the installed version with the version available on GitHub. If a delta exists, it continues by pulling the latest version of plex_debrid from GitHub and replacing the existing plex_debrid container files. This will not affect any of your settings or configuration.

plex_debrid will be restarted automatically after the update is complete. As such, if you have any active scrapes running in plex_debrid, they will be interrupted and will be restarted once plex_debrid reloads. However, due to the lack of a caching feature within plex_debrid for items that have not exceeded their retry limit, the retry count will revert to 0 for any items that were in the process of being scraped when the update occurred. This means that any items that were in the process of being scraped when the update occurred will be re-scraped from the beginning. This is a known issue and will be addressed in a future update.

The benefit of this automatic update feature is that you will always be running the latest version of plex_debrid. This will ensure that you are always taking advantage of the latest features and bug fixes. It also means that the container will not need to be rebuilt or restarted by pulling a new image when a new version of plex_debrid is released. This will save you time and bandwidth, but most importantly, it will prevent the rclone_RD mount from being reset and severing the connection to your Plex server. Thus, the Plex server will not need to be restarted due to applying updates for the inbuilt applications.


## TODO
- Test the use of .env files to setup rclone and plex_debrid
- Add support for setting user/group -- currently runs as root
- Add docker s6-overlay
- Evaluate adding Plex Media Server to the container
- Add support for other Media Servers - Emby, Jellyfin, etc. -- currently only supports Plex

## Community

### pdrcrd
- For questions related to pdrcrd, see the GitHub [discussions](https://github.com/I-am-PUID-0/pdrcrd/discussions)
- or create a new [issue](https://github.com/I-am-PUID-0/pdrcrd/issues) if you find a bug or have an idea for an improvement.
- or join the pdrcrd [discord server](https://discord.gg/n5nQRYtrw2)

### plex_debrid
- For questions related to plex_debrid, see the GitHub [discussions](https://github.com/itsToggle/plex_debrid/discussions) 
- or create a new [issue](https://github.com/itsToggle/plex_debrid/issues) if you find a bug or have an idea for an improvement.
- or join the plex_debrid [discord server](https://discord.gg/u3vTDGjeKE) 


## Buy **[itsToggle](https://github.com/itsToggle)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy itsToggle a beer/coffee, feel free to use his real-debrid [affiliate link](http://real-debrid.com/?id=5708990) or send him a virtual beverage via [PayPal](https://www.paypal.com/paypalme/oidulibbe) :)


## GitHub Workflow Status
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/I-am-PUID-0/pdrcrd/docker-image.yml)
