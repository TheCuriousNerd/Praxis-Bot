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

from concurrent.futures import thread
from enum import Enum, auto
import enum
from random import randint
import pyparsing
import shlex

from bot_functions import utilities_script as utility
from bot_functions import utilities_db
from commands import loader_functions as function_loader
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

import re

from simpleeval import simple_eval

import threading
import time

class TokenType(Enum):
    NONE = auto()
    ARGUMENT = auto()
    FUNCTION = auto()
    VARIABLE = auto()

class Token_Processor():
    def __init__(self):
        super().__init__(
        )
        self.loadedFunctions = function_loader.load_functions(AbstractCommandFunction.FunctionType.ver0)
        self.functionCounter = self.FunctionCounter()

    def setup(self):
        pass

    def parseTokenResponse(self, userName, userID, commandRawInput:str, command_returnString, tokenSource):
        combinedUserData = {}
        combinedUserData["userName"] = userName
        combinedUserData["userID"] = userID
        commandArguments = utility.get_args(commandRawInput)
        #This removes the command from the arguments
        commandArguments.pop(0)

        #tempArg = commandRawInput.split("( )")
        tempArg = re.split("( )", commandRawInput)
        tempArg.pop(0)
        try:
            tempArg.pop(0)
        except:
            pass
        tempArg = self.cleanupTempArgs(tempArg)
        #print("\ntempArgs:")
        #for t in tempArg:
        #    print(t)

        #print("\nCommand Return String:")
        #print("\n" + str(command_returnString))
        response = self.new_stringFunctionParser(command_returnString, tempArg, combinedUserData, commandRawInput, tokenSource)
        return response

    def new_stringFunctionParser(self,
            input:str = "",
            arguments:list = [],
            userData = {},
            commandRawInput = "",
            tokenSource = None
            ):
        output = None
        print("Lets bake this string!!!")
        print(input)
        print(arguments)
        print(userData)
        print(commandRawInput)
        print(tokenSource)
        print("\n")


        parsedInput, parsedInputMap = utility.miniParser(input)
        print("\nParsed Input:")
        print(parsedInput)
        print("\nParsed Input Map:")
        print(parsedInputMap)
        compiledMapKeys = []
        for mapKey in parsedInputMap:
            tempMapList = parsedInputMap[mapKey]
            for temp in tempMapList:
                compiledMapKeys.append(temp)
        totalMapLevels = len(parsedInputMap)
        compiledMapKeys.sort()
        print("\nCompiled Map Keys:")
        print(compiledMapKeys)
        print("\nTotal Map Levels:")
        print(str(totalMapLevels) + "\n")

        # This is the main loop that will go through the parsedInput and replace tokens with the appropriate values.
        # If crazyLoop is true, then it will continue to loop until it finds no more tokens. From the innermost nested token to the outermost.
        crazyLoop = False

        if crazyLoop == False:

            # The part that handles the arguments ie (#*) and (#0)
            print("Argument Parsing...")
            for curMapLevel in parsedInput:
                parsedInputEntryCount = 0
                if curMapLevel > 1:
                    for entry in parsedInput[curMapLevel]:
                        if "#*" in entry:
                            print(entry)
                            parsedInput[curMapLevel][parsedInputEntryCount] = " ".join(filter(None, arguments))
                        for i in range(0, 10):
                            if "#%s" % (str(i)) in entry:
                                print("#%s" % (str(i)))
                                parsedInput[curMapLevel][parsedInputEntryCount] = arguments[i]
                        parsedInputEntryCount += 1

            # The part that handles the variables ie (@variable)
            print("Variable Parsing...\n")
            for curMapLevel in parsedInput:
                parsedInputEntryCount = 0
                if curMapLevel > 1:
                    for entry in parsedInput[curMapLevel]:
                        if "@" in entry:
                            try:
                                targetVarName = entry[1:]
                                print(entry)
                                db = utilities_db.Praxis_DB_Connection(autoConnect=True)
                                tableName = "home_praxisbot_commands_v0_savedvariables"
                                results = db.getItemRow(tableName, "name", targetVarName)
                                print(results)
                                varData = str(results[2])
                                parsedInput[curMapLevel][parsedInputEntryCount] = varData
                            except:
                                print("Error: Variable not found.\n")
                                varData = ""
                                parsedInput[curMapLevel][parsedInputEntryCount] = varData
                        parsedInputEntryCount += 1



            # The part that handles the functions ie ($function)
            print("Function Parsing...")
            compiledFunctionsToRun = []
            compiledThreadsToRun = []
            for curMapLevel in parsedInput:
                parsedInputEntryCount = 0
                if curMapLevel > 1:
                    for entry in parsedInput[curMapLevel]:
                        if "$" in entry: # Replace this with a comparison to the function list to see if the entry is a valid function
                            print("\n]>>> Function " + entry)
                            #print(curMapLevel)
                            #print(parsedInputEntryCount)
                            print(parsedInput[curMapLevel][parsedInputEntryCount])
                            print("Function Starting Point: " + str(parsedInputMap[curMapLevel][parsedInputEntryCount]))
                            currentInputMapPoint = parsedInputMap[curMapLevel][parsedInputEntryCount]
                            currentInputMapPoint_max = 0
                            try:
                                currentInputMapPoint_max = parsedInputMap[curMapLevel][parsedInputEntryCount + 1]
                            except:
                                currentInputMapPoint_max = -1
                            print("Function Max Allowed Point: " + str(currentInputMapPoint_max))
                            steps = 0
                            functionStrings = []
                            functionStringsMap = []
                            functionStrings.append(parsedInput[curMapLevel][parsedInputEntryCount])
                            functionStringsMap.append(parsedInputMap[curMapLevel][parsedInputEntryCount])
                            functionStringsDict = {}
                            functionStringsDict[parsedInputMap[curMapLevel][parsedInputEntryCount]] = parsedInput[curMapLevel][parsedInputEntryCount]
                            def recursiveForwardSearch(steps, currentInputMapPoint):
                                #print("]>recursiveForwardSearch")
                                #print("]>steps: " + str(steps))
                                #print("]>curMapLevel: " + str(curMapLevel))
                                try:
                                    #print("Cur: " + str(parsedInput[curMapLevel + steps]))
                                    tempBlock = False # Temp Block is used in the later if statement to only run once if the condition is true.
                                    furtherEntryCounter = 0
                                    for furtherEntry in parsedInput[curMapLevel + steps]:
                                        #print(furtherEntryList)
                                        #print(parsedInputMap[entry + steps])
                                        try:
                                            try:
                                                #print("currentInputMapPoint: ")
                                                #print(currentInputMapPoint)
                                                #print("parsedInputMap: ")
                                                #print(parsedInputMap[curMapLevel + steps][furtherEntryCounter])
                                                newPoint = parsedInputMap[curMapLevel + steps][furtherEntryCounter]
                                                if (currentInputMapPoint < newPoint) and ((newPoint < currentInputMapPoint_max) or currentInputMapPoint_max == -1):
                                                    #print("results: " + furtherEntry)
                                                    #functionStrings.append(furtherEntry)
                                                    #print(parsedInputMap[curMapLevel + steps][furtherEntryCounter])
                                                    #functionStringsMap.append(parsedInputMap[curMapLevel + steps][furtherEntryCounter])
                                                    functionStringsDict[newPoint] = furtherEntry
                                                    currentInputMapPoint = parsedInputMap[curMapLevel + steps][furtherEntryCounter]
                                                    tempBlock = True
                                            except:
                                                pass
                                            #print("Going up...")
                                            recursiveForwardSearch(steps + 1, currentInputMapPoint)
                                            tempBlock = False
                                        except:
                                            pass
                                            #print("No further entries")
                                        furtherEntryCounter += 1
                                    #print("Going down...")
                                    steps -= 1
                                except:
                                    pass
                                #print("]>recursiveForwardSearch COMPLETE")
                            recursiveForwardSearch(steps, currentInputMapPoint)
                            #print("Steps: " + str(steps))
                            print("\nFunction Strings: " + str(functionStrings))
                            print("Function Strings Map: " + str(functionStringsMap))
                            print("Function Strings Dict: " + str(functionStringsDict))
                            compiledFunctionsToRun.append(functionStringsDict)
                            collectedStringKeys = functionStringsDict.keys()


                            # innerFunctions = {}
                            # for key in collectedStringKeys:
                            #     if "$" in functionStringsDict[key]:
                            #         print("Inner Function: " + functionStringsDict[key])
                            #         innerFunctions[key] = functionStringsDict[key]
                            # print("Captured Functions: ")
                            # print(innerFunctions)


                        parsedInputEntryCount += 1

            # The part that handles the compiled functions ie ($function)
            print("\nCompiled Functions: ")
            print(compiledFunctionsToRun)
            print("\n")

            thread_points = []
            thread_all_points = []
            threadsToRunLast = []
            specialFunctionList = []
            specialFunctionTypes = ["if", "random", "thread"]
            thread_startTime = (time.time()+0.25)

            for fCount in range(len(compiledFunctionsToRun)):
                for comp_ in compiledFunctionsToRun[fCount]:
                    # print(comp_)
                    # print(compiledFunctionsToRun[fCount][comp_])
                    if "thread" in compiledFunctionsToRun[fCount][comp_]:
                        thread_points.append(comp_)

            for compiled_ in compiledFunctionsToRun:
                for c_ in compiled_:
                    if "thread" in compiled_[c_]:
                        for key in compiled_:
                            thread_points.append(key)
            thread_points = list(dict.fromkeys(thread_points))

            for fCount in range(len(compiledFunctionsToRun)):
                print("\n Work Loop Start")
                if len(compiledFunctionsToRun) >= fCount:
                    specialFunctionFound = False
                    specialFunction = {"name":"", "startPoint":0}
                    compiledWork = compiledFunctionsToRun[fCount - 1]
                    for work_ in compiledWork:
                        print("found work")
                        #print(compiledWork[work_])
                        # If statement function handling
                        # This will check for an if statement and if it is true it will allow the inner functions to run and be returned.
                        if "if" in compiledWork[work_]:
                            # print("This is an if statement: ")
                            # print(compiledWork[work_])
                            # print(str(work_))
                            specialFunctionFound = True
                            specialFunction["name"] = compiledWork[work_][1:] # This will remove the $ from the function name
                            specialFunction["startPoint"] = work_
                            specialFunctionList.append(specialFunction)


                        # Random function handling
                        # This will check for the random function and if it has one, it will randomly clear all the inputs, except for one.
                        if "random" in compiledWork[work_]:
                            # print("This is a random statement: ")
                            # print(compiledWork[work_])
                            # print(str(work_))
                            specialFunctionFound = True
                            if "$" in compiledWork[work_]:
                                specialFunction["name"] = compiledWork[work_][1:] # This will remove the $ from the function name
                            else:
                                specialFunction["name"] = compiledWork[work_]
                            specialFunction["startPoint"] = work_
                            specialFunctionList.append(specialFunction)

                        # Threading function handling
                        # This will check for the threading function and if it has one, it will create threads for each input it receives.
                        if "thread" in compiledWork[work_]:
                            print("This is a thread statement: ")
                            print(compiledWork[work_])
                            print(str(work_))
                            specialFunctionFound = True
                            specialFunction["name"] = compiledWork[work_][1:] # This will remove the $ from the function name
                            dict_lowest_points = []
                            thread_root_points = []

                            for dict_ in compiledFunctionsToRun:
                                dict_lowest_points_temp = []
                                for key in dict_:
                                    dict_lowest_points_temp.append(key)
                                dict_lowest_points_temp.sort()
                                dict_lowest_points.append(dict_lowest_points_temp[0])
                            print(dict_lowest_points)

                            # def shouldBeThreaded(key_to_test, thread_root_points):
                            #     isThreaded = False
                            #     for th_r in thread_root_points:
                            #         for dict_ in compiledFunctionsToRun:
                            #             if dict_.get(key_to_test, 0) == th_r:
                            #                 # This is a thread root
                            #                 for key in dict_:
                            #                     if key == key_to_test:
                            #                         isThreaded = True
                            #     return isThreaded

                            for compiled_ in compiledFunctionsToRun:
                                for c_ in compiled_:
                                    if "thread" in compiled_[c_]:
                                        for key in compiled_:
                                            thread_root_points.append(key)

                            thread_root_points = list(dict.fromkeys(thread_root_points))

                            print(thread_root_points)
                            thread_points.extend(thread_root_points)
                            thread_points = list(dict.fromkeys(thread_points))
                            thread_all_points.extend(thread_root_points)
                            thread_all_points = list(dict.fromkeys(thread_all_points))

                            specialFunction["startPoint"] = work_
                            specialFunction["thread_points"] = thread_points # This should contain the keys of the functions that need to be threaded.
                            print(thread_points)
                            specialFunctionList.append(specialFunction)


                def worker(key, keyList, workToDo, parsedInput, parsedInputMap, specialFunctionList, compiledFunctionsToRun, userData, startTime=0):
                    print("\n WORKER STARTED")
                    while int(time.time()) < startTime:
                        time.sleep(0.001)
                    targetCommand = ""
                    targetCommandKey = 0
                    targetCommandParams = ""
                    resultDestination = (0,0)

                    targetCommandParamsPrep = []
                    grabbedFunction = False
                    for key in keyList:
                        if grabbedFunction == False:
                            resultDestination = utility.parserEntryCoordLookup(parsedInputMap, key)
                            targetCommand = workToDo[key]
                            targetCommandKey = key
                            #workToDo[key] = "resultsNotSet"
                            grabbedFunction = True
                        else:
                            if targetCommand[1:].strip() not in specialFunctionTypes:
                                key_location = utility.parserEntryCoordLookup(parsedInputMap, key)
                                targetCommandParamsPrep.append(parsedInput[key_location[0]][key_location[1]])
                                parsedInput[key_location[0]][key_location[1]] = "" # This will clear the entry in the dict so that the results can be displayed.
                                workToDo[key] = ""
                        #print(key)
                        #print(workToDo[key])
                        #print(utility.parserEntryCoordLookup(parsedInputMap, key))
                    targetCommandParams = " ".join(filter(None, targetCommandParamsPrep))
                    reResultsPrepped_arg = re.split("( )", targetCommandParams)
                    preppedParams = self.cleanupTempArgs(reResultsPrepped_arg)

                    print("\nTarget Key: " + str(key))
                    print("\nTarget Command: " + targetCommand)
                    targetCommand = targetCommand[1:].strip() # Removes the $
                    print("Target Command: " + targetCommand)
                    print("Target Command Params::" + str(preppedParams) + "::")

                    if self.does_function_exist(targetCommand) == True:
                        print("\nFunction Exists")
                        functionResults = ""
                        print("!!!EXECUTING FUNCTION!!!")
                        print("Function: " + targetCommand)
                        functionResults = self.run_function(userData, targetCommand, preppedParams, tokenSource)
                        print("Function Results: " + str(functionResults))
                        #functionResults = "[FUNCTION COMPLETE]"
                        parsedInput[resultDestination[0]][resultDestination[1]] = str(functionResults)
                        workToDo[targetCommandKey] = str(functionResults)

                    if "if" in targetCommand:
                        specialFunctionWork = specialFunctionList[0]
                        print("\nHandling the if statement: ")
                        print("Starting Point: ")
                        print(specialFunctionWork["startPoint"])
                        targetLogicPoint, isEnd  = utility.nextGreaterElementInList(keyList, specialFunctionWork["startPoint"])
                        #targetLogicPoint, isEnd = utility.nextGreaterElementInList(keyList, targetLogicPoint)
                        print("Target Logic Point: ")
                        print(targetLogicPoint)
                        #targetResultsPoint, isEnd = utility.nextGreaterElementInList(keyList, targetLogicPoint)

                        for lvl in parsedInputMap:
                            if targetLogicPoint in parsedInputMap[lvl]:
                                targetResultsPoint, bonus = utility.nextGreaterElementInList(parsedInputMap[lvl], targetLogicPoint)

                        print("Target Results Point: ")
                        print(targetResultsPoint)

                        logicToCompile = []
                        for key in keyList:
                            if key >= targetLogicPoint:
                                if key < targetResultsPoint:
                                    logicToCompile.append(workToDo[key])
                        logicToEval = "".join(filter(None, logicToCompile))

                        print(workToDo)
                        print("Logic To Eval: ")
                        print(logicToEval)
                        print("Result:")
                        print(simple_eval(str(logicToEval)))
                        if str(simple_eval(str(logicToEval))).lower() == "true":
                            thingsToAdd = []

                            for key in keyList:
                                if key >= targetResultsPoint:
                                    thingsToAdd.append(workToDo[key])
                                if key >= targetLogicPoint:
                                    targetDestination = utility.parserEntryCoordLookup(parsedInputMap, key)
                                    parsedInput[targetDestination[0]][targetDestination[1]] = "" # This will clear the entry in the dict so that the results can be displayed.

                            print("Function Results: " + str(thingsToAdd))
                            parsedInput[resultDestination[0]][resultDestination[1]] = "".join(filter(None, thingsToAdd))

                    # This forwards the data to the next function.
                    for key in keyList:
                        funcCounter = 0
                        for workToDo_ in compiledFunctionsToRun:
                            for w_ in workToDo_:
                                if w_ == key:
                                    print("\nForwarding data to next function: ")
                                    print("target key: " + str(key))
                                    workToDo_[w_] = workToDo[w_]
                            funcCounter += 1
                            print(workToDo_)
                    return parsedInput


                print("\n Special Function List: ")
                print(specialFunctionList)

                workToDo:dict = compiledFunctionsToRun.pop(-1)
                print("\nworkToDo: ")
                print(workToDo)
                print(workToDo.keys())
                keyList = []
                for key in workToDo:
                    keyList.append(key)
                keyList.sort()
                print("\nkeyList: ")
                print(keyList)
                print("\nThread Points: ")
                print(thread_points)


                print("LAST CALL BEFORE RUNNING FUNCTIONS")

                if keyList[0] in thread_points:
                    print("\nThreading Function Found")
                    print("Threading Function: " + str(keyList[0]))
                    #parsedInput = worker(key, keyList, workToDo, parsedInput, parsedInputMap, specialFunctionList, compiledFunctionsToRun)
                    parsedInputCopy = {}
                    for k in parsedInput:
                        parsedInputCopy[k] = parsedInput[k]

                    thread_ = threading.Thread(target=worker, args=(key, keyList, workToDo, parsedInputCopy, parsedInputMap, specialFunctionList, compiledFunctionsToRun, userData, thread_startTime))
                    threadsToRunLast.append(thread_)
                    #thread_points.remove(keyList[0])
                else:
                    if key not in thread_all_points:
                        parsedInput = worker(key, keyList, workToDo, parsedInput, parsedInputMap, specialFunctionList, compiledFunctionsToRun, userData)

            for thread_ in threadsToRunLast:
                thread_.daemon = True
                thread_.start()

            def thread_checker(threadsToRunLast):
                for thread_ in threadsToRunLast:
                    if thread_.is_alive():
                        return True
                return False

            while thread_checker(threadsToRunLast):
                time.sleep(0.1)
                print("\nTHREADS still running...")

                # for thread_ in threadsToRunLast:
                #     thread_.join()


                # for th in threadsToRunLast:
                #     while th.is_alive():
                #         time.sleep(0.001)


                # if len(threadsToRunLast) > 0:
                #     thread_waiter = True
                #     while thread_waiter == True:
                #         for thread_ in threadsToRunLast:
                #             if thread_.is_alive() == False:
                #                 thread_waiter = False
                #         time.sleep(0.01)


                # def cleanup_points(collected_inputs, points_to_clear):
                #     tempData = dict(collected_inputs)
                #     if len(points_to_clear) != 0:
                #         for key_ in points_to_clear:
                #                     level, levelEntry = utility.parserEntryCoordLookup(parsedInputMap, key_)
                #                     tempData[level][levelEntry] = ""
                #     return tempData
                # parsedInput = cleanup_points(parsedInput, thread_all_points)
                #time.sleep(0.55)

            points_to_clear = []
            points_to_clear.extend(thread_all_points)
            # Remove duplicates
            points_to_clear = list(dict.fromkeys(points_to_clear))
            print("\nPoints to Clear: " + str(points_to_clear))

            output = utility.miniParserReverser(parsedInput, parsedInputMap, False, points_to_clear)


        #time.sleep(15)



        if crazyLoop == True:
            print("Uncharted Waters, be wary of infinite loops!")



        return output




    def cleanupTempArgs(self, input:list):
        space_char = " "
        blank = ''
        #print(input)
        #for i in input:
            #print(i)
        #print(" ")
        for x in range(len(input) - 1, -1, -1) :
            #print("x in range")
            #print(input[x])
            if input[x] is space_char and (input[x-1] is not space_char and input[x-1] is not blank) and x > 0:
                #print("-inner if")
                input.pop(x)
            elif(input[x] is blank):
                #print("-inner if 1 - remove blank")
                input.pop(x)
            elif (input[x] is space_char or input[x] is blank) and x < len(input) - 1:
                #print("-inner elif 2 - concatinate space")
                input[ x + 1 ] = space_char + input[ x + 1 ]
                input.pop(x)
        output = input

        return output



    def tokenSearch(self, input) -> bool:
        tokensFound = False
        parserContent = pyparsing.Word(pyparsing.alphanums) | ' '

        input = "$(%s)" % input
        parser = pyparsing.nestedExpr('$(', ')')
        results = parser.parseString(input)
        formattedResults = results.asList()

        for r in formattedResults[0]:
            if type(r) == list:
                tokensFound = True

        return tokensFound

    def hasArgzOrVars(self, input) -> bool:
        results = False

        if "#" in input:
            results = True
        if "@" in input:
            results = True
        #print(input + "\n has arg or vars: " + str(results))
        return results


    # def stringCleanup(
    #     self,
    #     input:str = "",
    #     arguments:list = []
    #     ):
    #     results = ""
    #     for i in input[0]:
    #         results = results + i + " "
    #     return input

    class FunctionCounter():
        def __init__(self) -> None:
            self.counts = {}

        def count(self, functionName):
            try:
                i = self.counts[functionName]
                self.counts[functionName] = i + 1
            except:
                self.counts[functionName] = 0

        def getCount(self, functionName):
            try:
                i = self.counts[functionName]
                return i
            except:
                self.counts[functionName] = 0
                return self.counts[functionName]



    def does_function_exist(self, function):
        try:
            function_:AbstractCommandFunction = self.loadedFunctions[function]
            if function_ is not None:
                return True
            else:
                return False
        except:
            return False

    def run_function(self, user, function, args, tokenSource):
        try:
            #self.functionCounter.count(function)

            function_:AbstractCommandFunction = self.loadedFunctions[function]
            if function_ is not None:
                function_response = function_.do_function(tokenSource, user, function, args, None)
                return function_response
        except Exception as e:
            print("Exception: ")
            print(e)
            return "{Function Error}"





