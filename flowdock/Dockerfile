FROM balenalib/raspberrypi3-ubuntu-python:3.7-bionic-build

WORKDIR /usr/src/app

RUN pip3 install pillow requests redis

COPY *.py ./

CMD [ "sleep", "infinity" ]

