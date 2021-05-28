
cd "standalone_user_client"
docker-compose up -d
cd ".."
cd "standalone_db"
docker-compose up -d
cd ".."
cd "standalone_eventLog"
docker-compose up -d
cd ".."
cd "standalone_command"
docker-compose up -d
cd ".."
cd "standalone_channelrewards"
docker-compose up -d
cd ".."
cd "standalone_lights"
docker-compose up -d
cd ".."
cd "standalone_tts_core"
docker-compose up -d
cd ".."
cd "standalone_websource"
docker-compose up -d
cd ".."
cd "standalone_discord_script"
docker-compose up -d
cd ".."
cd "standalone_twitch_script"
docker-compose up -d
cd ".."
cd "standalone_twitch_pubsub"
docker-compose up -d
