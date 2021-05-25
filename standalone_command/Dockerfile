FROM python:3.10.0a7-alpine3.13

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_command
RUN mkdir /Praxis/standalone_command/bot_functions
COPY /bot_functions /Praxis/standalone_command/bot_functions
COPY config.py /Praxis/standalone_command
COPY badwords.py /Praxis/standalone_command

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_command/standalone_command.py"]