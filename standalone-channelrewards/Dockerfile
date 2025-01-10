FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-channelrewards
RUN mkdir /Praxis/standalone-channelrewards/bot_functions
COPY /bot_functions /Praxis/standalone-channelrewards/bot_functions
COPY config.py /Praxis/standalone-channelrewards
COPY badwords.py /Praxis/standalone-channelrewards

COPY credentials.py /Praxis/standalone-channelrewards
RUN mkdir /Praxis/standalone-channelrewards/credentials
COPY /credentials /Praxis/standalone-channelrewards/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-channelrewards/channel_rewards
COPY /commands /Praxis/standalone-channelrewards/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-channelrewards/standalone-channelrewards.py"]
