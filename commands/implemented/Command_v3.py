
from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from bot_functions import utilities_script as utility

import pyparsing


class Command_v3(AbstractCommand, AbstractCommandFunction, metaclass=ABCMeta):
    """
    this is the v3 command.
    """
    command = "testerino_v3"
    helpText = ["This is a v3 command.",
        "\nExample:","testerino_v3"]

    def __init__(self):
        super().__init__(
            Command_v3.command,
            n_args=1,
            command_type=AbstractCommand.CommandType.Ver3
            )
        self.helpText = Command_v3.helpText
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):

        # Look up command in DB and get return strings.

        # Proccess string and run functions
        fullCommand = command + " " + rest # This creates the full command string.
        functionsList = self.searchForFunctions(fullCommand) # Generates a list of functions to run in a specific order. Inner to Outer Most
        for function in functionsList:
            if function[2] == True:
                pass
            else:
                self.run_function(user, function, fullCommand)

        returnString = user + " sent: [ " + command + " ] with: " + rest
        #print(returnString)


        return returnString

    def searchForFunctions(self, input):
        parserContent = pyparsing.Word(pyparsing.alphanums)
        parser = pyparsing.nestedExpr('(', ')', content=parserContent)
        testResult_ = parser.parseString(input)
        testResult = testResult_.asList()

        #result1 = ("functionName", input, False)
        #result2 = ("functionName2", ("functionName3", input, False, None), True)
        #results = []
        return testResult

    def run_function(self, user, function, input):
        function_:AbstractCommandFunction = self.loadedFunctions[function]
        if function_ is not None:
            function_response = function_.do_function(user, input)

    def get_help(self):
        return self.helpText
