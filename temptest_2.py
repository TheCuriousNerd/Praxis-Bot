from enum import Enum, auto
import pyparsing

class TokenType(Enum):
    NONE = auto()
    ARGUMENT = auto()
    FUNCTION = auto()
    VARIABLE = auto()

def init():
    stringToTest = "This is a $(testFunction) $(testFunction $(#0)) command $(@user)"

    print("Before:")
    print(stringToTest)
    result = stringFunctionParser(stringToTest)
    print("After:")
    print(result)


def stringFunctionParser(
        input:str = "",
        arguments:list = []
        ):
    curStr = input

    curStr = processString(input, arguments)

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

    print("cur test:")
    for results in results[0]:
        if type(results) == list:
            print("{Token FOUND}:")
            print(results)
            print(len(results))

            if len(results) > 1:
                for r in results:
                    selectedToken = TokenType.NONE
                    if "#" in r[0]:
                        selectedToken = TokenType.ARGUMENT
                        print(processToken(r[0], arguments, selectedToken))
                    elif "@" in r[0]:
                        selectedToken = TokenType.VARIABLE
                        print(processToken(r[0], arguments, selectedToken))
                    else:
                        selectedToken = TokenType.FUNCTION
                        print(processToken(r, arguments, selectedToken))
            else:
                selectedToken = TokenType.NONE
                if "#" in results[0]:
                    selectedToken = TokenType.ARGUMENT
                    print(processToken(results[0], arguments, selectedToken))
                elif "@" in results[0]:
                    selectedToken = TokenType.VARIABLE
                    print(processToken(results[0], arguments, selectedToken))
                else:
                    selectedToken = TokenType.FUNCTION
                    print(processToken(results[0], arguments, selectedToken))


    return input

def processToken(input, arguments, targetToken):
    returnString = ""
    print(input)
    if targetToken == TokenType.ARGUMENT:
        print("{FOUND a ARGUMENT}")
    elif targetToken == TokenType.VARIABLE:
        print("{FOUND a VARIABLE}")
    elif targetToken == TokenType.FUNCTION:
        print("{FOUND a FUNCTION}")
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