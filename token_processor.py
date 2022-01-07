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

from enum import Enum, auto
import pyparsing
import shlex

from bot_functions import utilities_script as utility
from commands import loader_functions as function_loader
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

import re

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

    def new_parseTokenResponse(self, userData, userID, commandRawInput:str, command_returnString, tokenSource):
        combinedUserData = {}
        combinedUserData["userData"] = userData
        combinedUserData["userID"] = userID
        commandArguments = utility.get_args(commandRawInput)
        #This removes the command from the arguments
        commandArguments.pop(0)

    def new_stringFunctionParser(self,
            input:str = "",
            arguments:list = [],
            userData = "",
            commandRawInput = "",
            tokenSource = None
            ):
            pass

    #Commands will call this function to parse tokens in the response string.
    def parseTokenResponse(self, userData, userID, commandRawInput:str, command_returnString, tokenSource):
        combinedUserData = {}
        combinedUserData["userData"] = userData
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
        print("\ntempArgs:")
        for t in tempArg:
            print(t)

        print("\nCommand Return String:")
        print("\n" + str(command_returnString))
        response = self.stringFunctionParser(command_returnString, tempArg, combinedUserData, commandRawInput, tokenSource)
        return response

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

    def searchPrep(self, input):
        parserContent = pyparsing.Word(pyparsing.alphanums) | ' '

        #pyparsing.ParserElement.leaveWhitespace()
        input = "$(%s)" % input
        input = input.replace(" ", " ")
        parser:pyparsing.Forward = pyparsing.nested_expr('$(', ')')
        print(str(input))
        print(str(type(parser)))
        #parser.ignore_whitespace(True)
        #parser.setDefaultWhitespaceChars("")
        #results = parser.parse_string(input, parseAll=True)

        results = parser.parse_string(input)
        formattedResults = results.asList()
        print(str(formattedResults))

        def resetWhiteSpace(parsedResults):
            for listEntry in parsedResults:
                if type(listEntry) == list:
                    resetWhiteSpace(listEntry)
                else:
                    listEntry = listEntry.replace(" ", " ")
        resetWhiteSpace(formattedResults)
        print(str(formattedResults))
        return formattedResults

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


    def stringCleanup(
        self,
        input:str = "",
        arguments:list = []
        ):
        results = ""
        for i in input[0]:
            results = results + i + " "
        return input

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

    def stringFunctionParser(self,
            input:str = "",
            arguments:list = [],
            userData = "",
            commandRawInput = "",
            tokenSource = None
            ):
        print("\nString Parsing Initiated, input includes:")
        print("\n" + str (input))
        output = None
        results = self.searchPrep(input)
        data_struct = results
        rawReturnString = input
        print("\nString Testing Initiating, Results include:")
        print("\n" + str(results))

        #print("\nv0 test:")
        for result in results[0]:
            if type(result) == list:
                print("\n{Token FOUND}:")
                print(result)
                print(len(result))

                def processLoop(data_tree, input):
                    print("\nLOOP TIME")
                    print(input)
                    global currentString
                    currentString = input
                    NoArgzNoVars = self.hasArgzOrVars(input)
                    for entry in data_tree[0]:
                        inputData_ = entry
                        if len(inputData_) == 1:
                            #print(str(inputData_) + " is a token")
                            for data in inputData_:

                                if type(data) == list:
                                    print(str(data) + " is a list")
                                    processLoop(data, currentString)

                                elif type(data) == str:
                                    #print(data + " is a str")

                                    if "#" in data:
                                        selectedToken = TokenType.ARGUMENT
                                        currentString = self.processToken(currentString, data, arguments, selectedToken, userData, commandRawInput, rawReturnString, tokenSource)
                                        print("\nCURRENT STRING UPDATED:" + currentString)
                                    elif "@" in data:
                                        selectedToken = TokenType.VARIABLE
                                        currentString = self.processToken(currentString, data, arguments, selectedToken, userData, commandRawInput, rawReturnString, tokenSource)
                                        #print(currentString)
                                    else:
                                        selectedToken = TokenType.FUNCTION
                                        # Only run the following once the Arguments and Variables are parsed
                                        NoArgzNoVars = self.hasArgzOrVars(input)
                                        if NoArgzNoVars == False:
                                            print("FUNCTION Time" + str(inputData_))
                                            currentString = self.processToken(currentString, inputData_[0], arguments, selectedToken, userData, commandRawInput, rawReturnString, tokenSource)
                                            #print(currentString)
                                            break
                                else:
                                    print(str(data) + " is something else")
                        elif len(inputData_) > 1:
                            pass
                        elif type(inputData_[0]) == str:
                            print(inputData_ + " is a edge case str__")
                            print("EDGE CASE?! -DEBUG TO STUDY MORE")

                            if "#" in inputData_:
                                selectedToken = TokenType.ARGUMENT
                                #print(self.processToken(inputData_, arguments, selectedToken))
                            elif "@" in inputData_:
                                selectedToken = TokenType.VARIABLE
                                #print(self.processToken(inputData_, arguments, selectedToken))
                            else:
                                selectedToken = TokenType.FUNCTION
                                #print(self.processToken(inputData_, arguments, selectedToken))

                        else:
                            print(inputData_ + " is something else__")
                    return currentString

                output = processLoop(data_struct, input)
                #print(self.tokenSearch(output))
                if self.tokenSearch(output):
                    print("\n-----------------\nLoop Part 2\n-----------------\n")
                    results2 = self.searchPrep(output)
                    print("\n Loop2 New Result:" + str(results2))
                    print("\n Loop2 New Output:" + str(output))
                    for newResult in results2[0]:

                        if type(newResult) == list:
                            print("\n{Token FOUND}:")
                            print(newResult)
                            output = processLoop(newResult, output)

                print("\n-----------------\nLoop Part 3 TEST\n-----------------\n")
                print(output)
                hasTokens = self.tokenSearch(output)
                print("Has Tokens " + str(hasTokens))
                while hasTokens:
                    print("\n-----------------\nLoop Part 3\n-----------------\n")
                    results3 = self.searchPrep(output)
                    print(results3)
                    for newResult in results3[0]:

                        if type(newResult) == list:
                            print("\n{Token FOUND}:")
                            print(newResult)
                            output = processLoop(newResult, output)
                            hasTokens = False

        print("\n-----------------\nPOST LOOPS\n-----------------\n")
        return output


    def processToken(self, input:str, data, arguments, targetToken, userData, commandRawInput, rawReturnString, tokenSource):
        returnString = input
        #print("running a thing!")
        #print(str(data) + " is about to run!\n")

        #print(input)
        #print(data)
        #print(arguments)
        #print(targetToken)
        #print(" ")


        def handleInput_Argument(index, arg, returnString:str):
            token1 = "$(#" + str(index) + ")"
            token2 = "#" + str(index)
            returnString = returnString.replace(token1, arg)
            returnString = returnString.replace(token2, arg)
            return returnString

        def handleInput_Variable():
            pass

        def handleInput_Function(functionName, arg, returnString:str):
            print("\nAbout to run function:")
            print(functionName)
            print(arg)
            print(returnString)

            def prepStringReplacement(
                searchString_Prefix = "$(",
                searchString_Suffix = ")",
                newString = ""
                ):
                searchString = searchString_Prefix + functionName + " "

                # tempArg = re.split("( )", commandRawInput)
                # tempArg.pop(0)
                # tempArg.pop(0)
                # tempArg = self.cleanupTempArgs(tempArg)


                def predictSearchString(functionName):
                    rePattern = "(?<=\$\(%s)(.*?)(?=\))" % (functionName)
                    print("About to predict...")
                    print(rePattern)
                    print(returnString)
                    reSearch = re.search(rePattern, returnString)
                    print(reSearch.group(0))
                    if reSearch is not None:

                        reResults = "$(%s%s)" % (functionName, reSearch.group(0))
                        name_ = "$(%s " % functionName
                        print(name_)
                        if name_ in reSearch.group(0):
                            print("name found!")
                            reResults = reResults.replace(name_, "", 1)

                        print("reResults:")
                        print(reResults)
                        return reResults
                    else:
                        return searchString


                #for a in tempArg:
                #    if searchString + a in returnString:
                #        searchString = searchString + a + " "

                #searchString = searchString[:-1]
                #searchString = searchString + searchString_Suffix

                searchString = predictSearchString(functionName)
                #print("\ntempArg:")
                #print(tempArg)
                # print("rawReturnString:")
                # print(rawReturnString)
                # print("searchString:")
                # print(searchString)
                # print("newString:")
                # print(newString)
                # print("returnString:")
                # print(returnString)
                # print("\n")
                #modifiedString = returnString.replace(searchString, newString)
                return searchString , newString

            def updateReturnString(oldString, newString):
                return returnString.replace(oldString, newString)

            if functionName == "testerino":
                computedResult = ""
                for a in arg:
                    if a is not arg[0]:
                        computedResult = computedResult + a + " "
                computedResult = computedResult[:-1]
                returnString = prepStringReplacement(newString = computedResult)

            #return str(self.loadedFunctions[functionName])
            if self.does_function_exist(functionName):
                rePattern_arg = "(?<=\$\(%s)(.*?)(?=\))" % (functionName)
                reSearch_arg = re.search(rePattern_arg, returnString)
                try:
                    reResults_arg = reSearch_arg.group(0)
                    reResultsPrepped_arg = re.split("( )", reResults_arg)
                    reResults_formated = self.cleanupTempArgs(reResultsPrepped_arg)
                    # This removes first char of first element in list
                    reResults_formated[0] = reResults_formated[0][1:]

                    reResults_formated_temp_ = reResults_formated
                    if '$(%s' % functionName in reResults_formated:
                        reResults_formated_temp_ = reResults_formated
                        reResults_formated_temp_.remove('$(%s' % functionName)

                    print("\nRunning Function...")
                    print(functionName)
                    print(reResults_formated_temp_)

                    functionResults = self.run_function(userData, functionName, reResults_formated_temp_, tokenSource)
                    print("\nFunction Results:")
                    print(functionResults)
                    oldString, newString = prepStringReplacement(newString = str(functionResults))
                    returnString = updateReturnString(oldString, newString)
                    print("\nnew returnString:")
                    print(returnString)
                except:
                    returnString = returnString

            return returnString


        if targetToken == TokenType.ARGUMENT:
            print("\n{RUNNING a ARGUMENT}")
            if "$(#*)" in returnString:
                args = ""

                tempArg = re.split("( )", commandRawInput)
                tempArg.pop(0)
                try:
                    tempArg.pop(0)
                except:
                    pass
                tempArg = self.cleanupTempArgs(tempArg)

                #skipFirst = True
                for args_ in tempArg:
                    args = args + args_ + " "
                args = args[:-1]

                if args != "":
                    returnString = handleInput_Argument("*", args, returnString)
            argIndex = 0
            for argz in arguments:
                #print(" ")
                returnString = handleInput_Argument(argIndex, argz, returnString)
                argIndex = argIndex + 1
        elif targetToken == TokenType.VARIABLE:
            print("\n{RUNNING a VARIABLE}")
        elif targetToken == TokenType.FUNCTION:
            print("\n{RUNNING a FUNCTION}")
            returnString = handleInput_Function(data, arguments, returnString)

        return returnString

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
                self.functionCounter.count(function)

                function_:AbstractCommandFunction = self.loadedFunctions[function]
                if function_ is not None:
                    function_response = function_.do_function(tokenSource, user, function, args, None)
                    return function_response
            except:
                return "{Function Error}"


