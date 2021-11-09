FROM python:3.8-bullseye

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_discord_script
RUN mkdir /Praxis/standalone_discord_script/bot_functions
COPY /bot_functions /Praxis/standalone_discord_script/bot_functions
COPY config.py /Praxis/standalone_discord_script
COPY badwords.py /Praxis/standalone_discord_script

COPY credentials.py /Praxis/standalone_discord_script
RUN mkdir /Praxis/standalone_discord_script/credentials
COPY /credentials /Praxis/standalone_discord_script/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_discord_script/channel_rewards
COPY /commands /Praxis/standalone_discord_script/commands

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.8-dev
RUN apt-get install libnacl-dev
RUN apt-get install libffi-dev

COPY requirements_sa_discord.txt requirements_sa_discord.txt
RUN pip3 install -r requirements_sa_discord.txt
RUN pip3 install novus[voice]

COPY . .

CMD [ "python3", "standalone_discord_script/standalone_discord_script.py"]