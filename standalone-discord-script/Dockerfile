FROM python:3.8-bullseye

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-discord-script
RUN mkdir /Praxis/standalone-discord-script/bot_functions
COPY /bot_functions /Praxis/standalone-discord-script/bot_functions
COPY config.py /Praxis/standalone-discord-script
COPY badwords.py /Praxis/standalone-discord-script

COPY credentials.py /Praxis/standalone-discord-script
RUN mkdir /Praxis/standalone-discord-script/credentials
COPY /credentials /Praxis/standalone-discord-script/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-discord-script/channel_rewards
COPY /commands /Praxis/standalone-discord-script/commands

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.8-dev
RUN apt-get install libnacl-dev
RUN apt-get install libffi-dev
RUN apt-get install -y ffmpeg

COPY requirements_sa_discord.txt requirements_sa_discord.txt
RUN pip3 install -r requirements_sa_discord.txt
RUN pip3 install novus[voice]

COPY . .

CMD [ "python3", "standalone-discord-script/standalone-discord-script.py"]