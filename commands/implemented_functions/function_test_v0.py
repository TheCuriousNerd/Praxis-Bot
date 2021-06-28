from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Function_Helpers

from bot_functions import utilities_script as utility

class Function_v0(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "testFunction"
    helpText = ["This is a v0 function.",
        "\nExample:","testFunction"]

    def __init__(self):
        super().__init__(
            functionName = Function_v0.functionName,
            n_args=0,
            functionType=AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_v0.helpText
            )

    def do_function(self, user, input):
        self.input_check(input)
        output = self.do_work(user, input)

        return output

    def do_work(self, user, input):
        work = input
        return work

    def input_check():
        return None