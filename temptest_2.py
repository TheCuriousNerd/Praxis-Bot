from enum import Enum, auto
import pyparsing

class TokenType(Enum):
    NONE = auto()
    ARGUMENT = auto()
    FUNCTION = auto()
    VARIABLE = auto()

def init():
    stringToTest = "This is a $(testFunction) $(testFunction $(#0)) command $(@user)"
    #stringToTest = "This is a $(testFunction1 $(testFunction2 $(testFunction3 $(testFunction4)))) test for nested functions"
    #stringToTest = "This is a $(testFunction 1) $(12345 $(abcdef 123 #4 5 6)) $(123abc $(123123123123)) $(testFunction $(#0)) command $(@user)"
    argzToTest = ["UBER_TESTERINO"]
    test2 = "This is a $(testerino $(#0))"


    #result = stringFunctionParser(stringToTest)
    result2 = stringFunctionParser(test2, argzToTest)



def stringFunctionParser(
        input:str = "",
        arguments:list = []
        ):
    curStr = input

    print("Before:")
    print(input)

    curStr = processString(input, arguments)

    print("\nAfter:")
    print(curStr)
    print("-----------------------------")

    return curStr

def stringCleanup(
        input:str = "",
        arguments:list = []
        ):
    results = ""
    for i in input[0]:
        results = results + i + " "
    return input

def processString(
        input:str = "",
        arguments:list = []
        ):
    results = searchPrep(input)
    print(results)

    print("\nv0 test:")
    for result in results[0]:
        if type(result) == list:
            print("\n{Token FOUND}:")
            print(result)
            #print(len(result))

            def processLoop(inputData_, input):
                global currentString
                currentString = input
                if type(inputData_) == list:
                    print(str(inputData_) + " is a token")
                    for data in inputData_:

                        if type(data) == list:
                            print(str(data) + " is a list")
                            processLoop(data, currentString)

                        elif type(data) == str:
                            print(data + " is a str")

                            if "#" in data:
                                selectedToken = TokenType.ARGUMENT
                                currentString = processToken(currentString, data, arguments, selectedToken)
                                print(currentString)
                            elif "@" in data:
                                selectedToken = TokenType.VARIABLE
                                currentString = processToken(currentString, data, arguments, selectedToken)
                                print(currentString)
                            else:
                                selectedToken = TokenType.FUNCTION
                                currentString = processToken(currentString, data, arguments, selectedToken)
                                print(currentString)
                        else:
                            print(str(data) + " is something else")


                elif type(inputData_[0]) == str:
                    print(inputData_ + " is a edge case str__")
                    print("EDGE CASE?! -DEBUG TO STUDY MORE")

                    if "#" in inputData_:
                        selectedToken = TokenType.ARGUMENT
                        print(processToken(inputData_, arguments, selectedToken))
                    elif "@" in inputData_:
                        selectedToken = TokenType.VARIABLE
                        print(processToken(inputData_, arguments, selectedToken))
                    else:
                        selectedToken = TokenType.FUNCTION
                        print(processToken(inputData_, arguments, selectedToken))

                else:
                    print(inputData_ + " is something else__")
                return currentString

            output = processLoop(result, input)

    return output

def processToken(input:str, data, arguments, targetToken):
    returnString = input
    print("running a thing!")
    print(str(data) + " is about to run!")

    #print(input)
    #print(data)
    #print(arguments)
    #print(targetToken)


    def handleInput_Argument(index, arg, returnString:str):
        token1 = "$(#" + str(index) + ")"
        token2 = "#" + str(index)
        returnString = returnString.replace(token1, arg)
        returnString = returnString.replace(token2, arg)
        return returnString

    def handleInput_Variable():
        pass

    def handleInput_Function():
        pass


    if targetToken == TokenType.ARGUMENT:
        print("{RUNNING a ARGUMENT}")
        argIndex = 0
        for argz in arguments:
            print(argz)
            print(" ")
            returnString = handleInput_Argument(argIndex, argz, returnString)
            argIndex = argIndex + 1
    elif targetToken == TokenType.VARIABLE:
        print("{RUNNING a VARIABLE}")
    elif targetToken == TokenType.FUNCTION:
        print("{RUNNING a FUNCTION}")
        if data == "testerino":
            pass
            #return "test 123abc\n"

    return returnString

def searchPrep(input):
    parserContent = pyparsing.Word(pyparsing.alphanums) | ' '

    input = "$(%s)" % input
    parser = pyparsing.nestedExpr('$(', ')')
    results = parser.parseString(input)
    formattedResults = results.asList()

    return formattedResults


if __name__ == '__main__':
    init()