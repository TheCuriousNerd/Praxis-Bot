# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
# Name / Email / Website
# Twitter / Twitch / Youtube

# Authors:
#   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
#       Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd

# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import hashlib
import os

import requests
from gtts import gTTS
from playsound import playsound

from ..bot_functions import utilities_script as utility
import config


def tts(inputText: str, *args):
    outpath = create_speech_file(inputText)
    if utility.isRunningInDocker() == True:
        print("Docker Detected, skipping playsound()")
    else:
        print("Playing Sound...")
        playsound(outpath)


def create_speech_gtts(input_text: str):
    """
    Will create a sound file for the provided text by using gTTS
    :param input_text: any reasonable english text
    :return: returns the path of the file for the sound
    """
    path = os.path.join(get_tts_dir(), create_file_name(input_text, "mp3"))
    if not os.path.exists(path):
        sound_digest = gTTS(text=input_text, lang='en')
        sound_digest.save(path)
    return path


speechCreationFunctions = {  # this is a mapping of the Speaker enum to function pointers
    config.Speaker.GOOGLE_TEXT_TO_SPEECH: create_speech_gtts
}


def create_speech_file(text: str):
    """
    Helper function that will create a sound file for the provided text. This will use the configuration in config.py
    to use TTS engines and name the file
    :param text: the text you would like to turn into a sound file
    :return: returns the path of the sound file
    """
    text_creation_function = speechCreationFunctions.get(config.currentSpeaker)
    output_path = text_creation_function(text)
    return output_path


def create_file_name(text: str, ext: str):
    """
    :param text: the content of the message. using the CONTENT_BASED FileNameStrategy, this will (ostensibly) produce a
    unique file name based on the content of the message. Two messages of equal content will produce the same name
    :param ext: the desired file extension i.e. mp3, ogg, wav, etc...
    :return: returns the formatted filename i.e. 01-01-20_01-01-01_tts.mp3
    """
    if config.fileNameStrategy == config.FileNameStrategy.CONTENT_BASED:
        unique_id = hashlib.md5(bytes(text, 'utf-8')).hexdigest()
        return "%s_tts.%s" % (unique_id, ext)

    elif config.fileNameStrategy == config.FileNameStrategy.TIME_BASED:
        time = datetime.datetime.now()
        return "%s_tts.%s" % (time.strftime("%m-%d-%Y_%H-%M-%S"), ext)

    else:
        return "unconfigured_tts.%s" % ext


def play_speech(fileName):
    destPath = get_tts_dir()
    playsound(destPath + fileName)


def get_tts_dir():
    """
    Checks for the tts directory, and will create it if it does not exist
    :return: the relative file path of the tts dir
    """
    dir = os.path.join(os.getcwd(), "tts")  # this is platform-agnostic
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir


if __name__ == "__main__":
    print("Enter Text: ")
    textInput = str(input())
    tts(textInput)
