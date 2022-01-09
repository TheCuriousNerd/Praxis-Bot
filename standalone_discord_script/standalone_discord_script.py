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

import abc
from operator import isub
import random
import re
import time

from discord import client
from discord.activity import Game
from discord.types.snowflake import Snowflake
from discord.voice_client import VoiceClient
import bot_functions.utilities_script as utility
import bot_functions.utilities_db
from json import loads
from urllib.parse import urlencode

from json import dump, loads

import requests

from discord import message
from discord.client import Client
import asyncio

from bot_functions import tts

import config

from commands import command_base
from commands import loader as command_loader
from commands.command_base import AbstractCommand

import credentials

import discord
import discord.message
import discord.channel
import discord.abc

from bot_functions.cooldowns import Cooldown_Module

import youtube_dl

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))


# api = flask.Flask(__name__)

# @api.route('/', methods=['GET'])
# def Discord_Script_Status():
#     return flask.make_response('BOO', 200)




youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)





class Discord_Module(discord.Client):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.discordCredential: credentials.Discord_Credential

        self.cooldownModule:Cooldown_Module = Cooldown_Module()
        self.cooldownModule.setupCooldown("discordRateLimit", 10, 1)

        # don't freak out, this is *merely* a regex for matching urls that will hit just about everything
        self._urlMatcher = re.compile(
            "(https?:(/{1,3}|[a-z0-9%])|[a-z0-9.-]+[.](com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw))")
        self.guild = discord.Object(id=197565046916775945)
        self.commands = [
            discord.ApplicationCommand(
                name="math",
                description="Solves your math problem.",
                options=[discord.ApplicationCommandOption(
                    name="equation",
                    description="The equation you want to solve.",
                    type=discord.ApplicationCommandOptionType.string,
                    )],
                ),
            discord.ApplicationCommand(
                name="test",
                description="Does a variety of tests.",
                options=[discord.ApplicationCommandOption(
                    name="input",
                    description="The input data.",
                    type=discord.ApplicationCommandOptionType.string,
                    required=False
                    )],
                ),
        ]
        self.VC_Channel:discord.channel.VoiceChannel = None
        self.voiceClient = None
        self.voice_isQueueEnabled = True
        self.voice_isQueueLooping = False
        self.voice_isQueueRepeating = False
        self.voice_isQueueShuffle = False
        self.voiceQueue = []

        self.DB = bot_functions.utilities_db.Praxis_DB_Connection()
        self.tasks = []


    def main(self):
        self.loop.create_task(self.task_lookup_Loop())
        self.loop.create_task(self.startup())
        self.loop.run_forever()

    async def startup(self):
            await self.login(self.discordCredential.token)
            #await self.register_application_commands(None)
            await self.setupCommands()
            await self.register_application_commands(self.commands)
            await self.connect()

    # async def startup(self):
    #     await self.start(self.discordCredential.token)

    # def main(self):
    #     print("starting loop")
    #     self.loop.create_task(self.startup())
    #     self.loop.run_forever()

    #async def api_startup(self):
    #    api.run(host='0.0.0.0', port=42048)

    async def setupCommands(self):
        defaultOptions=[discord.ApplicationCommandOption(
                        name="input",
                        description="Command input data.",
                        type=discord.ApplicationCommandOptionType.string,
                        required=False
                        )]
        commandsToAdd = [
            {"name": "raidtime", "description": "Moves the raiders to the raid channel.", "options": []},
            {"name": "endraid", "description": "Moves the raiders to the raid channel.", "options": defaultOptions},
            {"name":"play", "description":"Plays TTS audio in voice channel.", "options":defaultOptions},
            {"name":"playnext", "description":"Adds audio to the next slot in the queue.", "options":defaultOptions},
            {"name":"stop", "description":"Stops audio being played in the voice channel.", "options":[]},
            {"name":"pause", "description":"Pauses audio being playing in the voice channel.", "options":[]},
            {"name":"resume", "description":"Resumes audio being playing in the voice channel.", "options":[]},
            #{"name":"skip", "description":"Skips audio being played to the next audio in the queue in the voice channel.", "options":[]},
            {"name":"clear", "description":"Clears the queue.", "options":[]},
            {"name":"volume", "description":"Changes the volume.", "options":defaultOptions},
            #{"name":"loop", "description":"Enables/Disables the looping of the queue.", "options":defaultOptions},
            #{"name":"repeat", "description":"Enables/Disables the repeat of an audio.", "options":defaultOptions},
            #{"name":"shuffle", "description":"Shuffles the queue.", "options":defaultOptions},
            {"name":"join", "description":"Joins a voice channel.", "options":defaultOptions},
            {"name":"leave", "description":"Leaves the voice channel.", "options":[]},
        ]
        for command_ in commandsToAdd:
            newCommand = discord.ApplicationCommand(
                    name=command_["name"],
                    description=command_["description"],
                    options=command_["options"],
                    )
            self.commands.append(newCommand)

    async def task_lookup_Loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            #praxis_logger_obj.log(" -Discord: task_lookup_Loop()")
            await self.getTasks()
            #await self.send_message_to_channel(835319293981622302, "Inner Loop Tick")
            await self.task_Loop()
            await asyncio.sleep(0.1)

    async def getTasks(self):
        self.DB.startConnection()
        newTasks = self.DB.getTasksFromQueue("standalone_discord")
        if newTasks is not None:
            for task in newTasks:
                #await self.send_message_to_channel(835319293981622302, "New Task: " + str(task))
                try:
                    await self.deleteTaskFromDB(task)
                except Exception as e:
                    praxis_logger_obj.log("Error deleting task from DB: " + str(e))
            #Add new tasks to the queue
            for task in newTasks:
                try:
                    await self.send_message_to_channel(835319293981622302, "New Task: " + str(task) + " Task Type: " + str(type(task)))
                    taskToAdd = []
                    for item_ in task:
                        taskToAdd.append(item_)
                    taskToAdd[5] = loads(taskToAdd[5])

                    await self.addTask(taskToAdd)
                except Exception as e:
                    praxis_logger_obj.log("Error adding task to queue: " + str(e))

    async def addTask(self, task):
        self.tasks.append(task)

    async def task_Loop(self):
        #await self.send_message_to_channel(835319293981622302, "Inner Loop")
        if self.tasks is not None:
            #await self.send_message_to_channel(835319293981622302, "Inner Loop is not None")
            for task in self.tasks:
                try:
                    #await self.send_message_to_channel(835319293981622302, "Inner Loop Task Loop: " + str(task))
                    curTask = task
                    self.tasks.remove(task)
                    await self.task_handler(task)
                except:
                    pass

        if self.voiceClient is not None:
            if self.voiceClient.is_connected():
                if self.voiceClient.is_playing() == False or self.voiceClient.is_paused() == True:
                    if len(self.voiceQueue) != 0:
                        if self.voice_isQueueLooping == True:
                            await self.play_voice_task_handler(self.voiceQueue[0])
                            self.voiceQueue.append(self.voiceQueue.pop(0))
                        else:
                            await self.play_voice_task_handler(self.voiceQueue[0])
                            self.voiceQueue.pop(0)

    async def task_handler(self, task):
        if task[2] == "voice":
            await self.voice_task_handler(task)
        elif task[2] == "text":
            await self.text_task_handler(task)
        elif task[2] == "user":
            await self.user_task_handler(task)
        else:
            await self.unknown_task_handler(task)

    async def voice_task_handler(self, task):
        if task[4] == "play":
            await self.play_voice_task_handler(task)
        if task[4] == "playNext":
            await self.playNext_voice_task_handler(task)
        elif task[4] == "stop":
            await self.stop_voice_task_handler(task)
        elif task[4] == "pause":
            await self.pause_voice_task_handler(task)
        elif task[4] == "resume":
            await self.resume_voice_task_handler(task)
        elif task[4] == "skip":
            await self.skip_voice_task_handler(task)
        elif task[4] == "queue":
            await self.queue_voice_task_handler(task)
        elif task[4] == "remove":
            await self.remove_voice_task_handler(task)
        elif task[4] == "clear":
            await self.clear_voice_task_handler(task)
        elif task[4] == "volume":
            await self.volume_voice_task_handler(task)
        elif task[4] == "loop":
            await self.loop_voice_task_handler(task)
        elif task[4] == "repeat":
            await self.repeat_voice_task_handler(task)
        elif task[4] == "shuffle":
            await self.shuffle_voice_task_handler(task)
        elif task[4] == "tts":
            await self.tts_voice_task_handler(task)
        elif task[4] == "join":
            await self.join_voice_task_handler(task)
        elif task[4] == "leave":
            await self.leave_voice_task_handler(task)
        else:
            await self.unknown_task_handler(task)


    async def prepTrack(self, task):
        preppedTrack:dict = task[5]
        if preppedTrack["type"] == "file":
            return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(preppedTrack["text"]))
        elif preppedTrack["type"] == "url":
            return await YTDLSource.from_url(preppedTrack["text"], loop=self.loop)
        elif preppedTrack["type"] == "tts":
            #generate TTS audio to then play
            filePath = tts.create_speech_file(preppedTrack["text"])[8:] # Removes "/praxis/" from the path
            return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filePath))
        else:
            return None

    async def play_voice_task_handler(self, task):
        #await self.send_message_to_channel(835319293981622302, "Voice Task")
        if self.voiceClient is None or self.voiceClient.is_connected() is False:
            #await self.send_message_to_channel(835319293981622302, "VC is none?")
            guildData:discord.Guild = self.get_guild(self.guild.id)
            memberData = await guildData.fetch_member(int(task[6]))
            self.VC_Channel = memberData.voice.channel
            #await self.send_message_to_channel(835319293981622302, "VC ID: " + str(self.VC_Channel.id))
            voiceClientID = self.get_channel(self.VC_Channel.id)
            #self.voiceClient:discord.VoiceClient = await self.VC_Channel.connect(self.VC_Channel.id)
            joinTask = [None, "standalone_discord", "voice", str(time.time()), "join", voiceClientID, task[6]]
            await self.join_voice_task_handler(joinTask)

        # Checks if queue is enabled and empty, if so, it will add the audio source to the queue and then start playing it.
        #if self.voice_isQueueEnabled and self.voiceQueue == []:
        newTrack = await self.prepTrack(task)
        #self.voiceQueue.append(newTrack)

        # If the newTrack is not reinstanstiated, then the subsequent audio added to the queue will not be played.
        #newTrack = await self.prepTrack(task)
        #self.voiceQueue.append(newTrack)
        #newTrack = await self.prepTrack(task)
        #self.voiceQueue.append(newTrack)

        await self.send_message_to_channel(835319293981622302, "Appended Track to Queue: " + str(newTrack))


        if self.voiceClient.is_connected():
            if self.voiceClient.is_playing():
                #self.voiceClient.stop()
                #source = newTrack
                self.voiceQueue.append(newTrack)
                #await self.send_message_to_channel(835319293981622302, "Playing new Source: " + str(source))
                #self.voiceClient.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                #while self.voiceClient.is_playing():
                #    pass
                #await self.nextTrack()
            else:
                self.voiceQueue.append(newTrack)
                source = self.voiceQueue.pop(0)
                #await self.send_message_to_channel(835319293981622302, "Player: " + str(source))
                self.voiceClient.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                #while self.voiceClient.is_playing():
                #    pass
                #await self.nextTrack()
        else:
            try:
                await self.voiceClient.connect(self.VC_Channel)
            except:
                guildData:discord.Guild = self.get_guild(self.guild.id)
                memberData = await guildData.fetch_member(int(task[6]))
                self.VC_Channel = memberData.voice.channel
                await self.voiceClient.connect(self.VC_Channel)
            source = self.voiceQueue.pop(0)
            self.voiceClient.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

    async def nextTrack(self):
        #praxis_logger_obj.log("Voice Task - Next Track")
        if self.voiceClient is None:
            pass
        else:
            #await self.send_message_to_channel(835319293981622302, "Voice Task - Next Track")
            if self.voice_isQueueLooping or self.voice_isQueueRepeating:
                self.voiceQueue.insert(0, self.voiceQueue[0])
            if self.voice_isQueueShuffle:
                random.shuffle(self.voiceQueue)
            if self.voiceQueue != []:
                if self.voiceClient.is_playing():
                    self.voiceClient.stop()
                source = self.voiceQueue.pop(0)
                #await self.send_message_to_channel(835319293981622302, "Player: " + str(source))
                self.voiceClient.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                while self.voiceClient.is_playing():
                    pass
                await self.nextTrack()

    async def playNext_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            #appends the next track to the front of the queue
            newTrack = await self.prepTrack(task)
            self.voiceQueue.append(newTrack)

    async def stop_voice_task_handler(self, task):
        if self.voiceClient.is_connected():
            if self.voiceClient.is_playing():
                self.voiceClient.stop()

    async def pause_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            self.voiceClient.pause()

    async def resume_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            self.voiceClient.resume()

    async def skip_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            await self.nextTrack()

    async def queue_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            # This returns the current queue into the chat.
            # MAKE THIS LATER
            pass

    async def remove_voice_task_handler(self, task):
        # This removes the current track from the queue.
        # MAKE THIS LATER
        pass


    async def clear_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            self.voiceClient.stop()
            self.voiceQueue = []

    async def volume_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            self.voiceClient.source.volume = float(task[5]) / 100

    async def loop_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            value:str = task[5]
            self.voice_isQueueLooping = (value.lower() == "true")

    async def repeat_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            value:str = task[5]
            self.voice_isQueueRepeating = (value.lower() == "true")

    async def shuffle_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            value:str = task[5]
            self.voice_isQueueShuffle = (value.lower() == "true")

    async def tts_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            # This will be a TTS function.
            # MAKE THIS LATER
            data = loads(task[5])
            textToSpeak = data["text"]
            pass

    async def join_voice_task_handler_OLD(self, task):
        if self.voiceClient is None:
            try:
                self.VC_Channel = self.get_channel(int(task[5]))
            except:
                guildData:discord.Guild = self.get_guild(self.guild.id)
                memberData = await guildData.fetch_member(int(task[6]))
                self.VC_Channel = memberData.voice.channel
            self.voiceClient = await self.VC_Channel.connect(self.VC_Channel)
        else:
            curChannelID = self.VC_Channel.id
            try:
                newChannelID = int(task[5])
            except:
                guildData:discord.Guild = self.get_guild(self.guild.id)
                memberData = await guildData.fetch_member(int(task[6]))
                newChannelID = memberData.voice.channel.id

            if self.voiceClient.is_connected():
                await self.voiceClient.disconnect()
            if curChannelID != newChannelID:
                self.VC_Channel = self.get_channel(newChannelID)
                self.voiceClient = await self.VC_Channel.connect(self.VC_Channel)

    async def join_voice_task_handler(self, task):
        #await self.send_message_to_channel(835319293981622302, "Joining...")
        if self.voiceClient is None:
            try:
                self.VC_Channel:discord.channel.VoiceChannel = self.get_channel(int(task[5]))
                self.voiceClient = await self.VC_Channel.connect()
            except:
                guildData:discord.Guild = self.get_guild(self.guild.id)
                memberData = await guildData.fetch_member(int(task[6]))
                self.VC_Channel = self.get_channel(memberData.voice.channel.id)
                self.voiceClient = await self.VC_Channel.connect()
        else:
            await self.voiceClient.disconnect()
            self.voiceClient = None
            await self.join_voice_task_handler(task)
            #await self.send_message_to_channel(835319293981622302, "vs is not none")
        #await self.send_message_to_channel(835319293981622302, "Finished joining")

    async def leave_voice_task_handler(self, task):
        if self.voiceClient is None:
            pass
        else:
            await self.voiceClient.disconnect()


    async def text_task_handler(self, task):
        if task[4] == "message":
            await self.send_message_task_handler(task)
        elif task[4] == "embed":
            await self.send_embed_task_handler(task)
        else:
            await self.unknown_task_handler(task)

    async def send_message_task_handler(self, task):
        if task[5] == "channel":
            pass
            # Sends Message to Channel
        elif task[5] == "user":
            pass
            # Sends Message to User
        else:
            await self.unknown_task_handler(task)

    async def send_embed_task_handler(self, task):
        if task[5] == "channel":
            pass
            # Sends Message to Channel
        elif task[5] == "user":
            pass
            # Sends Message to User
        else:
            await self.unknown_task_handler(task)





    async def user_task_handler(self, task):
        if task[4] == "name":
            name = await self.get_user(int(task[5])).name
            self.DB.add_taskToQueue("standalone_function", "response", time.time(), "discordName", task[5], name)
        else:
            await self.unknown_task_handler(task)





    async def deleteTaskFromDB(self, task):
        self.DB.deleteItems("task_queue_v0", "id", task[0])

    async def unknown_task_handler(self, task):
        return False

    async def on_ready(self):
        print('Logged on as', self.user)




    async def on_slash_command(self, interaction: discord.Interaction):
        praxis_logger_obj.log("\n -Slash Command: " + str(interaction.command_name))
        if interaction:
            cmdName = interaction.command_name
            author:discord.member.Member = interaction.user
            msg = interaction.data
            msgChannel = interaction.channel
            try:
                inputData = msg["options"][0]["value"]
            except:
                inputData = ""
            #await interaction.response.send_message("%s called %s | %s || FROM %s" % (author.name, cmdName, inputData, msgChannel.name))
            if cmdName == "test":
                await interaction.response.send_message("%s called %s FROM %s\nECHO: %s" % (author.name, cmdName, msgChannel.name, inputData))
            if inputData == "123":
                await self.voiceTest()
            elif inputData == "abc":
                await self.move_user_to_voice_channel(interaction.user.id, 663970225821188096)

            if cmdName == "raidtime":
                raidTeamIDs = config.raidTeamIDs
                if author.id in raidTeamIDs:
                    await self.move_users_to_voice_channel(raidTeamIDs, 741473571141976096)
                    await interaction.response.send_message("%s moved the Raid Team from %s" % (author.name, msgChannel.name))
                else:
                    await interaction.response.send_message("%s cannot call this command." % (author.name))

            if cmdName == "endraid":
                if inputData == "":
                    inputData = 812662889008594944
                raidTeamIDs = config.raidTeamIDs
                if author.id in raidTeamIDs:
                    await self.move_users_to_voice_channel(raidTeamIDs, inputData)
                    await interaction.response.send_message("%s moved the Raid Team from %s" % (author.name, msgChannel.name))
                else:
                    await interaction.response.send_message("%s cannot call this command." % (author.name))

            DefaultCommands = ["join", "leave", "play", "pause", "stop", "resume", "skip", "clear", "volume", "loop", "repeat", "shuffle"]
            for command in DefaultCommands:
                if cmdName == command:
                    #await self.send_message_to_channel(835319293981622302, "About to run handler")
                    resturnString = await self.default_slash_command_handler(interaction, author, msgChannel, command, inputData)
                    await interaction.response.send_message(resturnString)
            slashV3Commands = ["math"]
            for command in slashV3Commands:
                if cmdName == command:
                    #await self.send_message_to_channel(835319293981622302, "About to run math handler")
                    await self.v3_slash_command_handler("!"+cmdName, inputData, msgChannel.id, author, interaction)

            #response = ""
            #await interaction.response.send_message(response)
            #await interaction.response.send_message("%s called %s | %s || FROM %s" % (author.name, cmdName, inputData, msgChannel.name))
            #await self.send_message_to_channel(835319293981622302, str(utility.get_dir("tts")))
        else:
            await interaction.response.send_message("You called a slash command")

    async def v3_slash_command_handler(self, command, rest, targetChannel, author, interaction):
        try:
            #await self.send_message_to_channel(835319293981622302, "Trying to run math handler")
            is_actionable = await self.is_command(command)
            #await self.send_message_to_channel(835319293981622302, "Is actionable: " + str(is_actionable))
            if is_actionable:
                if self.cooldownModule.isCooldownActive("discordRateLimit") == False:
                    ##await self.send_message_to_channel(835319293981622302, "Not on cooldown")
                    await self.exec_command(None, command, rest, targetChannel, author, interaction)
                    ##await self.send_message_to_channel(835319293981622302, "Executed command")
        except:
            await self.send_message_to_channel(835319293981622302, "something went wrong with a command")
            print("something went wrong with a command")

    async def default_slash_command_handler(self, interaction, author:discord.member.Member, msgChannel, command, inputData):
        reponseText = ""
        if command == "join":
            #await self.send_message_to_channel(835319293981622302, "Join detected")
            task = [None, "standalone_discord", "voice", str(time.time()), "join", inputData, author.id]
            #await self.send_message_to_channel(835319293981622302, str(task))
            await self.addTask(task)
            #await self.join_voice_task_handler(task)
            reponseText = "Joining Voice Channel"
        elif command == "leave":
            await self.leave_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "leave", "", ""])
            #await self.addTask([None, "standalone_discord", "voice", str(time.time()), "leave", "", ""])
            reponseText = "Leaving Voice Channel"
        elif command == "play":
            if await self.isUserAllowed(author.id):
                #await self.send_message_to_channel(835319293981622302, "Good User")
                inputArgs = "".join(inputData)
                newAudio = {}
                #await self.send_message_to_channel(835319293981622302, inputArgs)
                # Determine if inputArgs is either a url, a file, or a string
                #if utility.contains_url(inputArgs):
                #    # inputArgs is a url
                #    newAudio["type"] = "url"
                if utility.contains_pattern(inputArgs, ".*\.(mp3|pcm|wav|aiff|aac|ogg|wma|flac|alac)$"):
                    # inputArgs is a file
                    newAudio["type"] = "file"
                    #await self.send_message_to_channel(835319293981622302, "Detected File")
                else:
                    # inputArgs is a string
                    newAudio["type"] = "tts"
                newAudio["text"] = inputArgs
                preppedAudio = newAudio
                #await self.send_message_to_channel(835319293981622302, "Playing Audio: " + str(newAudio["text"]))
                #await self.play_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "play", preppedAudio, author.id])
                await self.addTask([None, "standalone_discord", "voice", str(time.time()), "play", preppedAudio, author.id])
            reponseText = "Playing Audio"
        elif command == "pause":
            await self.pause_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "pause", "", ""])
            reponseText = "Paused Audio"
        elif command == "resume":
            await self.resume_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "resume", "", ""])
            reponseText = "Resumed Audio"
        elif command == "stop":
            await self.stop_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "stop", "", ""])
            reponseText = "Stopped Audio"
        elif command == "skip":
            await self.skip_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "skip", "", ""])
            reponseText = "Skipped Audio"
        elif command == "clear":
            await self.clear_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "clear", "", ""])
            reponseText = "Cleared Audio Queue"
        elif command == "volume":
            await self.volume_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "volume", inputData, ""])
            reponseText = "Set Volume to " + str(inputData)
        elif command == "loop":
            await self.loop_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "loop", inputData, ""])
            reponseText = "Set Loop to " + str(inputData)
        elif command == "repeat":
            await self.repeat_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "repeat", inputData, ""])
            reponseText = "Set Repeat to " + str(inputData)
        elif command == "shuffle":
            await self.shuffle_voice_task_handler([None, "standalone_discord", "voice", str(time.time()), "shuffle", inputData, ""])
            reponseText = "Set Shuffle to " + str(inputData)

        await interaction.response.send_message(reponseText)

    async def isUserAllowed(self, userID):
        goodIDs = [76078763984551936, 276588812539527168]
        if userID in goodIDs:
            return True
        else:
            return False

    async def voiceTest(self, filename: str = "68e2183965ed238c82d138030b82986f_tts"):
        praxis_logger_obj.log("\n -Voice Test")
        self.VC_Channel:discord.channel.VoiceChannel = self.get_channel(663970225821188096)
        praxis_logger_obj.log("About to Connect")
        self.voiceClient:discord.VoiceClient = await self.VC_Channel.connect()
        audioFile = utility.get_dir("tts") + "/%s.mp3" % filename
        player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audioFile))
        self.voiceClient.play(player)
        #praxis_logger_obj.log("\n -Voice Channel: " + str(self.VC_Channel))
        #praxis_logger_obj.log("\n -Voice Channel Type: " + str(type(self.VC_Channel)))

        #await self.VC.move_to(self.VC_Channel)
        #await self.VC_Channel
        waitBool = True
        while waitBool:
            if self.voiceClient.is_playing():
                await asyncio.sleep(1)
            else:
                waitBool = False
        await self.voiceClient.disconnect()


    async def move_user_to_voice_channel(self, memberData, newChannelID):
        await memberData.move_to(self.get_channel(newChannelID))


    async def move_users_to_voice_channel(self, userIDs, newChannelID):

        guildData:discord.Guild = self.get_guild(self.guild.id)
        for userID in userIDs:
            memberData = await guildData.fetch_member(userID)
            await self.move_user_to_voice_channel(memberData, newChannelID)






    async def on_connect(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game("Exploring the internet"))

    async def on_message(self, message: discord.Message):
        print("{" + message.guild.name + "}[ " + str(message.channel) + " ](" + message.author.display_name + ")> ")
        #print(message.author.mention)
        print(message.content)

        debugLogString= "\n\n{" + message.guild.name + "}[ " + str(message.channel) + " ](" + message.author.display_name +")> " + message.content + "\n"
        praxis_logger_obj.log(debugLogString)

        if not await self.isSenderBot(message):
            # This will check for the Praxis-Bot-tts channel and will TTS stuff from there.
            #await self.eval_triggeredEvents(message)
            command, rest = utility.parse_line(message.content)
            if command == "-tts":
                await self.addTask([None, "standalone_discord", "voice", str(time.time()), "play", {"type":"tts","text":rest}, message.author.id])

            await self.eval_commands(message)
            await self.eval_tts(message)


    async def eval_triggeredEvents(self, message: discord.Message):
        # This will check for the selected channels and will TTS stuff from there.
        #await self.tts_message(message)
        foundChannel = False

        for channel in self.selected_ttsChannels:
            if channel == message.channel.id:
                # await self.tts_message(message)
                pass

    async def eval_tts(self, message: discord.Message):
        command, rest = utility.parse_line(message.content)
        try:
            is_actionable = await self.is_command(command)
            if not is_actionable:
                await self.exec_tts(message)
        except:
                    print("something went wrong with tts")

    async def eval_commands(self, message: discord.Message):
        command, rest = utility.parse_line(message.content)
        try:
            is_actionable = await self.is_command(command)
            if is_actionable:
                if self.cooldownModule.isCooldownActive("discordRateLimit") == False:
                    await self.exec_command(message, command, rest)
        except:
                    print("something went wrong with a command")

    async def is_command(self, word: str) -> bool:
        # todo need to url-escape word
        clean_param = urlencode({'name': word})
        url = "http://standalone_command:42010/api/v1/command?%s" % clean_param
        resp = requests.get(url)
        return resp.status_code == 200

    async def exec_command(self, realMessage: discord.Message, command: str, rest: str, returnStringChannelID:int = 0, user = None, interaction = None):
        # todo need to url-escape command and rest
        if user != None:
            author_name = str(user.name)
            author_id = str(user.id)
        else:
            author_name = str(realMessage.author.name)
            author_id = str(realMessage.author.id)
        params = urlencode(
            {'command_source': command_base.AbstractCommand.CommandSource.Discord,
            'user_name': author_name,
            'user_id': author_id,
            'command_name': command,
            'rest': rest,
            'bonus_data': realMessage})

        url = "http://standalone_command:42010/api/v1/exec_command?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None and interaction is None:
                #await self.send_message(realMessage, msg)
                if returnStringChannelID == 0:
                    await self.send_message_to_channel(realMessage.channel.id, msg)
                else:
                    await self.send_message_to_channel(returnStringChannelID, msg)
            if interaction != None:
                await interaction.response.send_message(msg)
        else:
            # todo handle failed requests
            pass

    async def send_message(self, message: discord.Message, response):
        isBlocked = await self.isChannel_inConfigList(str(message.channel.id), config.block_DiscordChannelsMessaging)
        if self.cooldownModule.isCooldownActive("discordRateLimit") == False and not isBlocked and not config.blockAll_DiscordChannelsMessaging:
            if not utility.contains_slur(response):
                await message.channel.send(message.channel.id)

                self.cooldownModule.actionTrigger("discordRateLimit")

    async def send_message_to_channel(self, channel, message):
        isBlocked = await self.isChannel_inConfigList(str(channel), config.block_DiscordChannelsMessaging)
        if self.cooldownModule.isCooldownActive("discordRateLimit") == False and not isBlocked and not config.blockAll_DiscordChannelsMessaging:
            if not utility.contains_slur(message):
                destChannel = self.get_channel(channel)
                await destChannel.send(message)

                self.cooldownModule.actionTrigger("discordRateLimit")


    # Checks if Sender is bot.
    async def isSenderBot(self, message: discord.Message):
        isBot = False
        for bot in config.botList:
            if message.author.display_name.lower() == bot.lower():
                isBot = True
                print("<{ bot detected! }> ")
        return isBot

    async def isChannel_inConfigList(self, selectedChannel, selectedList):
        #print(channel)
        #print(selectedList)
        is_Self = False
        for discordChannel in selectedList:
            #print("isSelf: " + str(discordChannel) + " vs " + str(selectedChannel))
            if discordChannel == selectedChannel:
                is_Self = True

        return is_Self

    async def exec_tts(self, message: discord.Message):
        isBlocked = await self.isChannel_inConfigList(str(message.channel.id), config.block_DiscordChannelsTTS)
        isForced = (await self.isChannel_inConfigList(str(message.channel.id), config.force_DiscordChannelsTTS) and not config.blockAll_DiscordChannelsTTS)
        #print("isBlocked: " + str(isBlocked))
        #print("isForced: " + str(isForced))

        print(message.channel.id, message.channel.id, message.channel.id)
        isMessageChannelInList = False
        for TTS_C_id in config.selected_DiscordTTSChannels:
            print(TTS_C_id)
            if int(TTS_C_id) == int(message.channel.id):
                isMessageChannelInList = True
        if config.autoEnabled_DiscordChannelsTTS and (isMessageChannelInList) and not isBlocked and not config.blockAll_DiscordChannelsTTS or isForced or config.forceAll_DiscordChatChannelsTTS:
            if not message.content.startswith('!'):
                text_to_say: str = "%s says, %s" % (message.author.display_name, message.content)
                channel_text = "%s user msg" % message.channel

                await self.exec_tts_sender("", text_to_say)

    async def exec_tts_sender(self, username, message):
        params = urlencode({'tts_sender': username, 'tts_text': message})
        #standalone_tts_core
        url = "http://standalone_tts_core:42064/api/v1/tts/send_text?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            pass


        if not await self.contains_slur(message):
            if self.tts_enabled:
                if not message.content.startswith('!'):
                    pass
                    #text_to_say: str = "%s says, %s" % (message.author.display_name, message.content)
                    #channel_text = "%s user msg" % message.channel

                    #tts.tts(text_to_say)

    #FINISH THIS EVENT LOG
    async def send_EventLog(self, eventName, eventTime, eventType, eventData):
        params = urlencode(
            {'event_name': eventName,
            'event_time': eventTime,
            'event_type': eventType,
            'event_data': eventData})
        url = "http://standalone_eventlog:42008/api/v1/event_log/add_event?%s" % params
        resp = requests.get(url)

        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            pass




if __name__ == "__main__":
    testModule = Discord_Module()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()
    testModule.discordCredential = credentials_manager.find_Discord_Credential(config.credentialsNickname)

    testModule.main()