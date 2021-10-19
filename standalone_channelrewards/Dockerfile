FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_channelrewards
RUN mkdir /Praxis/standalone_channelrewards/bot_functions
COPY /bot_functions /Praxis/standalone_channelrewards/bot_functions
COPY config.py /Praxis/standalone_channelrewards
COPY badwords.py /Praxis/standalone_channelrewards

COPY credentials.py /Praxis/standalone_channelrewards
RUN mkdir /Praxis/standalone_channelrewards/credentials
COPY /credentials /Praxis/standalone_channelrewards/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_channelrewards/channel_rewards
COPY /commands /Praxis/standalone_channelrewards/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_channelrewards/standalone_channelrewards.py"]
