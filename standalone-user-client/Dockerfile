FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-user-client
RUN mkdir /Praxis/standalone-user-client/bot_functions
COPY /bot_functions /Praxis/standalone-user-client/bot_functions
COPY config.py /Praxis/standalone-user-client
COPY badwords.py /Praxis/standalone-user-client

COPY credentials.py /Praxis/standalone-user-client
RUN mkdir /Praxis/standalone-user-client/credentials
COPY /credentials /Praxis/standalone-user-client/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-user-client/channel_rewards
COPY /commands /Praxis/standalone-user-client/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-user-client/standalone-user-client.py"]