FROM python:3.6

RUN pip install --upgrade pip; \
    apt-get update; \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/project
ADD requirements.txt /home/project/
WORKDIR /home/project/

RUN pip install -r requirements.txt