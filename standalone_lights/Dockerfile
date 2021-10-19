FROM python:3.7-stretch

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_lights
RUN mkdir /Praxis/standalone_lights/bot_functions
COPY /bot_functions /Praxis/standalone_lights/bot_functions
COPY config.py /Praxis/standalone_lights
COPY badwords.py /Praxis/standalone_lights

COPY credentials.py /Praxis/standalone_lights
RUN mkdir /Praxis/standalone_lights/credentials
COPY /credentials /Praxis/standalone_lights/credentials

RUN mkdir /Praxis/channel_rewards
RUN mkdir /Praxis/commands
COPY /channel_rewards /Praxis/standalone_lights/channel_rewards
COPY /commands /Praxis/standalone_lights/commands

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_lights/standalone_lights.py"]