if __name__ == '__main__':
    testModule = Token_Processor()
    #parsed = utility.miniParser("ROOT(testA(123))((4525)testB)(testC(2362))")
    #stringToParse = "(DOOK(testA(123))((4525)testB)(testC(2362))POOF)"
    #stringToParse = "(you rolled a ($echo ($roll #*) with) with (#0))"
    #stringToParse = "(#*) = ($math(9+9+(#*)*1+1000)) (@test) ($math($math(#*)*2+1000))"
    #stringToParse = "($if (10==($math (10)))($math (#*)))" # If Statement example
    #stringToParse = "(@test) ($math($math(#*)*2+1000))"
    #stringToParse = "(@test) ($setVar(test)(varData)) (@test)"
    #stringToParse = "test ($obsWebSocket ((SetSceneItemEnabled)({\"sourceName\":\"Color Callibration\", \"sceneItemEnabled\": true, \"sceneName\":\"Cam feed [Main] INFOBOX\"})))"
    #stringToParse = "test ($obsWebSocket ((GetVersion)({})))"
    #stringToParse = "test ($obsWebSocket (SetCurrentProgramScene)({\"sceneName\":\"Cam feed [Main] INFOBOX\"}))"
    #stringToParse = "($ttsCoreSpeak (Hello World))"
    #stringToParse = "($lights (downstairs)(red))($lights (downstairs)(blue))($lights (downstairs)(green))"
    #stringToParse = "($setScene (Cam feed [Main] INFOBOX))"
    #stringToParse = "($getAverageBitrate)"
    #stringToParse = "Pre-test ($thread ($lights (downstairs)(stream)) ($ttsCoreSpeak (This is a token processor threading test))) Post-test"
    stringToParse = "a ($math (2+2)) ($thread ($ttsCoreSpeak (this is a random number "+str(randint(111,999))+"))) ($thread (($lights(downstairs)(stream)) ($lights(downstairs)(blue))) ) a"
    #stringToParse = "($addCounter(testing)(4))"
    parsed, parseMap = utility.miniParser(stringToParse)
    parsedKeys = parsed.keys()
    parsedMapKeys = parseMap.keys()
    print("\n\n")
    for key in parsedKeys:
        print(key)
        print(parsed[key])
    print("\n\n")
    for map in parsedMapKeys:
        print(map)
        print(parseMap[map])
    print("\n\n")

    reversedString = utility.miniParserReverser(parsed, parseMap, keep_parenthesis=False)

    print("\n\n")
    print(stringToParse)
    print(reversedString)
    print("\n")
    commandName = "!test"
    commandRawInput = "%s 5+10" % (commandName)
    commandResponse = testModule.parseTokenResponse("Alex", None, commandRawInput, stringToParse, "Test_Source")
    print("\n\ncommandResponse")
    print(commandResponse)
