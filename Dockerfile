FROM golang:alpine AS builder
ADD https://github.com/itsToggle/rclone_RD/archive/refs/heads/master.zip /
RUN \
  apk add --update --no-cache zip && unzip /master.zip && \
  cd rclone_RD-master && CGO_ENABLED=0 go build -tags cmount

FROM alpine:latest
COPY --from=builder /go/rclone_RD-master/rclone /rclone-linux
ADD https://github.com/itsToggle/plex_debrid/archive/refs/heads/main.zip /
ADD . / ./
ENV \
  XDG_CONFIG_HOME=/config \
  TERM=xterm 
RUN \
  apk add --update --no-cache gcompat libstdc++ libxml2-utils curl tzdata nano ca-certificates wget fuse python3 build-base py3-pip python3-dev linux-headers && \
  ln -sf python3 /usr/bin/python && \
  mkdir /config && touch /config/ignored.txt && \     
  chmod 711 rclone-linux &&\
  unzip main.zip && rm main.zip && \
  mv plex_debrid-main/ plex_debrid && \   
  python3 -m venv /venv && \
  source /venv/bin/activate && \
  pip3 install --upgrade pip && \
  pip3 install -r /plex_debrid/requirements.txt && \
  pip3 install -r /requirements.txt
VOLUME /config  
HEALTHCHECK --interval=60s --timeout=10s \
  CMD ["/bin/sh", "-c", "source /venv/bin/activate && python /healthcheck.py"]
ENTRYPOINT ["/bin/sh", "-c", "source /venv/bin/activate && python /main.py"]