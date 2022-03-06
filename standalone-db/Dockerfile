
FROM python:3.7-stretch

WORKDIR /Praxis


RUN mkdir /Praxis/standalone-db
RUN mkdir /Praxis/standalone-db/bot_functions
COPY /bot_functions /Praxis/standalone-db/bot_functions
COPY config.py /Praxis/standalone-db
COPY badwords.py /Praxis/standalone-db

COPY credentials.py /Praxis/standalone-db
RUN mkdir /Praxis/standalone-db/credentials
COPY /credentials /Praxis/standalone-db/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-db/channel_rewards
COPY /commands /Praxis/standalone-db/commands

COPY requirements_sa_db.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "standalone-db/standalone-db.py"]