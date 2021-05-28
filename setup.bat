# powershell
start docker build --file ./standalone_user_client/Dockerfile --tag standalone_user_client .
start docker build --file ./standalone_eventLog/Dockerfile --tag standalone_eventlog .
start docker build --file ./standalone_channelrewards/Dockerfile --tag standalone_channelrewards .
start docker build --file ./standalone_command/Dockerfile --tag standalone_command .
start docker build --file ./standalone_lights/Dockerfile --tag standalone_lights .
start docker build --file ./standalone_tts_core/Dockerfile --tag standalone_tts_core .
start docker build --file ./standalone_websource/Dockerfile --tag standalone_websource .
start docker build --file ./standalone_discord_script/Dockerfile --tag standalone_discord_script .
start docker build --file ./standalone_twitch_script/Dockerfile --tag standalone_twitch_script .
start docker build --file ./standalone_twitch_pubsub/Dockerfile --tag standalone_twitch_pubsub .