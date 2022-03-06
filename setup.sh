#!/bin/bash
docker build --file ./standalone-user-client/Dockerfile --tag standalone-user-client .
docker build --file ./standalone-db/Dockerfile --tag standalone-db .
docker build --file ./standalone-eventlog/Dockerfile --tag standalone-eventlog .
docker build --file ./standalone-command/Dockerfile --tag standalone-command .
docker build --file ./standalone-channelrewards/Dockerfile --tag standalone-channelrewards .
docker build --file ./standalone-lights/Dockerfile --tag standalone-lights .
docker build --file ./standalone-tts-core/Dockerfile --tag standalone-tts-core .
docker build --file ./standalone-websource/Dockerfile --tag standalone-websource .
docker build --file ./standalone-discord-script/Dockerfile --tag standalone-discord-script .
docker build --file ./standalone-twitch-script/Dockerfile --tag standalone-twitch-script .
docker build --file ./standalone-twitch-pubsub/Dockerfile --tag standalone-twitch-pubsub .