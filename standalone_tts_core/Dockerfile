FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_tts_core
RUN mkdir /Praxis/standalone_tts_core/bot_functions
COPY /bot_functions /Praxis/standalone_tts_core/bot_functions
COPY config.py /Praxis/standalone_tts_core
COPY badwords.py /Praxis/standalone_tts_core

COPY credentials.py /Praxis/standalone_tts_core
RUN mkdir /Praxis/standalone_tts_core/credentials
COPY /credentials /Praxis/standalone_tts_core/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_tts_core/channel_rewards
COPY /commands /Praxis/standalone_tts_core/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_tts_core/standalone_tts_core.py"]