# pdrcrd

## Description
A combined docker image for the unified deployment of **[itsToggle's](https://github.com/itsToggle)** projects -- **[plex_debrid](https://github.com/itsToggle/plex_debrid)** and **[rclone_RD](https://github.com/itsToggle/rclone_RD)**


## Features


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


## TODO
- Test the use of .env files to setup rclone and plex_debrid
- Add support for setting user/group -- currently runs as root
- Add docker s6-overlay
- Add multiarch support - only supports linux/amd64 for now
- Add automated builds and/or optional local updates to pull the latest updates from **[plex_debrid](https://github.com/itsToggle/plex_debrid)** and **[rclone_RD](https://github.com/itsToggle/rclone_RD)**
- Evaluate adding Plex

## Community

### pdrcrd
- For questions related pdrcpd see the github [discussions](https://github.com/I-am-PUID-0/pdrcrd/discussions)
- or create a new [issue](https://github.com/I-am-PUID-0/pdrcrd/issues) if you find a bug or have an idea for an improvement.
- or join the pdrcpd [discord server](https://discord.gg/vagjYTwE)

### plex_debrid
- For questions related to plex_debrid see the github [discussions](https://github.com/itsToggle/plex_debrid/discussions) 
- or create a new [issue](https://github.com/itsToggle/plex_debrid/issues) if you find a bug or have an idea for an improvement.
- or join the plex_debrid [discord server](https://discord.gg/u3vTDGjeKE) 


## Buy **[itsToggle](https://github.com/itsToggle)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy itsToggle a beer/coffee, feel free to use his real-debrid [affiliate link](http://real-debrid.com/?id=5708990) or send him a virtual beverage via [PayPal](https://www.paypal.com/paypalme/oidulibbe) :)
