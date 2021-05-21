FROM python:3.7.10-alpine3.12

WORKDIR /Praxis

COPY /bot_functions_test /PraxisStreamTest/
COPY /bot_functions_test /Praxis/

RUN mkdir /Setup
RUN mkdir /Setup/bot_functions_test
COPY /bot_functions_test /Setup/bot_functions_test

RUN mv /Setup/bot_functions_test/* /Praxis/



COPY requirements_sa_command.txt requirements_sa_command.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_command.txt

COPY . .

CMD [ "python3", "standalone_channelrewards.py"]