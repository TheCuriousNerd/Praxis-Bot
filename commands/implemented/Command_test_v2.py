# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
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

from commands.command_base import AbstractCommand

import utilities_script as utility

class Command_test_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the test command.
    """
    command = "testerino"

    def __init__(self):
        super().__init__(Command_test_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["This is a test command.",
        "\nExample:","testerino"]
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):
        returnString = user + " sent: [ " + command + " ] with: " + rest
        #print(returnString)
        return returnString

    def get_help(self):
        return self.help