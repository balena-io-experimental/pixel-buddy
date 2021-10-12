FROM balenalib/raspberrypi3-python:3.7

RUN install_packages libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libmtdev-dev

RUN pip install kivy -i https://www.piwheels.org/simple

WORKDIR /usr/src/app

COPY hello.py ./


COPY images images


COPY start.sh ./


CMD ["bash","./start.sh"]