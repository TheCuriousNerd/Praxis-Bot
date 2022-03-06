FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-twitch-pubsub
RUN mkdir /Praxis/standalone-twitch-pubsub/bot_functions
COPY /bot_functions /Praxis/standalone-twitch-pubsub/bot_functions
COPY config.py /Praxis/standalone-twitch-pubsub
COPY badwords.py /Praxis/standalone-twitch-pubsub

COPY credentials.py /Praxis/standalone-twitch-pubsub
RUN mkdir /Praxis/standalone-twitch-pubsub/credentials
COPY /credentials /Praxis/standalone-twitch-pubsub/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-twitch-pubsub/channel_rewards
COPY /commands /Praxis/standalone-twitch-pubsub/commands

COPY requirements_sa_twitch_pubsub.txt requirements_sa_twitch_pubsub.txt
RUN pip3 install -r requirements_sa_twitch_pubsub.txt

COPY . .

CMD [ "python3", "standalone-twitch-pubsub/standalone-twitch-pubsub.py"]