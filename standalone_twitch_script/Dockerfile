FROM python:3.10.0a7-alpine3.13

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_twitch_script
RUN mkdir /Praxis/standalone_twitch_script/bot_functions
COPY /bot_functions /Praxis/standalone_twitch_script/bot_functions
COPY config.py /Praxis/standalone_twitch_script
COPY badwords.py /Praxis/standalone_twitch_script

COPY requirements_sa_twitch.txt requirements_sa_twitch.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_twitch.txt

COPY . .

CMD [ "python3", "standalone_twitch_script/standalone_twitch_script.py"]