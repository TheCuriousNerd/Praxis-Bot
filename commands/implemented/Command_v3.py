
from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction, Function_Helpers

from bot_functions import utilities_script as utility

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
        command_returnStringProcessed = ""
        # example return string: "@(user) sent a message"
        # example return string: "@(user) rolled $(roll #(0))"


        # Proccess strings
        fullCommand = command + " " + rest # This creates the full command string.
        commandArguments = utility.get_args(rest)

        functionsList = self.searchForFunctions(command_returnString) # Generates a list of functions to run in a specific order. Inner to Outer Most

        for function in functionsList:
            if function[2] == True: # If function contains a function
                pass
            else:
                self.run_function(user, function, fullCommand)

        returnString = user + " sent: [ " + command + " ] with: " + rest
        #print(returnString)


        return returnString

    def searchForFunctions(self, input):
        parserContent = pyparsing.Word(pyparsing.alphanums)
        parser = pyparsing.nestedExpr('@(', ')')
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

    def do_function():
        return None