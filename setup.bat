echo "Creating Praxis Bot Images..."

start powershell docker build --file ./standalone_user_client/Dockerfile --tag standalone_user_client .
start powershell docker build --file ./standalone_db/Dockerfile --tag standalone_db .
start powershell docker build --file ./standalone_eventLog/Dockerfile --tag standalone_eventlog .
start powershell docker build --file ./standalone_channelrewards/Dockerfile --tag standalone_channelrewards .
start powershell docker build --file ./standalone_command/Dockerfile --tag standalone_command .
start powershell docker build --file ./standalone_lights/Dockerfile --tag standalone_lights .
start powershell docker build --file ./standalone_tts_core/Dockerfile --tag standalone_tts_core .
start powershell docker build --file ./standalone_websource/Dockerfile --tag standalone_websource .
start powershell docker build --file ./standalone_discord_script/Dockerfile --tag standalone_discord_script .
start powershell docker build --file ./standalone_twitch_script/Dockerfile --tag standalone_twitch_script .
start powershell docker build --file ./standalone_twitch_pubsub/Dockerfile --tag standalone_twitch_pubsub .
