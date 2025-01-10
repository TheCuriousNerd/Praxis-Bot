FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-eventlog
RUN mkdir /Praxis/standalone-eventlog/bot_functions
COPY /bot_functions /Praxis/standalone-eventlog/bot_functions
COPY config.py /Praxis/standalone-eventlog
COPY badwords.py /Praxis/standalone-eventlog

COPY credentials.py /Praxis/standalone-eventlog
RUN mkdir /Praxis/standalone-eventlog/credentials
COPY /credentials /Praxis/standalone-eventlog/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-eventlog/channel_rewards
COPY /commands /Praxis/standalone-eventlog/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-eventlog/standalone-eventlog.py"]