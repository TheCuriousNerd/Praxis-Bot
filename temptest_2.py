import pyparsing

def init():
    stringToTest = "This is a $(test) command @(user)"
    print(searchForFunctions1(stringToTest))
    #print(searchForFunctions2(stringToTest))

def searchForFunctions1(input):
        parserContent = pyparsing.Word(pyparsing.alphanums)
        parser = pyparsing.nestedExpr('$(', ')')
        testResult_ = parser.parseString(input)
        testResult = testResult_.asList()

        #result1 = ("functionName", input, False)
        #result2 = ("functionName2", ("functionName3", input, False, None), True)
        #results = []
        return testResult

def searchForFunctions2(input):
        parserContent = pyparsing.Word(pyparsing.alphanums)
        parser = pyparsing.nestedExpr('@(', ')')
        testResult_ = parser.parseString(input)
        testResult = testResult_.asList()

        #result1 = ("functionName", input, False)
        #result2 = ("functionName2", ("functionName3", input, False, None), True)
        #results = []
        return testResult

if __name__ == '__main__':
    init()