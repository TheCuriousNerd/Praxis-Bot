FROM python:3.10.0a7-alpine3.13

WORKDIR /Praxis

COPY requirements_sa_discord.txt requirements_sa_discord.txt
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip3 install -r requirements_sa_discord.txt

COPY . .

CMD [ "python3", "standalone_discord_script.py"]