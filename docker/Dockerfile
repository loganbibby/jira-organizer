FROM python:3.10-alpine

WORKDIR /app

EXPOSE 5000

VOLUME /data

ENV CONFIG_MODULE="jira_organizer.config.docker"

COPY ./jira_organizer /app/jira_organizer
COPY ./requirements.txt /app/requirements.txt
COPY ./docker/docker_config.py /app/jira_organizer/config/docker.py

RUN pip install --upgrade pip \
    pip install -r /app/requirements.txt

CMD flask --app jira_organizer:app run --host=0.0.0.0
