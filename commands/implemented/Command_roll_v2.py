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

from commands.command_base import AbstractCommand

import random
import bot_functions.utilities_script as utility

class Command_roll_v2(AbstractCommand, metaclass=ABCMeta):
    """
    this is the roll command.
    """
    command = "!roll"

    def __init__(self):
        super().__init__(Command_roll_v2.command, n_args=1, command_type=AbstractCommand.CommandType.Ver2)
        self.help = ["This will roll dice, based on your inputs.",
        "\nExample:","roll \"d20\"", "roll \"1D20+5\"", "roll \"10df\"", "roll \"10Df+3\""]
        self.isCommandEnabled = True

    def do_command(self, source = AbstractCommand.CommandSource.default, user = "User",  command = "", rest = "", bonusData = None):
        returnString = user + " sent: [ " + command + " ] with: " + rest

        if ("f") in rest.lower():
            returnString = self.roll(2, user, command + " " +rest)
        else:
            returnString = self.roll(1, user, command + " " +rest)

        return returnString

    def roll(self, roll_type, user, user_message):
        diceRoll = ""
        switch = {
            1: "Standard",
            2: "Fate Dice"
        }
        temp_preParsedMessage = user_message.split("+")

        tempParsedMessage = temp_preParsedMessage[0].split(" ")
        temp_dice_stmt: str = tempParsedMessage[1]
        parsedMessage = temp_dice_stmt.lower().split("d")

        loopBool: bool = False
        if parsedMessage[0] != "":
            loopBool = True
        if loopBool == True:
            if int(parsedMessage[0]) == 1:
                loopBool = False

        if roll_type == 1:
            print("-rolling...")
            # If roll is in xdx+x format
            if loopBool == True:
                rolls: list = []
                for x in range(int(parsedMessage[0])):
                    rolls.append(random.randint(1, int(parsedMessage[1]))) # This is the roller

                rollTotal = 0
                for roll in rolls:
                    rollTotal = rollTotal + roll
                    diceRoll = diceRoll + str(roll) + ", "
                diceRoll = diceRoll[:-2]  # This removes the last two characters in the string

                if len(temp_preParsedMessage) == 2:
                    diceRoll = diceRoll + " + " + temp_preParsedMessage[1] + " = " + str(
                        rollTotal + int(temp_preParsedMessage[1]))
                else:
                    diceRoll = diceRoll + " = " + str(rollTotal)
            # If roll is in dx+x format
            if loopBool == False:
                roll: int = random.randint(1, int(parsedMessage[1])) # This is the roller

                if len(temp_preParsedMessage) == 2:
                    diceRoll = str(roll) + " + " + temp_preParsedMessage[1] + " = " + str(
                        roll + int(temp_preParsedMessage[1]))
                else:
                    diceRoll = str(roll)
            diceRoll = user + " rolled: " + diceRoll

        if roll_type == 2:

            print("-fate Rolling....")
            # !roll 4df
            # If roll is in xdx+x format
            if loopBool == True:
                rolls: list = []
                for x in range(int(parsedMessage[0])):
                    rolls.append(random.randint(-1, 1)) # This is the roller

                rollTotal = 0
                for roll in rolls:
                    rollTotal = rollTotal + roll
                    diceRoll = diceRoll + str(roll) + ", "
                diceRoll = diceRoll[:-2]  # This removes the last two characters in the string

                if len(temp_preParsedMessage) == 2:
                    diceRoll = diceRoll + " + " + temp_preParsedMessage[1] + " = " + str(
                        rollTotal + int(temp_preParsedMessage[1]))
                else:
                    diceRoll = diceRoll + " = " + str(rollTotal)
            # If roll is in dx+x format
            if loopBool == False:
                roll: int = random.randint(-1, 1) # This is the roller

                if len(temp_preParsedMessage) == 2:
                    diceRoll = str(roll) + " + " + temp_preParsedMessage[1] + " = " + str(
                        roll + int(temp_preParsedMessage[1]))
                else:
                    diceRoll = str(roll)
            diceRoll = user + " fate rolled: " + diceRoll

        return diceRoll

    def get_help(self):
        return self.help