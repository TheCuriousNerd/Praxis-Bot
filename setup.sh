#!/bin/bash
docker build --file /standalone_user_client/Dockerfile --tag standalone_user_client .
docker build --file /standalone_eventlog/Dockerfile --tag standalone_eventlog .
docker build --file /standalone_command/Dockerfile --tag standalone_command .
docker build --file /standalone_channelRewards/Dockerfile --tag standalone_channelrewards .
docker build --file /standalone_lights/Dockerfile --tag standalone_lights .
docker build --file /standalone_tts_core/Dockerfile --tag standalone_tts_core .
docker build --file /standalone_websource/Dockerfile --tag standalone_websource .
docker build --file /standalone_DiscordScript/Dockerfile --tag standalone_discordscript .
docker build --file /standalone_TwitchScript/Dockerfile --tag standalone_twitchscript .
docker build --file /standalone_Twitch_Pubsub/Dockerfile --tag standalone_twitch_pubsub .