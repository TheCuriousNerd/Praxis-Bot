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
import random
import re

from discord import client
from discord.types.snowflake import Snowflake
from discord.voice_client import VoiceClient
import bot_functions.utilities_script as utility
from json import loads
from urllib.parse import urlencode

import requests

from discord import message
from discord.client import Client
import asyncio

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

import os
import bot_functions.praxis_logging as praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

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
                description="Solves your math problem."),
        ]

    async def startup(self):
        await self.start(self.discordCredential.token)

    def main(self):
        print("starting loop")
        self.loop.create_task(self.startup())
        self.loop.run_forever()

    async def on_ready(self):
        print('Logged on as', self.user)

    def newMain(self):
        self.loop.create_task(self.newStartup())
        self.loop.run_forever()

    async def newStartup(self):
            await self.login(self.discordCredential.token)
            #await self.register_application_commands(None)
            #await self.register_application_commands(self.commands)
            await self.connect()

    async def on_slash_command(self, interaction: discord.Interaction):
        praxis_logger_obj.log("\n -Slash Command: " + str(interaction.command_name))
        if interaction:
            cmdName = interaction.command_name
            await interaction.response.send_message("You called %s" % cmdName)
            await self.voiceTest()
            await self.send_message_to_channel(835319293981622302, "slash command extra")
        else:
            await interaction.response.send_message("You called a slash command")


    async def voiceTest(self):
        praxis_logger_obj.log("\n -Voice Test")
        self.VC_Channel:discord.channel.VoiceChannel = self.get_channel(812662889008594944)
        praxis_logger_obj.log("About to Connect")
        await self.VC_Channel.connect()
        #praxis_logger_obj.log("\n -Voice Channel: " + str(self.VC_Channel))
        #praxis_logger_obj.log("\n -Voice Channel Type: " + str(type(self.VC_Channel)))

        #await self.VC.move_to(self.VC_Channel)
        #await self.VC_Channel



    async def on_message(self, message: discord.Message):
        print("{" + message.guild.name + "}[ " + str(message.channel) + " ](" + message.author.display_name + ")> ")
        #print(message.author.mention)
        print(message.content)

        debugLogString= "\n\n{" + message.guild.name + "}[ " + str(message.channel) + " ](" + message.author.display_name +")> " + message.content + "\n"
        praxis_logger_obj.log(debugLogString)

        if not await self.isSenderBot(message):
            # This will check for the Praxis-Bot-tts channel and will TTS stuff from there.
            #await self.eval_triggeredEvents(message)

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

    async def exec_command(self, realMessage: discord.Message, command: str, rest: str):
        # todo need to url-escape command and rest
        params = urlencode(
            {'command_source': command_base.AbstractCommand.CommandSource.Discord,
            'user_name': realMessage.author.mention,
            'command_name': command,
            'rest': rest,
            'bonus_data': realMessage})

        url = "http://standalone_command:42010/api/v1/exec_command?%s" % params
        resp = requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = loads(resp.text)
            msg = data['message']
            if msg is not None:
                #await self.send_message(realMessage, msg)
                await self.send_message_to_channel(realMessage.channel.id, msg)
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

    testModule.newMain()