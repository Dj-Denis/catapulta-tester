FROM python:3.6

RUN pip install --upgrade pip; \
    apt-get update; \
    apt-get install -y supervisor; \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/project
ADD requirements.txt /home/project/
RUN mkdir -p /home/.conf/supervisor.d
ADD .conf/supervisor.d/django.conf /home/.conf/supervisor.d/django.conf
WORKDIR /home/project/


ENV PYTHONUNBUFFERED=0

RUN pip install -r requirements.txt