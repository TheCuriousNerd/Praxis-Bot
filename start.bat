
echo "Starting Praxis Bot Services..."

start /wait powershell cd "standalone-core" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-user-client" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-eventlog" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-command" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-channelrewards" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-lights" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-tts-core" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-websource" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-discord-script" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-twitch-script" ; docker-compose up -d ; cd ".."
start powershell cd "standalone-twitch-pubsub" ; docker-compose up -d ; cd ".."
