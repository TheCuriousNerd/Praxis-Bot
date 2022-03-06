FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-twitch-script
RUN mkdir /Praxis/standalone-twitch-script/bot_functions
COPY /bot_functions /Praxis/standalone-twitch-script/bot_functions
COPY config.py /Praxis/standalone-twitch-script
COPY badwords.py /Praxis/standalone-twitch-script

COPY credentials.py /Praxis/standalone-twitch-script
RUN mkdir /Praxis/standalone-twitch-script/credentials
COPY /credentials /Praxis/standalone-twitch-script/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-twitch-script/channel_rewards
COPY /commands /Praxis/standalone-twitch-script/commands

COPY requirements_sa_twitch.txt requirements_sa_twitch.txt
RUN pip3 install -r requirements_sa_twitch.txt

COPY . .

CMD [ "python3", "standalone-twitch-script/standalone-twitch-script.py"]