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

import config
from bot_functions import utilities_script as utilities
import os

class Chyron_Module():
    def __init__(self):
        super().__init__()
        self.chyron_computedString = ""
        self.chyron_items:list = []

    def main(self, rightNow_ = "Chill Stream"):
        self.addItem(
            "RightNow",
            "► Now:   ",
            rightNow_)
        self.addItem(
            "WeekDays",
            "► Weekdays:   ",
            "Daily Dev Streams starting around 3:30pm EST")
        self.addItem(
            "ThuFriSat",
            "► Friday & Saturday:   ",
            "FFxiv (Express Delivery Raid Team) Thu, Fri, Sat @ 7pm EST")
        self.addItem(
            "Commands",
            "► Commands:   ",
            "!animal,   !climateclock,   !discord,   !github,   !lights,   !math,   !roll")
        #self.addItem(
        #    "Website",
        #    "► Want to read about my various projects?  visit:   ",
        #    "TheCuriousNerd.com")
        self.addItem(
            "Follow",
            "► ",
            "If you like what you see and want more, hit the follow button to see more!")
        self.addItem(
            "Discord",
            "► Need help with Praxis Bot or with some other project? Join our discord!  Type:  \" !d \"  in chat to get the link or visit:   ",
            "discord.io/thecuriousnerd")

    def chyron_stringUpdater(self):
        newString = ""
        for c in self.chyron_items:
            c.item_stringUpdater()
            newString = newString + c.itemComputedString
            for x in range(config.chyronListSpaceCount):
                newString = newString + " "
        self.chyron_computedString = newString
        return newString

    def addItem(self, name, title, content):
        newItem:ChyronItem = ChyronItem()
        newItem.setupItem(name, title, content)
        self.chyron_items.append(newItem)

    def removeItem(self, name):
        for c in self.chyron_items:
            if c.itemName == name:
                self.chyron_items.remove(c)

    def updateChyronFile(self):
        dir = utilities.get_dir("stream_sources")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir = ""
        relative_path = "../Praxis/stream_sources/chyron.txt"
        real_file_path = os.path.join(script_dir, relative_path)

        file = open(real_file_path, "wb")
        chyron = self.chyron_stringUpdater().encode("utf8")
        file.write(chyron)
        file.close

    def getChyronFile(self):
        dir = utilities.get_dir("stream_sources")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        script_dir = ""
        relative_path = "../Praxis/stream_sources/chyron.txt"
        real_file_path = os.path.join(script_dir, relative_path)

        file = open(real_file_path, "rb")
        text = file.read()
        #print(text)
        file.close
        return text


class ChyronItem():
    def __init__(self):
        super().__init__()
        self.itemName = ""

        self.includeTitle = True
        self.itemTitle = ""
        self.itemContent = ""

        self.itemComputedString = ""

    def setupItem(self, name, title, content):
        print("\nSetting up Item {", name,"}[", title, content, "]")
        self.itemName = name
        self.itemTitle = title
        self.itemContent = content

    def item_stringUpdater(self):
        newString = ""
        if self.includeTitle == True:
            newString = newString + self.itemTitle
            newString = newString + self.itemContent
        self.itemComputedString = newString



if __name__ == "__main__":
    testModule = Chyron_Module()
    testModule.main()
    testModule.chyron_stringUpdater()

    test = testModule.chyron_computedString + "<<<|"
    print(test)

    testModule.updateChyronFile()