FROM python:3.10.2-slim-bullseye

MAINTAINER Hamed Khosravi <hmdkhsrvee@gmail.com>

RUN mkdir /trello
WORKDIR /trello

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y python3-pip

ADD requirements.txt /trello
RUN pip install -r requirements.txt
ADD . /trello
