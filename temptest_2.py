from enum import Enum, auto
import pyparsing

from bot_functions import utilities_script as utility


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

    def loadFunctions(self):
        pass

    def parseTokenResponse(self, commandRawInput, commandReponse):
        commandArguments = utility.get_args(commandRawInput)
        #This removes the command from the arguments
        commandArguments.pop(0)
        response = self.stringFunctionParser(commandReponse, commandArguments)
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

    #Remove this later
    def stringFunctionParser(self,
        input:str = "",
        arguments:list = []
        ):
        curStr = input
        curStr = self.processString(input, arguments)
        return curStr
    #========

    def stringCleanup(
        self,
        input:str = "",
        arguments:list = []
        ):
        results = ""
        for i in input[0]:
            results = results + i + " "
        return input

    def processString(self,
            input:str = "",
            arguments:list = []
            ):
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
                                    currentString = self.processToken(currentString, data, arguments, selectedToken)
                                    #print(currentString)
                                elif "@" in data:
                                    selectedToken = TokenType.VARIABLE
                                    currentString = self.processToken(currentString, data, arguments, selectedToken)
                                    #print(currentString)
                                else:
                                    selectedToken = TokenType.FUNCTION
                                    # Only run the following once the Arguments and Variables are parsed
                                    NoArgzNoVars = self.hasArgzOrVars(input)
                                    if NoArgzNoVars == False:
                                        #print("FUNCTION Time" + str(inputData_))
                                        currentString = self.processToken(currentString, inputData_[0], inputData_, selectedToken)
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


    def processToken(self, input:str, data, arguments, targetToken):
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
            #print("testFunction:")
            #print(str(arg))
            #print(returnString)
            if functionName == "testerino":
                #print("-testerino- Detected")
                searchString = "$("
                computedResult = ""
                for a in arg:
                    if a is not arg[0]:
                        computedResult = computedResult + a + " "
                    searchString = searchString + a + " "

                searchString = searchString[:-1]
                searchString = searchString + ")"
                #print(searchString)
                #print(computedResult)
                computedResult = computedResult[:-1]
                returnString = returnString.replace(searchString, computedResult)

            return returnString


        if targetToken == TokenType.ARGUMENT:
            print("{RUNNING a ARGUMENT}")
            argIndex = 0
            for argz in arguments:
                #print(argz)
                #print(" ")
                returnString = handleInput_Argument(argIndex, argz, returnString)
                argIndex = argIndex + 1
        elif targetToken == TokenType.VARIABLE:
            print("{RUNNING a VARIABLE}")
        elif targetToken == TokenType.FUNCTION:
            print("{RUNNING a FUNCTION}")
            returnString = handleInput_Function(data, arguments, returnString)

        return returnString





def lookupCommandReponse(input):
    response = ""
    if input == "!testerino":
        response = "A Testerino is Detected $(testerino $(#0))"
    return response


if __name__ == '__main__':
    testModule = Token_Processor()

    commandName = "!testerino"
    commandRawInput = "!testerino MODULE_TEST"
    commandReponse = lookupCommandReponse(commandName)

    testModule.setup()
    testResponse = testModule.parseTokenResponse(commandRawInput, commandReponse)
    print("\ncommandRaw:\n" + commandRawInput)
    print("\ncommandReponse:\n" + commandReponse)
    print("\nresult:\n" + testResponse + "\n")