def lookupCommandResponse(input):
    response = ""
    if input == "!test":
        response = "A Testerino is Detected $(testFunction $(#*)) $(testFunction $(#0) $(math $(#*)))"
        return response
    if input == "!math":
        response = "$(#*) = $(math $(math $(#*) + $(#*)) + $(#*) + 2)"
        return response
    if input == "!math2":
        response = "$(#*) = $(math $(#*))"
        return response
    if input == "!math3":
        response = "$(#*)=$(math $(math $(math $(math $(#*)) +2)) +2)"
        return response
    if input == "!test2":
        response = "$(testFunction $(#0) $(testFunction $(#*))) :: $(testFunction $(#0) $(testFunction $(#*))) :: $(math $(#*))"
        return response
    if input == "!date":
        response = "The current date and time is: $(datetime %Y-%m-%d)"
        return response

    return response

if __name__ == '__main__':
    #parsed = utility.miniParser("ROOT(testA(123))((4525)testB)(testC(2362))")
    #stringToParse = "(DOOK(testA(123))((4525)testB)(testC(2362))POOF)"
    stringToParse = "(you rolled a ($echo ($roll #*)) with (#0))"
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

    reversedString = utility.miniParserReverser(parsed, parseMap)

    print("\n\n")
    print(stringToParse)
    print(reversedString)
    print("\n\n")


if __name__ == '__dfdfmain__':
    testModule = Token_Processor()

    commandName = "!math3"
    commandRawInput = "%s 3+3" % (commandName)
    #commandRawInput2 = "!testerino GG    "
    commandResponse = lookupCommandResponse(commandName)

    testModule.setup()
    print("\n")
    testResponse = testModule.parseTokenResponse("TestUser", None, commandRawInput, commandResponse, None)
    print("\ncommandRaw:\n" + commandRawInput)
    print("\ncommandReponse:\n" + commandResponse)
    print("\nresult:\n" + str(testResponse) + "\n")
    # testResponse = testModule.parseTokenResponse("TestUser", commandRawInput2, commandResponse)
    # print("\ncommandRaw:\n" + commandRawInput)
    # print("\ncommandReponse:\n" + commandReponse)
    # print("\nresult:\n" + testResponse + "\n")
    # testResponse = testModule.parseTokenResponse("TestUser", commandRawInput, commandReponse)
    # print("\ncommandRaw:\n" + commandRawInput2)
    # print("\ncommandReponse:\n" + commandReponse)
    # print("\nresult:\n" + testResponse + "\n")