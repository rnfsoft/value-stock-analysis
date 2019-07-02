FROM python:3.7-slim


RUN python -m pip install --upgrade pip

RUN mkdir -p /home/project/dash_app
WORKDIR /home/project/dash_app
COPY requirements.txt /home/project/dash_app
RUN python -m pip install -r requirements.txt

COPY . /home/project/dash_app