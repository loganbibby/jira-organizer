FROM python:3.10-alpine

WORKDIR /app

EXPOSE 5000

VOLUME /data

COPY ./jira_organizer /app/jira_organizer
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    pip install -r /app/requirements.txt

CMD flask --app jira_organizer:app run --host=0.0.0.0
