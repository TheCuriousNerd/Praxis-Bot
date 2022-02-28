#!/bin/bash
python twitch_generate_credentials.py autostart
cd "standalone_twitch_pubsub"
docker-compose up -d
cd ..