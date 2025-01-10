FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-tts-core
RUN mkdir /Praxis/standalone-tts-core/bot_functions
COPY /bot_functions /Praxis/standalone-tts-core/bot_functions
COPY config.py /Praxis/standalone-tts-core
COPY badwords.py /Praxis/standalone-tts-core

COPY credentials.py /Praxis/standalone-tts-core
RUN mkdir /Praxis/standalone-tts-core/credentials
COPY /credentials /Praxis/standalone-tts-core/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-tts-core/channel_rewards
COPY /commands /Praxis/standalone-tts-core/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-tts-core/standalone-tts-core.py"]