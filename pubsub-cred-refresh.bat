python twitch_generate_credentials.py
docker build --file ./standalone_twitch_pubsub/Dockerfile --tag standalone_twitch_pubsub .
cd "standalone_twitch_pubsub"
docker-compose up -d