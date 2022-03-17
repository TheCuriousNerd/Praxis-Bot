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

from asyncio.tasks import sleep
import os
import sys
import re
from tkinter.messagebox import NO
import psutil
import subprocess
import platform
import time
import config as config
import art

clearScreen = lambda: os.system('cls' if os.name == 'nt' else 'clear')

urlMatcher = re.compile("(https?:(/{1,3}|[a-z0-9%])|[a-z0-9.-]+[.](com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw))")

def contains_url(input: str):
    containsURL = re.search(urlMatcher, input.lower()) is not None
    return containsURL

def contains_pattern(input:str, pattern):
    return re.search(pattern, input.lower()) is not None

def get_args(text: str) -> list:
    return text.split(" ")

# This takes all items from a list and puts them into a string, separated by a space
def list_to_string(list_to_convert):
    return " ".join(filter(None, list_to_convert))

def nextGreaterElementInList(list, integer): # This assumes list is ordered?
    try:
        return next(x for x in list if x > integer), False
    except:
        return list[-1], True

def does_contain_OnlyNumbers(text):
    isJustNumbers = False
    print("checking numbers")
    try:
        for x in range(10):
            if str(x) in str(text):
                isJustNumbers = True
        else:
            isJustNumbers = False
    except:
        pass

    return isJustNumbers

def rescale_value(value, min, max):
    #print("trying Rescale")
    returnValue = (value - min) / (max - min)
    #print("got ", returnValue)
    return returnValue

def strToBool(stringToTest):
        if stringToTest == "True":
            return True
        else:
            return False

def get_dir(selected_dir):
    """
    Checks for the tts directory, and will create it if it does not exist
    :return: the relative file path of the tts dir
    """
    dir = os.path.join(os.getcwd(), selected_dir)  # this is platform-agnostic
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def contains_value(self, search: str, data:str):
        contains = re.search(search, data)
        return contains.group(0)

def contains_slur(input: str):
    containsSlur: bool = False
    parsedMessage = input.split(" ")
    for word in parsedMessage:
        for slur in config.slurList:
            if word.lower() == slur:
                containsSlur = True
                break
        if containsSlur:
            break

    if containsSlur:
        print("<{ slur detected! }> ")
    return containsSlur

def parse_line(message: str):
        first_space = False
        start = -1
        idx = -1
        for x in range(0, len(message)):
            c = message[x]
            if c == ' ':
                if first_space:
                    idx = x
                    break
                else:
                    first_space = True
                    pass
            else:
                first_space = True
                if start == -1:
                    start = x

        if idx == -1:
            idx = len(message)

        command = message[start:idx]
        rest = message[idx + 1:]
        return command, rest

def miniParser(stringToParse: str):
    stringToParse = "(%s)" % stringToParse
    level_dict = {}
    level_map = {} # Have this so we can know how to rebuild a string from this.
    level = 0
    level_char = ''
    level_mapping = []
    charPosition = 0
    for char_ in stringToParse:
        if char_ == '(':
            if level not in level_dict:
                level_dict[level] = [level_char]
                level_map[level] = [charPosition]
            elif level_char != '':
                level_dict[level].append(level_char)
                level_map[level].append(charPosition)
            level_char = ''
            level += 1
        elif char_ == ')':
            if level not in level_dict:
                level_dict[level] = [level_char]
                level_map[level] = [charPosition]
            elif level_char != '':
                level_dict[level].append(level_char)
                level_map[level].append(charPosition)
            level_char = ''
            level -= 1
        else:
            level_char += char_
        charPosition += 1
    return level_dict, level_map

