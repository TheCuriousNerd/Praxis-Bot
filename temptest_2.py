from enum import Enum, auto
import pyparsing

class TokenType(Enum):
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

    def replace_Arguments(input:str):
        return processString(input, TokenType.ARGUMENT)
    def replace_Variables(input:str):
        return processString(input, TokenType.VARIABLE)
    def run_Functions(input:str):
        return processString(input, TokenType.FUNCTION)

    curStr = replace_Arguments(curStr)
    #print(curStr)
    curStr = replace_Variables(curStr)
    #print(curStr)
    curStr = run_Functions(curStr)
    #print(curStr)

    return curStr

def stringCleanup(input):
    results = ""
    for i in input[0]:
        results = results + i + " "
    return input

def processString(input, tokenType):
    results = new_Search(input, tokenType)
    print(results)
    for result in results[0]:
        if type(result) == list:
            print("LIST FOUND:")
            print(result)
        else:
            print(result)

    def processor(p_Input):
        if tokenType == TokenType.ARGUMENT:
            pass
        elif tokenType == TokenType.FUNCTION:
            pass
        elif tokenType == TokenType.VARIABLE:
            pass

    return input

def new_Search(input, tokenType):
    parserContent = pyparsing.Word(pyparsing.alphanums) | ' '

    if tokenType == TokenType.ARGUMENT:
        input = "$(%s)" % input
        parser = pyparsing.nestedExpr('$(', ')')
        results = parser.parseString(input)
        formattedResults = results.asList()
        print("Arguments Search:")
        return formattedResults
    elif tokenType == TokenType.FUNCTION:
        input = "$(%s)" % input
        parser = pyparsing.nestedExpr('$(', ')')
        results = parser.parseString(input)
        formattedResults = results.asList()
        print("Functions Search:")
        return formattedResults
    elif tokenType == TokenType.VARIABLE:
        input = "$(%s)" % input
        parser = pyparsing.nestedExpr('$(', ')')
        results = parser.parseString(input)
        formattedResults = results.asList()
        print("Variables Search:")
        return formattedResults


def test_function(input):
    result = "TestResult_" + input + input
    return result

def test_function2(input):
    result = "TestResult $(TF) " + input + " " + input
    return result

def searchForFunctions1(input):
        #print(input)
        input = "$(%s)" % input
        parserContent = pyparsing.Word(pyparsing.alphanums) | ' '
        parser = pyparsing.nestedExpr('$(', ')')
        testResult_ = parser.parseString(input)
        #print(testResult_)
        testResult = testResult_.asList()

        #result1 = ("functionName", input, False)
        #result2 = ("functionName2", ("functionName3", input, False, None), True)
        #results = []
        return testResult

if __name__ == '__main__':
    init()