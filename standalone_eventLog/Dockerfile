FROM python:3.7.10-alpine3.12

WORKDIR /Praxis

RUN mkdir /Praxis/standalone_eventLog
RUN mkdir /Praxis/standalone_eventLog/bot_functions
COPY /bot_functions /Praxis/standalone_eventLog/bot_functions
COPY config.py /Praxis/standalone_eventLog
COPY badwords.py /Praxis/standalone_eventLog

COPY requirements_sa_command.txt requirements_sa_command.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_eventLog/standalone_eventLog.py"]