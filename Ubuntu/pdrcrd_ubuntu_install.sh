#! /bin/bash
set -e
echo $'beta v0.01\n'

echo $'Do you wish to install docker?\n'
select yn in "Yes" "No"; do
    case $yn in
        Yes ) sudo apt-get remove docker docker-engine docker.io containerd runc 2>/dev/null || true ; 
              sudo apt-get update;
              sudo apt-get install -y \
                 ca-certificates \
                 curl \
                 gnupg; 
              sudo mkdir -m 0755 -p /etc/apt/keyrings; 
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg; 
              echo \
                "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
              sudo tee /etc/apt/sources.list.d/docker.list > /dev/null;
              sudo apt-get update;
              echo "Setting up docker";
              sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin;
              echo $'\n';
              echo $'docker install complete\n';
              break;;
        No ) echo $'\n'; break;;
    esac
done

echo $'Do you wish to install pdrcrd?\n'
select yn in "Yes" "No"; do
    case $yn in
        Yes ) echo $'\nDo you wish to set the config directory?  defualt: /etc/docker/config \n';
                select yn in "Yes" "No"; do
                    case $yn in
                        Yes ) echo  $'\nPlease input the absolute path for your config directory. defualt: /etc/docker/config \n';
                              read -p 'Config Path: ' configpathvar && echo $'\n';
                              echo $'The config directory path is set to' $configpathvar && echo $'\n';
                              break;;
                        No )  sudo mkdir /etc/docker/config 2>/dev/null || true; 
                              configpathvar=/etc/docker/config; 
                              echo $'The config directory path is set to' $configpathvar && echo $'\n';
                              break;;
                    esac
                done  
              echo $'Do you wish to set the log directory?  defualt: /etc/docker/log \n';
                select yn in "Yes" "No"; do
                    case $yn in
                        Yes ) echo $'\nPlease input the absolute path for your log directory. defualt: /etc/docker/log \n';
                              read -p 'Log Path: ' logpathvar && echo $'\n';
                              echo "The log directory path is set to" $logpathvar && echo $'\n';
                              break;;
                        No )  sudo mkdir /etc/docker/log 2>/dev/null || true; 
                              logpathvar=/etc/docker/log; 
                              echo $'The log directory path is set to' $logpathvar && echo $'\n';
                              break;;
                    esac
                done  
              echo $'Do you wish to set the rclone mount directory?  defualt: /etc/docker/mnt \n';
                select yn in "Yes" "No"; do
                    case $yn in
                        Yes ) echo $'\nPlease input the absolute path for your rclone mount directory. defualt: /etc/docker/log \n';
                              read -p 'Rclone Mount Directory: ' mntdirvar && echo $'\n';
                              echo "The rclone mount directory path is set to" $mntdirevar && echo $'\n';
                              break;;
                        No )  sudo mkdir /etc/docker/mnt 2>/dev/null || true; 
                              export mntdirvar=/etc/docker/mnt; 
                              echo "The rclone mount directory path is set to" $mntdirevar && echo $'\n';
                              break;;
                    esac
                done                  
              echo $'Do you wish to set the rclone mount name?  defualt: realdebrid \n';
                select yn in "Yes" "No"; do
                    case $yn in
                        Yes ) echo $'\nPlease input the rclone mount name \n';
                              read -p 'Rclone Mount Name: ' mntnmvar && echo $'\n';
                              echo "The rclone mount name is set to" $mntnmvar && echo $'\n';
                              break;;
                        No )  mntnmvar=realdebrid; 
                              echo "The rclone mount name is set to" $mntnmvar && echo $'\n';
                              break;;
                    esac
                done
              echo $'Please input your Real Debrid API Key.\n';                
              read -p 'Real Debrid API Key: ' rdapikey && echo $'\n';
              echo $'Please input your Plex Server Address -- Example: http://localhost:32400\n';                
              read -p 'Plex Server Address: ' plexsa && echo $'\n';                    
              echo $'Please input your Plex Username.\n';                
              read -p 'Plex Username: ' plexun && echo $'\n';
              echo $'Please input your Plex Token.\n';                
              read -p 'Plex Token: ' plextk && echo $'\n';             
              TZ="$(cat /etc/timezone)"   
sudo tee /etc/docker/docker-compose.yml << EOF  
services:
  pdrcrd:
    container_name: pdrcrd
    image: iampuid0/pdrcrd:latest
    stdin_open: true # docker run -i
    tty: true        # docker run -t    
    volumes:
      - $configpathvar:/config # rclone.conf & settings.json will both be here on the host CAUTION: rclone.conf is overwritten upon start/restart of the container
      - $logpathvar:/log # logs will be here on the host
      - $mntdirvar:/data:shared #rclone mount will be here on the host  
    environment:
      - TZ=$TZ
      - RD_API_KEY=$rdapikey
      - RCLONE_MOUNT_NAME=$mntnmvar
      - RCLONE_LOG_LEVEL=INFO
      - RCLONE_LOG_FILE=/log/$mntnmvar.txt  
      - RCLONE_DIR_CACHE_TIME=10s #optional, but recommended as default
#      - RCLONE_CACHE_DIR=/cache #optional
#      - RCLONE_VFS_CACHE_MODE=full #optional
#      - RCLONE_VFS_CACHE_MAX_SIZE=100G #optional
#      - RCLONE_VFS_CACHE_MAX_AGE=1h #optional
#      - RCLONE_DIR_PERMS=777 #optional, not functional in beta
#      - RCLONE_FILE_PERMS=777 #optional, not functional in beta
#      - RCLONE_UMASK= #optional, not functional in beta
      - PLEX_USER=$plexun  #required 
      - PLEX_TOKEN=$plextk  #required - see link for detail https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
      - PLEX_ADDRESS=$plexsa #required - format must include http:// and have no trailing characters after 32400 e.g / 
      - SHOW_MENU=false  #optional - if used, value must be true or false -- default is true
#       - PD_LOGFILE=true  #optional - if used, value must be true or false -- default is false
    devices:
      - /dev/fuse:/dev/fuse:rwm
    cap_add:
      - SYS_ADMIN     
    security_opt:
      - apparmor:unconfined    
      - no-new-privileges
#    restart: unless-stopped
EOF
              break;;
        No ) echo $'\n'; break;;
    esac
done
echo $'Do you wish to start pdrcrd?\n'
select yn in "Yes" "No"; do
    case $yn in
        Yes ) sudo docker-compose -f /etc/docker/docker-compose.yml up -d; 
              break;;
        No ) echo $'\n'; break;;
    esac
done
echo $'Do you wish to open the rclone_RD mount with windows explorer?\n'
select yn in "Yes" "No"; do
    case $yn in
        Yes ) explorer.exe `wslpath -w "$mntdirvar"`.; 
              break;;
        No ) echo $'\n'; break;;
    esac
done