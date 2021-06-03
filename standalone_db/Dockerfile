
FROM python:3.10.0a7-alpine3.13

WORKDIR /Praxis


RUN mkdir /Praxis/standalone_db
RUN mkdir /Praxis/standalone_db/bot_functions
COPY /bot_functions /Praxis/standalone_db/bot_functions
COPY config.py /Praxis/standalone_db
COPY badwords.py /Praxis/standalone_db

COPY credentials.py /Praxis/standalone_db
RUN mkdir /Praxis/standalone_db/credentials
COPY /credentials /Praxis/standalone_db/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_db/channel_rewards
COPY /commands /Praxis/standalone_db/commands

COPY requirements_sa_db.txt requirements.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "standalone_db/standalone_db.py"]