FROM golang:alpine AS builder
ADD https://github.com/itsToggle/rclone_RD/archive/refs/heads/master.zip /
RUN \
  apk add --update --no-cache zip && unzip /master.zip && \
  cd rclone_RD-master && CGO_ENABLED=0 go build -tags cmount

FROM alpine:latest
COPY --from=builder /go/rclone_RD-master/rclone /rclone-linux
ADD https://github.com/itsToggle/plex_debrid/archive/refs/heads/main.zip /
ADD setup.sh /
ADD pd_setup.py /
ADD settings-default.json /
ENV \
  XDG_CONFIG_HOME=/config \
  TERM=xterm 
RUN \
  apk add --update --no-cache tzdata ca-certificates coreutils wget fuse python3 build-base py3-pip python3-dev py3-dotenv && ln -sf python3 /usr/bin/python && \
  mkdir /config && touch /config/ignored.txt && \     
  chmod 711 rclone-linux && chmod 755 /setup.sh && \
  unzip main.zip && rm main.zip && \
  mv plex_debrid-main/ plex_debrid && rm /plex_debrid/README.md && rm /plex_debrid/Dockerfile && rm -R /plex_debrid/.github && \  
  pip3 install -r /plex_debrid/requirements.txt 
VOLUME /config  
CMD ./setup.sh;/bin/bash
