
from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction, Function_Helpers

from bot_functions import utilities_script as utility
from bot_functions import token_processor

import pyparsing

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

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):
        # Command Example:
        # Idea: "!roll #(0)" = "!roll d20"
        # command = "!roll"
        # rest = " #(0)" = " d20"

        # Look up command in DB and get return strings.
        command_returnString = Function_Helpers.get_Command_returnString(command)


        # Proccess strings
        commandRawInput = command + " " + rest # This creates the full command string.


        tokenWorker = token_processor.Token_Processor()
        tokenWorker.loadedFunctions = self.loadedFunctions
        tokenWorker_Results = tokenWorker.parseTokenResponse(user, commandRawInput, command_returnString)
        returnString = tokenWorker_Results

        return returnString


    def get_help(self):
        return self.helpText

    def do_function():
        return None