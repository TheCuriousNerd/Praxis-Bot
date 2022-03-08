#!/bin/bash
cd "standalone-core"
docker-compose up -d
cd ".."
cd "standalone-user-client"
docker-compose up -d
cd ".."
cd "standalone-eventlog"
docker-compose up -d
cd ".."
cd "standalone-command"
docker-compose up -d
cd ".."
cd "standalone-channelrewards"
docker-compose up -d
cd ".."
cd "standalone-lights"
docker-compose up -d
cd ".."
cd "standalone-tts-core"
docker-compose up -d
cd ".."
cd "standalone-websource"
docker-compose up -d
cd ".."
cd "standalone-discord-script"
docker-compose up -d
cd ".."
cd "standalone-twitch-script"
docker-compose up -d
cd ".."
cd "standalone-twitch-pubsub"
docker-compose up -d
cd ".."