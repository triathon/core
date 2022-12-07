FROM python:3.8.9-slim
WORKDIR /app
COPY . .
RUN apt-get -qy update
RUN apt-get -qy install gcc
RUN apt-get -qy install libpq-dev
RUN apt-get -qy install git
RUN apt-get -qy install wget
RUN python -m pip install --upgrade pip && pip install --user -r requirementsDev.txt

RUN cd /usr/local &&\
wget https://npmmirror.com/mirrors/node/v16.18.0/node-v16.18.0-linux-x64.tar.xz &&\
tar xvf node-v16.18.0-linux-x64.tar.xz &&\
mv node-v16.18.0-linux-x64 nodejs &&\
ln -s /usr/local/nodejs/bin/node /usr/bin/node &&\
ln -s /usr/local/nodejs/bin/npm /usr/bin/npm &&\

RUN solc-select install 0.4.26
RUN solc-select install 0.5.16
RUN solc-select install 0.6.11
RUN solc-select install 0.7.6
RUN solc-select install 0.8.16
RUN solc-select use 0.8.16