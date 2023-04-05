FROM golang:alpine AS builder
ADD https://github.com/itsToggle/rclone_RD/archive/refs/heads/master.zip /
RUN \
  apk add --update --no-cache zip && unzip /master.zip && \
  cd rclone_RD-master && CGO_ENABLED=0 go build -tags cmount

FROM alpine:latest
COPY --from=builder /go/rclone_RD-master/rclone /rclone-linux
ADD https://github.com/itsToggle/plex_debrid/archive/refs/heads/experimental.zip /
ADD setup.sh /
ADD pd_setup.py /
ADD settings-default.json /
ENV \
  XDG_CONFIG_HOME=/config \
  TERM=xterm 
RUN \
  apk add --update --no-cache tzdata fuse python3 && ln -sf python3 /usr/bin/python && \
  python3 -m ensurepip && \
  pip3 install --no-cache --upgrade pip setuptools python-dotenv && \
  mkdir /config && touch /config/ignored.txt && \     
  chmod 711 rclone-linux && chmod 755 /setup.sh && \
  unzip experimental.zip && rm experimental.zip && \
  mv plex_debrid-experimental/ plex_debrid && rm /plex_debrid/README.md && rm /plex_debrid/Dockerfile && rm -R /plex_debrid/.github && \  
  pip install -r /plex_debrid/requirements.txt 
VOLUME /config  
CMD ./setup.sh;/bin/sh
