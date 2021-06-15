
echo "Starting Praxis Bot Services..."

start powershell cd "standalone_user_client" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_db" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_eventLog" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_command" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_channelrewards" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_lights" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_tts_core" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_websource" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_discord_script" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_twitch_script" ; docker-compose up -d ; cd ".."
start powershell cd "standalone_twitch_pubsub" ; docker-compose up -d ; cd ".."