def miniParserReverser(parseToReverse: dict, parseMap: dict, keep_parenthesis: bool = False):
    #This reverses the miniparser results
    reversedResults = []
    reversedResultsString = ""

    #parseKeys = parseToReverse.keys()
    mapKeys = parseMap.keys()

    # curLevel = 0
    # curTargetListEntry = 0
    # targetLevel = 0 # This is the level we want to get to (the next lowest value in the parseMap)
    # targetListEntry = 0 # This is the index of the list entry in the parseMap that we want to get to
    # charCounter = 0
    # charCounterLast = 0

    totalStringsToJoin = 0
    compiledMapKeys = []
    for mapKey in mapKeys:
        tempMapList = parseMap[mapKey]
        for temp in tempMapList:
            compiledMapKeys.append(temp)
    compiledMapKeys.sort()

    totalStringsToJoin = len(compiledMapKeys)
    #print("totalStringsToJoin: ", totalStringsToJoin)
    #print("compiledMapKeys: ", compiledMapKeys)

    selectedLevel = 0
    selectedListEntry = 0
    curCharKey = 0

    curLevel = 0
    bonusParaCounter = 0

    isFullyResolved = False
    while not isFullyResolved:
        for mapKey in mapKeys:
            tempMapList = parseMap[mapKey]
            for temp in tempMapList:
                #print("temp: ", temp)
                if temp == curCharKey:
                    try:
                        curCharKey = compiledMapKeys[compiledMapKeys.index(temp)+1]
                    except:
                        curCharKey = compiledMapKeys[-1]
                    #print("curCharKey: ", curCharKey)
                    selectedLevel = mapKey
                    selectedListEntry = tempMapList.index(temp)
                    #print("Found a match at level: ", selectedLevel, " and list entry: ", selectedListEntry)
                    textToAppend = parseToReverse[selectedLevel][selectedListEntry]

                    # Check if it went up or down a level
                    if keep_parenthesis:
                        if mapKey != curLevel:
                            if mapKey < curLevel:
                                reversedResults[-1] = reversedResults[-1] + (")"*(curLevel - mapKey))
                                bonusParaCounter -= (curLevel - mapKey)
                            if mapKey > curLevel:
                                textToAppend = "(" + textToAppend
                                bonusParaCounter += 1
                                if totalStringsToJoin == 1:
                                    bonusParaCounter += 0
                            curLevel = mapKey
                        elif mapKey == curLevel and curLevel > 0:
                            reversedResults[-1] = reversedResults[-1] + (")"*(mapKey - 1)) + ("("*(mapKey - 1))

                    reversedResults.append(textToAppend)
                    totalStringsToJoin -= 1
        if totalStringsToJoin == 0:
            isFullyResolved = True

    reversedResultsString = "".join(reversedResults)
    if keep_parenthesis:
        #bonusParaCounter = bonusParaCounter - 1
        #print("last bonusParaCounter: ", bonusParaCounter)
        reversedResultsString = reversedResultsString + bonusParaCounter*")"

    return reversedResultsString

def parserEntryCoordLookup(parsedData: dict, data):
    level = 0
    levelEntry = 0

    for parseData_Level in parsedData:
        levelEntry = 0
        for parseData_LevelEntry in parsedData[parseData_Level]:
            if parseData_LevelEntry == data:
                level = parseData_Level
                return level, levelEntry
            else:
                levelEntry += 1

    return level, levelEntry

def isRunningInDocker():
    isD = os.getenv('ISDOCKER')
    if isD is None:
        return False
    return isD == True

def getContainerName():
    try:
        return os.getenv('CONTAINER_NAME')
    except:
        return None

def hard_shutdown():
    current_system_pid = os.getpid()

    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()

def restart_self():

    #current_system_pid = os.getpid()
    #os.startfile("python C:/praxis/main.py")
    #subprocess.run("python C:/praxis/main.py")
    #subprocess.call("python main.py", shell=True)
    if platform.system() == 'Windows':
        os.system('start cmd /k python main.py')
        hard_shutdown()
    if platform.system() == 'Linux':
        os.system('xfce4-terminal -e "python main.py"')
        hard_shutdown()

    #os.system('python twitch_script.py')
    #os.system('python discord_script.py')

def restart_target():
    pass

def launch_target(inputScript: str):
    cmd = "start cmd /k python " + inputScript
    os.system(cmd)

def splashScreen():
    if not config.skip_splashScreenClear:
            clearScreen()
    art.tprint("----------",font="slant")
    art.tprint("Praxis Bot",font="graffiti")
    art.tprint("----------",font="slant")
    print("-Maintained by Alex Orid, TheCuriousNerd.com\nFor help visit discord.com/invite/sNTXWn4")
    print("ver: " + config.praxisVersion_Alpha + config.praxisVersion_Delta + config.praxisVersion_Omega)
    print("\n\n\n")
    if not config.skip_splashScreenSleep:
            time.sleep(3)

if __name__ == "__main__":
    splashScreen()