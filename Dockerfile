FROM alpine:latest
LABEL description="webstringer\
Authored by JeffTadashi\
https://hub.docker.com/u/jefftadashi\
https://github.com/JeffTadashi/webstringer"

RUN \
apk update && \
apk add --upgrade --no-cache git python3 && \
git clone https://github.com/JeffTadashi/webstringer /opt/webstringer && \
pip3 install -r /opt/webstringer/requirements.txt && \
ln -s /opt/webstringer/webstringer.py /usr/local/bin/webstringer && \
apk del git

RUN mkdir /vol
VOLUME /vol
WORKDIR /vol

ENTRYPOINT ["webstringer"]
CMD [ "-h"]