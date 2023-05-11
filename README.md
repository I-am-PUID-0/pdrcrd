# pdrcrd

## Description
A combined docker image for the unified deployment of **[itsToggle's](https://github.com/itsToggle)** projects -- **[plex_debrid](https://github.com/itsToggle/plex_debrid)** and **[rclone_RD](https://github.com/itsToggle/rclone_RD)**


## Features
 - Bind-mounts rclone_RD to the host
 - RealDebrid API Key passed to rclone_rd and plex_debrid via docker enviorment variable
 - rclone_RD config automatically generated
 - rclone_RD flags passed via docker enviorment variable
 - Fuse.conf ```user_allow_other``` applied within the container vs. the host
 - Plex server values passed to plex_debrid settings.json via docker enviorment variables
 - Automatic update of plex_debrid to the latest version
 - Optional independent or combined utilization of rclone_RD and plex_debrid

## Docker Hub
A prebuilt image is hosted on [docker hub](https://hub.docker.com/r/iampuid0/pdrcrd) 


## Docker-compose
```
services:
  pdrcrd:
    container_name: pdrcrd
    image: iampuid0/pdrcrd:latest  
    stdin_open: true # docker run -i
    tty: true        # docker run -t    
    volumes:
      - your/host/path/config:/config
      - your/host/path/log:/log
      - your/host/path/mnt:/data:shared
    environment:
      - TZ=
      - RD_API_KEY=
      - RCLONE_MOUNT_NAME=
      - RCLONE_DIR_CACHE_TIME=10s
      - PLEX_USER=
      - PLEX_TOKEN=
      - PLEX_ADDRESS=
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

## Install script for Ubuntu and/or WSL
Shell script to install docker and/or pdrcrd. See the [pdrcrd Wiki](https://github.com/I-am-PUID-0/pdrcrd/wiki/Setup-Guides#install-script-for-ubuntu-andor-wsl) for details.

## Automatic Updates
If you would like to enable automatic updates for plex_debrid, utilize the ```AUTO_UPDATE``` environment variable. 
Addtional details can be found in the [pdrcrd Wiki](https://github.com/I-am-PUID-0/pdrcrd/wiki/Settings#automatic-updates)


## Environment Variables

To customize some properties of the container, the following environment
variables can be passed via the `-e` parameter (one for each variable) or via the docker-compose file within the ```environment:``` section.  Value
of this parameter has the format `<VARIABLE_NAME>=<VALUE>`.

| Variable       | Description                                  | Default | Required for rclone_RD| Required for plex_debrid|
|----------------|----------------------------------------------|---------|:-:|:-:|
|`TZ`| [TimeZone](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones) used by the container. | ` ` |
|`RD_API_KEY`| [RealDebrid API key](https://real-debrid.com/apitoken). | ` ` | :heavy_check_mark:| :heavy_check_mark:|
|`RCLONE_MOUNT_NAME`| A name for the rclone mount. | ` ` | :heavy_check_mark:|
|`RCLONE_LOG_LEVEL`| [Log level](https://rclone.org/docs/#log-level-level) for rclone. | `NOTICE` |
|`RCLONE_LOG_FILE`| [Log file](https://rclone.org/docs/#log-file-file) for rclone. | ` ` |
|`RCLONE_DIR_CACHE_TIME`| [How long a directory should be considered up to date and not refreshed from the backend](https://rclone.org/commands/rclone_mount/#vfs-directory-cache). #optional, but recommended is 10s. | `5m` |
|`RCLONE_CACHE_DIR`| [Directory used for caching](https://rclone.org/docs/#cache-dir-dir). | ` ` |
|`RCLONE_VFS_CACHE_MODE`| [Cache mode for VFS](https://rclone.org/commands/rclone_mount/#vfs-file-caching). | ` ` |
|`RCLONE_VFS_CACHE_MAX_SIZE`| [Max size of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching). | ` ` |
|`RCLONE_VFS_CACHE_MAX_AGE`| [Max age of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching). | ` ` |
|`PLEX_USER`| The [Plex USERNAME](https://app.plex.tv/desktop/#!/settings/account) for your account. | ` ` || :heavy_check_mark:|
|`PLEX_TOKEN`| The [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) associated with PLEX_USER. | ` ` || :heavy_check_mark:|
|`PLEX_ADDRESS`| The URL of your Plex server. Example: http://192.168.0.100:32400 or http://plex:32400 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (32400). E.g., ```/``` | ` ` || :heavy_check_mark:|
|`SHOW_MENU`| Enable the plex_debrid menu to show upon startup, requiring user interaction before the program runs. Conversely if the plex_debrid menu is disabled, the program will automatically run upon successful startup. If used, the value must be ```true``` or ```false```. | `true` |
|`PD_LOGFILE`| Log file for plex_debrid. The log file will appear in the ```/config``` as ```plex_debrid.log```. If used, the value must be ```true``` or ```false```. | `false` |
|`AUTO_UPDATE`| Enable automatic updates of plex_debrid. Adding this variable will enable automatic updates to the latest version of plex_debrid locally within the container. No values are required. | `false` |
|`AUTO_UPDATE_INTERVAL`| Interval between automatic update checks in hours. #optional - if used, value must be a [Whole Number](https://www.oxfordlearnersdictionaries.com/us/definition/english/whole-number). | `24` |

## Data Volumes

The following table describes data volumes used by the container.  The mappings
are set via the `-v` parameter or via the docker-compose file within the ```volumes:``` section.  Each mapping is specified with the following
format: `<HOST_DIR>:<CONTAINER_DIR>[:PERMISSIONS]`.

| Container path  | Permissions | Description |
|-----------------|-------------|-------------|
|`/config`| rw | This is where the application stores the rclone.conf, plex_debrid settings.json, and any files needing persistency. CAUTION: rclone.conf is overwritten upon start/restart of the container. Do NOT use an existing rclone.conf file if you have other rclone services. |
|`/log`| rw | This is where the application stores its log files. |
|`/mnt`| rw | This is where rclone_RD will be mounted. Not required when only utilizing plex_debrid.   |

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
