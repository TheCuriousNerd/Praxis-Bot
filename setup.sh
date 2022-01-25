#!/bin/bash
docker build --file ./standalone_user_client/Dockerfile --tag standalone_user_client .
docker build --file ./standalone_db/Dockerfile --tag standalone_db .
docker build --file ./standalone_eventlog/Dockerfile --tag standalone_eventlog .
docker build --file ./standalone_command/Dockerfile --tag standalone_command .
docker build --file ./standalone_channelrewards/Dockerfile --tag standalone_channelrewards .
docker build --file ./standalone_lights/Dockerfile --tag standalone_lights .
docker build --file ./standalone_tts_core/Dockerfile --tag standalone_tts_core .
docker build --file ./standalone_webSource/Dockerfile --tag standalone_websource .
docker build --file ./standalone_discord_script/Dockerfile --tag standalone_discord_script .
docker build --file ./standalone_twitch_script/Dockerfile --tag standalone_twitch_script .
docker build --file ./standalone_twitch_pubsub/Dockerfile --tag standalone_twitch_pubsub .