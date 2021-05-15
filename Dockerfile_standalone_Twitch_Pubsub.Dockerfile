FROM python:3.7.10-alpine3.12

WORKDIR /Praxis

COPY requirements_sa_twitch_pubsub.txt requirements_sa_twitch_pubsub.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_twitch_pubsub.txt

COPY . .

CMD [ "python3", "standalone_twitch_pubsub.py"]