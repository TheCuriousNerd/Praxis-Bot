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
import utilities_script as utilities
import os

class tempText_Module():
    def __init__(self):
        super().__init__()
        self.tempText_items = {}

    def main(self):
        pass

    def makeItem(self, tempTextItem_):
        self.addItem(tempTextItem_.itemName, tempTextItem_.itemTitle, tempTextItem_.itemContent)
        self.tempText_stringUpdater()
        self.update_tempTextFiles()

    def addItem(self, name, title, content):
        newItem:tempTextItem = tempTextItem(name=name, title=title, content=content)
        newItem.setupItem(name, title, content)
        self.tempText_items[name] = newItem

    def getItem(self, name):
        return self.tempText_items[name]

    def updateItem(self, name, title, content):
        newItem:tempTextItem = tempTextItem(name=name, title=title, content=content)
        newItem.setupItem(name, title, content)
        self.tempText_items[name] = newItem

    def deleteItem(self, name):
        return self.tempText_items.pop(name, None)

    def tempText_stringUpdater(self):
        for c in self.tempText_items:
            self.tempText_items[c].item_stringUpdater()

    def update_tempTextFiles(self):
        dir = utilities.get_dir("stream_sources")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

        for key in self.tempText_items:
            item = self.tempText_items[key]
            relative_path = "stream_sources/" + item.itemName + ".txt"
            real_file_path = os.path.join(script_dir, relative_path)

            file = open(real_file_path, "wb")
            itemText_ = item.item_stringUpdater().encode("utf8")
            file.write(itemText_)
            file.close

    def getTempTextFile(self, key):
        dir = utilities.get_dir("stream_sources")
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        relative_path = "stream_sources/" + key + ".txt"
        real_file_path = os.path.join(script_dir, relative_path)

        file = open(real_file_path, "rb")
        text = file.read()
        #print(text)
        file.close
        return text


class tempTextItem():
    def __init__(self, name = "", includeTitle = True, title = "", content = ""):
        super().__init__()
        self.itemName = name #This will determine the fileName

        self.includeTitle = includeTitle
        self.itemTitle = title
        self.itemContent = content

        self.itemComputedString = ""

    def setupItem(self, name, title, content):
        print("\nSetting up tempTextItem {", name,"}[", title, content, "]")
        self.itemName = name
        self.itemTitle = title
        self.itemContent = content
        self.item_stringUpdater()

    def item_stringUpdater(self):
        newString = ""
        if self.includeTitle == True:
            newString = newString + self.itemTitle
            newString = newString + self.itemContent
        self.itemComputedString = newString
        return self.itemComputedString



if __name__ == "__main__":
    testModule = tempText_Module()
    testModule.main()

    testItem = tempTextItem("testy","title: ", "content content content")
    testModule.makeItem(testItem)

    testModule.update_tempTextFiles()