#!/bin/bash
docker build --file Dockerfile_standalone_user_client.Dockerfile --tag standalone_user_client .
docker build --file Dockerfile_standalone_eventlog.Dockerfile --tag standalone_eventlog .
docker build --file Dockerfile_standalone_command.Dockerfile --tag standalone_command .
docker build --file Dockerfile_standalone_channelRewards.Dockerfile --tag standalone_channelrewards .
docker build --file Dockerfile_standalone_lights.Dockerfile --tag standalone_lights .
docker build --file Dockerfile_standalone_tts_core.Dockerfile --tag standalone_tts_core .
docker build --file Dockerfile_standalone_websource.Dockerfile --tag standalone_websource .
docker build --file Dockerfile_standalone_DiscordScript.Dockerfile --tag standalone_discordscript .
docker build --file Dockerfile_standalone_TwitchScript.Dockerfile --tag standalone_twitchscript .
docker build --file Dockerfile_standalone_Twitch_Pubsub.Dockerfile --tag standalone_twitch_pubsub .