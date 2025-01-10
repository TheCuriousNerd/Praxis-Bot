FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-websource
RUN mkdir /Praxis/standalone-websource/bot_functions
COPY /bot_functions /Praxis/standalone-websource/bot_functions
COPY config.py /Praxis/standalone-websource
COPY badwords.py /Praxis/standalone-websource

COPY credentials.py /Praxis/standalone-websource
RUN mkdir /Praxis/standalone-websource/credentials
COPY /credentials /Praxis/standalone-websource/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-websource/channel_rewards
COPY /commands /Praxis/standalone-websource/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-websource/standalone-websource.py"]