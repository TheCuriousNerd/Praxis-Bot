import pyparsing

def init():
    stringToTest = "This is a $(testFunction) $(testFunction #(0)) command @(user)"
    #stringToTest = "$(test$(test$(test)))$(test)$(test)"
    print(searchForFunctions1(stringToTest))

    print(stringFunctionParser(stringToTest))

def stringFunctionParser(
        input:str = "",
        arguments:list = []
        ):
    curStr = input

    def replace_Arguments(input:str):
        return input
    def replace_Variables(input:str):
        return input
    def run_Functions(input:str):
        return input

    curStr = replace_Arguments(curStr)
    curStr = replace_Variables(curStr)
    curStr = run_Functions(curStr)

    return curStr


def test_function(input):
    result = "TestResult_" + input + input
    return result

def test_function2(input):
    result = "TestResult $(TF) " + input + " " + input
    return result

def searchForFunctions1(input):
        input = "$(%s)" % input
        parserContent = pyparsing.Word(pyparsing.alphanums) | ' '
        parser = pyparsing.nestedExpr('$(', ')')
        testResult_ = parser.parseString(input)
        testResult = testResult_.asList()

        #result1 = ("functionName", input, False)
        #result2 = ("functionName2", ("functionName3", input, False, None), True)
        #results = []
        return testResult

if __name__ == '__main__':
    init()