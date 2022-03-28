# Praxis Bot

Praxis Bot is software that focuses on improving communication and management between people, processes, and services. This bot aims to assist and enhance live streams, digital exhibits, chat rooms, and other countless spaces or venues.

The bot provides and assists with several things like custom commands, channel rewards, stream sources, digital or practical effects, and moderation support, especially across multiple platforms and systems simultaneously.

<br>

Table of Contents:
* [Requirements](/#Requirements)
* [Docker](/#Docker)
* [User TTS Speaker](/#User-TTS-Speaker)
* [Dashboard](/#Dashboard)
* [Credentials](/#Credentials)

___

# Requirements:
- Docker (For the Standalone Containers)
- Python (Min Version > 3.7 for TTS Speaker)<br>
*(After install remember to use: `pip install -r requirements.txt`)*

<br>

___

# Docker:

This bot primarily uses docker to run various services.
To install Docker for windows visit: https://www.docker.com/get-started

## Image Setup:

Use the following command in the terminal to setup all the images after you make the credentials.

Windows: `setup.bat`<br>
Linux / macOS: `setup.sh`


## Docker-Compose Info:

Use the following command to start up all the standalone containers based on the images you just created after you clone the repository.

To Start:

Windows: `start.bat`<br>
Linux / macOS: `start.sh`<br>

To Stop:

Windows: `stop.bat`<br>
Linux / macOS: `stop.sh`<br>

<br>

___

# User TTS Speaker:
To receive audio from standalone_tt_core.py launch standalone_tts_speaker.py.

`python standalone_tts_speaker.py`

or

Windows: `praxis-tts-speaker.bat`<br>
Linux / macOS: `praxis-tts-speaker.sh`<br>
*(Modify these to match the correct directory! Or no work for YOU!!!)*<br>
*(Also be sure to have requirements setup!!!)*<br>
<br>
___

# Dashboard:

Once Praxis Bot is setup, to access the Dashboard visit `localhost:42808`(NGINX) or `localhost:8000`(Django) in your browser.<br>
<br>
___

# Credentials:

## Credentials Setup:

Create a json based on the templates and put them into the `/credentials/` folder.
Refer to the `/credential_templates/` folder for examples.<br>
<br>

## For Twitch Credentials:

### Twitch IRC Chat Credentials:
Username = `TwitchUsername` *(Must match ***credentialsNickname*** in config)*

Helix Client ID = `https://dev.twitch.tv/console/apps`

Oauth = `https://twitchapps.com/tmi/`

V5 Client ID = `https://twitchtokengenerator.com/`

### Twitch PubSub Credentials:

pubsub_client_id = `https://dev.twitch.tv/console/apps` Set url to `http://localhost:17563`<br>
pubsub_secret = `^Look at Instructions Above^`<br>

pubsub_AccessToken = Generate by using: `python twitch_generate_credentials.py`<br>
pubsub_RefreshToken = `^Look at Instructions Above^`<br>
<br>

## For Database Credentials:

Nickname = `Anything You Want` *(Must match ***credentialsNickname*** in config)*

Engine Example = `"postgresql://user:password@ipAddress/DB_NAME_HERE"`<br>
<br>

## For Discord Credentials:
Nickname = `Anything You Want` *(Must match ***credentialsNickname*** in config)*

Token = `https://discord.com/developers/`<br>
<br>

## Phue Credentials:
The lights module will only be able to establish and generate credentials if the button on the bridge is pressed prior to running the script via:
`python lights_module.py`<br>

After running a credential file will be created in the user's home directory on their operating system called `.python_hue` this can then be moved into the credentials folder.<br>
<br>

## Credential Usage:

Place json credentials in the `/credentials/` folder.
To load them, run `load_credentials()` from `Credentials_Module` in the `credentials.py` script.

</br>

___

# Praxis Bot Development and Technical Support:

If you want to get in on the action and join the conversations that affect this project's long-term development, create cool modules, or have questions join our discord!

Server Link: [The Curious Nerd Discord Server](https://discord.com/invite/sNTXWn4)

To preview the bot you can check it out on my stream [thecuriousnerd.tv](https://thecuriousnerd.tv) This project is used heavily on my stream and is often worked upon during them.

</br>

___
# Support The Project:

If you wish to support the project, one of the easiest ways to do so is via my patreon or by sending either BTC or Eth

Patreon: https://www.patreon.com/Thecuriousnerd<br>
Bitcoin: `1BFQTkb43bGMSNJjsQtiqai5eQjF5CLcAG`<br>
Ethereum: `0x34DE0330ba2CD4030bBbFE9B46D31DeFeE1ffa54`

</br>

___
