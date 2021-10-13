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

from bot_functions import utilities_script as utility
from commands.command_functions import AbstractCommandFunction, Function_Helpers

class TokenType(Enum):
    NONE = auto()
    ARGUMENT = auto()
    FUNCTION = auto()
    VARIABLE = auto()

class Token_Processor():
    def __init__(self):
        super().__init__(
        )
        self.loadedFunctions = None

    def setup(self):
        pass

    #Commands will call this function to parse tokens in the response string.
    def parseTokenResponse(self, userData, commandRawInput, command_returnString):
        commandArguments = utility.get_args(commandRawInput)
        #This removes the command from the arguments
        commandArguments.pop(0)
        response = self.stringFunctionParser(command_returnString, commandArguments, userData)
        return response


    def searchPrep(self, input):
        parserContent = pyparsing.Word(pyparsing.alphanums) | ' '

        input = "$(%s)" % input
        parser = pyparsing.nestedExpr('$(', ')')
        results = parser.parseString(input)
        formattedResults = results.asList()

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

    def stringFunctionParser(self,
            input:str = "",
            arguments:list = [],
            userData = ""
            ):
        output = None
        results = self.searchPrep(input)

        #print("\nv0 test:")
        for result in results[0]:
            if type(result) == list:
                #print("\n{Token FOUND}:")
                #print(result)
                #print(len(result))

                def processLoop(inputData_, input):
                    #print("LOOP TIME")
                    #print(inputData_)
                    #print(input)
                    global currentString
                    currentString = input
                    NoArgzNoVars = self.hasArgzOrVars(input)
                    if type(inputData_) == list:
                        #print(str(inputData_) + " is a token")
                        for data in inputData_:

                            if type(data) == list:
                                #print(str(data) + " is a list")
                                processLoop(data, currentString)

                            elif type(data) == str:
                                #print(data + " is a str")

                                if "#" in data:
                                    selectedToken = TokenType.ARGUMENT
                                    currentString = self.processToken(currentString, data, arguments, selectedToken, userData)
                                    #print(currentString)
                                elif "@" in data:
                                    selectedToken = TokenType.VARIABLE
                                    currentString = self.processToken(currentString, data, arguments, selectedToken, userData)
                                    #print(currentString)
                                else:
                                    selectedToken = TokenType.FUNCTION
                                    # Only run the following once the Arguments and Variables are parsed
                                    NoArgzNoVars = self.hasArgzOrVars(input)
                                    if NoArgzNoVars == False:
                                        #print("FUNCTION Time" + str(inputData_))
                                        currentString = self.processToken(currentString, inputData_[0], inputData_, selectedToken, userData)
                                        #print(currentString)
                                        break
                            else:
                                print(str(data) + " is something else")


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

                output = processLoop(result, input)
                #print(self.tokenSearch(output))
                if self.tokenSearch(output):
                    #print("\n-----------------\nLoop Part 2\n-----------------\n")
                    results2 = self.searchPrep(output)
                    #print(results2)
                    for newResult in results2[0]:

                        if type(newResult) == list:
                            #print("\n{Token FOUND}:")
                            #print(newResult)
                            output = processLoop(newResult, output)

        return output


    def processToken(self, input:str, data, arguments, targetToken, userData):
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

            def modifyReturnString(
                searchString_Prefix = "$(",
                searchString_Suffix = ")",
                newString = ""
                ):
                searchString = searchString_Prefix
                for a in arg:
                    searchString = searchString + a + " "
                searchString = searchString[:-1]
                searchString = searchString + searchString_Suffix
                modifiedString = returnString.replace(searchString, newString)
                return modifiedString

            if functionName == "testerino":
                computedResult = ""
                for a in arg:
                    if a is not arg[0]:
                        computedResult = computedResult + a + " "
                computedResult = computedResult[:-1]
                returnString = modifyReturnString(newString = computedResult)

            if self.does_function_exist(functionName):
                functionResults = self.run_function(userData, functionName, arg)
                returnString = modifyReturnString(newString = functionResults)

            return returnString


        if targetToken == TokenType.ARGUMENT:
            print("{RUNNING a ARGUMENT}")
            if "$(#*)" in returnString:
                args = ""
                for args_ in arguments:
                    args = args + args_ + " "
                args = args[:-1]
                returnString = handleInput_Argument("*", args, returnString)
            argIndex = 0
            for argz in arguments:
                #print(" ")
                returnString = handleInput_Argument(argIndex, argz, returnString)
                argIndex = argIndex + 1
        elif targetToken == TokenType.VARIABLE:
            print("{RUNNING a VARIABLE}")
        elif targetToken == TokenType.FUNCTION:
            print("{RUNNING a FUNCTION}")
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

    def run_function(self, user, function, args):
            try:
                function_:AbstractCommandFunction = self.loadedFunctions[function]
                if function_ is not None:
                    function_response = function_.do_function(user, function, args, None)
                    return function_response
            except:
                return "{Function Error}"


def lookupCommandResponse(input):
    response = ""
    if input == "!testerino":
        response = "A Testerino is Detected $(testerino $(#0) $(#1) $(#*))"
    return response


if __name__ == '__main__':
    testModule = Token_Processor()

    commandName = "!testerino"
    commandRawInput = "!testerino MODULE_TEST ABC123 XYZ"
    commandReponse = lookupCommandResponse(commandName)

    testModule.setup()
    testResponse = testModule.parseTokenResponse("TestUser", commandRawInput, commandReponse)
    print("\ncommandRaw:\n" + commandRawInput)
    print("\ncommandReponse:\n" + commandReponse)
    print("\nresult:\n" + testResponse + "\n")