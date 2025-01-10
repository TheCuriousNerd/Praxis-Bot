FROM python:3.8

WORKDIR /Praxis

RUN mkdir /Praxis/standalone-lights
RUN mkdir /Praxis/standalone-lights/bot_functions
COPY /bot_functions /Praxis/standalone-lights/bot_functions
COPY config.py /Praxis/standalone-lights
COPY badwords.py /Praxis/standalone-lights

COPY credentials.py /Praxis/standalone-lights
RUN mkdir /Praxis/standalone-lights/credentials
COPY /credentials /Praxis/standalone-lights/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone-lights/channel_rewards
COPY /commands /Praxis/standalone-lights/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone-lights/standalone-lights.py"]