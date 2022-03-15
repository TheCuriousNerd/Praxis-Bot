FROM python:3.7-stretch

WORKDIR /Praxis


RUN mkdir /Praxis/standalone-core
RUN mkdir /Praxis/standalone-core/bot_functions
COPY /bot_functions /Praxis/standalone-core/bot_functions
COPY config.py /Praxis/standalone-core
COPY badwords.py /Praxis/standalone-core

COPY credentials.py /Praxis/standalone-core
RUN mkdir /Praxis/standalone-core/credentials
COPY /credentials /Praxis/standalone-core/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-core/channel_rewards
COPY /commands /Praxis/standalone-core/commands

COPY requirements_sa_db.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "standalone-core/standalone-core.py"]