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

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Abstract_Function_Helpers

from bot_functions import utilities_script as utility

from bot_functions.Mathematician import Mathematician

class Function_Math_unitConversion(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "math_unitConversion"
    helpText = ["This is a v0 function.",
        "\nExample:","testFunction"]

    def __init__(self):
        super().__init__(
            functionName = Function_Math_unitConversion.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_Math_unitConversion.helpText,
            bonusFunctionData = None
            )

    def do_function(self, tokenSource, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):
        #mathProblem = utility.list_to_string(args)

        mathematician = Mathematician()
        mathResults = mathematician.solve_unitConversion(args[0], args[1], args[2])

        return mathResults