FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_twitch_script
RUN mkdir /Praxis/standalone_twitch_script/bot_functions
COPY /bot_functions /Praxis/standalone_twitch_script/bot_functions
COPY config.py /Praxis/standalone_twitch_script
COPY badwords.py /Praxis/standalone_twitch_script

COPY credentials.py /Praxis/standalone_twitch_script
RUN mkdir /Praxis/standalone_twitch_script/credentials
COPY /credentials /Praxis/standalone_twitch_script/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_twitch_script/channel_rewards
COPY /commands /Praxis/standalone_twitch_script/commands

COPY requirements_sa_twitch.txt requirements_sa_twitch.txt
RUN pip3 install -r requirements_sa_twitch.txt

COPY . .

CMD [ "python3", "standalone_twitch_script/standalone_twitch_script.py"]