FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_twitch_pubsub
RUN mkdir /Praxis/standalone_twitch_pubsub/bot_functions
COPY /bot_functions /Praxis/standalone_twitch_pubsub/bot_functions
COPY config.py /Praxis/standalone_twitch_pubsub
COPY badwords.py /Praxis/standalone_twitch_pubsub

COPY credentials.py /Praxis/standalone_twitch_pubsub
RUN mkdir /Praxis/standalone_twitch_pubsub/credentials
COPY /credentials /Praxis/standalone_twitch_pubsub/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_twitch_pubsub/channel_rewards
COPY /commands /Praxis/standalone_twitch_pubsub/commands

COPY requirements_sa_twitch_pubsub.txt requirements_sa_twitch_pubsub.txt
RUN pip3 install -r requirements_sa_twitch_pubsub.txt

COPY . .

CMD [ "python3", "standalone_twitch_pubsub/standalone_twitch_pubsub.py"]