#!/bin/bash
python3 twitch_generate_credentials.py autostart
cd "standalone-twitch-pubsub"
docker-compose up -d
cd ..