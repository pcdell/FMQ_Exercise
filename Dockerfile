FROM ubuntu:latest

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt install systemd -y
RUN apt install python3 python3-pip -y
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
RUN apt install mysql-server -y

COPY ./static ./static

COPY ./templates ./templates

COPY .env .
COPY app.py .
COPY models.py .
COPY requirements.txt .
COPY mysqlsampledatabase.sql .
COPY startup.sh .


RUN python3 -m pip install --upgrade pip setuptools --break-system-packages
RUN python3 -m pip install -r requirements.txt --break-system-packages