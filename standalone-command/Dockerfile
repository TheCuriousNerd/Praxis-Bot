FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-command
RUN mkdir /Praxis/standalone-command/bot_functions
COPY /bot_functions /Praxis/standalone-command/bot_functions
COPY config.py /Praxis/standalone-command
COPY badwords.py /Praxis/standalone-command

COPY credentials.py /Praxis/standalone-command
RUN mkdir /Praxis/standalone-command/credentials
COPY /credentials /Praxis/standalone-command/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-command/channel_rewards
COPY /commands /Praxis/standalone-command/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-command/standalone-command.py"]