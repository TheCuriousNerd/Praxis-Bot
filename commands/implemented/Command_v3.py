# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

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


from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests
from bot_functions.praxis_logging import praxis_logger
import bot_functions.praxis_logging
import os

from commands import loader_functions as function_loader
from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

from bot_functions import utilities_script as utility
from bot_functions import token_processor

import credentials

import pyparsing
import time
from sqlalchemy.engine.cursor import LegacyCursorResult

praxis_logger_obj = praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

class Command_v3(AbstractCommand, AbstractCommandFunction, metaclass=ABCMeta):
    """
    this is the v3 command.
    """
    command = "base_v3"
    helpText = ["This is the v3 command.",
        "\nExample:","base_v3","base_v3 ARGZ"]

    def __init__(self):
        super().__init__(
            Command_v3.command,
            n_args=1,
            command_type=AbstractCommand.CommandType.Ver3
            )
        self.helpText = Command_v3.helpText
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User", userID = "0",  command = "", rest = "", bonusData = None):
        # Command Example:
        # Idea: "!roll $(#0))" = "!roll d20"
        # Command: "!roll"
        # Rest: "$(#0))" = "d20"
        # Example command response: "You rolled $(roll $(#0)))""

        # Look up command in DB and get return strings.
        commandName = command
        v3helper = Abstract_Function_Helpers()
        v3cmd = v3helper.get_command(commandName)
        v3cmd_response = v3helper.get_Command_returnString(commandName)
        #if v3cmd_response is None:
        #    return "not none"
        enoughArgs = self.enoughArgs(rest, v3cmd_response)
        allowedToRun = self.allowedToRun(user, userID, source, v3cmd)
        if allowedToRun == False:
            return "You are not allowed to run this command."
        offCooldown = self.isOffCooldown(v3cmd)
        if offCooldown == False:
            return "This command is on cooldown."

        # Proccess strings
        commandRawInput = commandName + " " + rest # This creates the full command string.
        # Gets rid of the empty space if there are no arguments provided by the user
        if rest is "":
            commandRawInput = commandRawInput [:-1]
        if not enoughArgs:
            return "Not enough arguments for command: %s please try again." % commandName

        tokenWorker = token_processor.Token_Processor()
        #tokenWorker.loadedFunctions = function_loader.load_functions(AbstractCommandFunction.FunctionType.ver0)
        tokenWorker_Results = tokenWorker.parseTokenResponse(user, userID, commandRawInput, v3cmd_response, source)
        self.update_lastUsed(commandName)
        returnString = tokenWorker_Results

        return returnString

    def enoughArgs(self, args, v3cmd_response):
        howManyArgsNeeded = 0
        howManyArgsAvailable = 0
        argRange = range(25)
        for i in argRange:
            if ("$(#%s)" % str(i)) in v3cmd_response:
                howManyArgsNeeded = howManyArgsNeeded + 1

        args = utility.get_args(args)
        for a in args:
            if a is not "":
                howManyArgsAvailable = howManyArgsAvailable + 1

        if howManyArgsAvailable >= howManyArgsNeeded:
            return True
        else:
            return False

    def allowedToRun(self, user:str, userID:str, source:str, v3cmd):
        try:
            if v3cmd is None:
                return False
            else:
                if v3cmd.__getattribute__("is_enabled") == True:
                    if v3cmd.__getattribute__("is_restricted") == True:
                        allowed_services = v3cmd.__getattribute__("allowed_services")
                        allowed_services_list = allowed_services.split(",")
                        allowed_users = v3cmd.__getattribute__("allowed_users")
                        allowed_users_list = allowed_users.split(",")
                        i = 0
                        for s in allowed_services_list:
                            allowed_services_list[i] = allowed_services_list[i].lower()
                            i+=1
                        i = 0
                        for a in allowed_users_list:
                            allowed_users_list[i] = allowed_users_list[i].lower()
                            i+=1
                        is_allowed_to_run = False
                        is_allowed_services_blank = False
                        is_allowed_users_blank = False

                        if (allowed_services == "") or (allowed_services is None):
                            is_allowed_services_blank = True
                        if (allowed_users == "") or (allowed_users is None):
                            is_allowed_users_blank = True

                        if is_allowed_services_blank == True:
                            if user.lower() in allowed_users_list:
                                is_allowed_to_run = True
                        else:
                            if source.lower() in allowed_services_list:
                                if is_allowed_users_blank == True:
                                    is_allowed_to_run = True
                                else:
                                    if user.lower() in allowed_users_list:
                                        is_allowed_to_run = True

                        return is_allowed_to_run

                    else:
                        return True
                else:
                    return False
        except Exception as e:
            praxis_logger.log(praxis_logger,"Error in allowedToRun: %s" % e)
            return False


    # def allowedToRun_old(self, user:str, userID:str, source:str, v3cmd):
    #     try:
    #         if v3cmd is None:
    #             return False
    #         else:
    #             # praxis_logger.log(praxis_logger, "Source Type:")
    #             # praxis_logger.log(praxis_logger, str(type(source)))
    #             if v3cmd.__getattribute__("is_enabled") == True:
    #                 if v3cmd.__getattribute__("is_restricted") == True:
    #                     allowed_services = v3cmd.__getattribute__("allowed_services")
    #                     allowed_services_list = allowed_services.split(",")
    #                     allowed_users = v3cmd.__getattribute__("allowed_users")
    #                     allowed_users_list = allowed_users.split(",")
    #                     i = 0
    #                     for s in allowed_services_list:
    #                         allowed_services_list[i] = allowed_services_list[i].lower()
    #                         i+=1
    #                     i = 0
    #                     for a in allowed_users_list:
    #                         allowed_users_list[i] = allowed_users_list[i].lower()
    #                         i+=1

    #                     if (allowed_services != "") or (allowed_services is not None):
    #                         if source.lower() in allowed_services_list:
    #                             if (allowed_users != "") or (allowed_users is not None):
    #                                 if (user.lower() in allowed_users_list) or (userID.lower() in allowed_users_list):
    #                                     return True
    #                                 else:
    #                                     return False
    #                             else:
    #                                 return True
    #                         else:
    #                             return False
    #                     else:
    #                         if (allowed_users != "") or (allowed_users is not None):
    #                             if (user.lower() in allowed_users_list) or (userID.lower() in allowed_users_list):
    #                                 return True
    #                             else:
    #                                 return False
    #                         else:
    #                             return True
    #                 else:
    #                     return True

    #                     # if source in v3cmd.__getattribute__("allowed_sources"):
    #                     #     if user in v3cmd.__getattribute__("allowed_users"):
    #                     #         return True
    #                     #     else:
    #                     #         if v3cmd.__getattribute__("allowed_users") == "":
    #                     #             return True

    #                     #     if userID in v3cmd.__getattribute__("allowed_users"):
    #                     #         return True
    #                     #     else:
    #                     #         if v3cmd.__getattribute__("allowed_users") == "":
    #                     #             return True
    #                     #     return False
    #                     # else:
    #                     #     if v3cmd.__getattribute__("allowed_sources") == "":
    #                     #         return True
    #                     #     return False

    #                 # else:
    #                 #     return True
    #             elif v3cmd.__getattribute__("is_enabled") == False:
    #                 return False
    #     except Exception as e:
    #         praxis_logger.log(praxis_logger,"Error in allowedToRun: %s" % e)
    #         return False


    def isOffCooldown(self, v3cmd):
        lastUsed = v3cmd.__getattribute__("last_used")
        coolDownLength = v3cmd.__getattribute__("cooldown_length")
        curTime = int(time.time())
        if curTime - lastUsed > coolDownLength:
            return True
        else:
            return False

    def update_lastUsed(self, commandName):
        helper = Abstract_Function_Helpers()
        helper.update_lastUsed(commandName)
        return None


    def get_help(self):
        return self.helpText

    def do_function():
        return None