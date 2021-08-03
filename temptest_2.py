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

    print("Before:")
    print(stringToTest)
    result = stringFunctionParser(stringToTest)
    print("\nAfter:")
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
    for result in results[0]:
        if type(result) == list:
            print("\n{Token FOUND}:")
            print(result)
            #print(len(result))


            # def processLoop(inputData):
            #     for iD in inputData:
            #         if type(iD) == list:
            #             if len(inputData) > 1:
            #                 for r in inputData:
            #                     if type(r) == list:
            #                         print("list found")
            #                         #print(r)
            #                         processLoop(r)
            #                     selectedToken = TokenType.NONE
            #                     if "#" in r[0]:
            #                         selectedToken = TokenType.ARGUMENT
            #                         print(processToken(r[0], arguments, selectedToken))
            #                     elif "@" in r[0]:
            #                         selectedToken = TokenType.VARIABLE
            #                         print(processToken(r[0], arguments, selectedToken))
            #                     else:
            #                         selectedToken = TokenType.FUNCTION
            #                         print(processToken(r, arguments, selectedToken))
            #             else:
            #                 selectedToken = TokenType.NONE
            #                 if "#" in iD[0]:
            #                     selectedToken = TokenType.ARGUMENT
            #                     print(processToken(iD[0], arguments, selectedToken))
            #                 elif "@" in iD[0]:
            #                     selectedToken = TokenType.VARIABLE
            #                     print(processToken(iD[0], arguments, selectedToken))
            #                 else:
            #                     selectedToken = TokenType.FUNCTION
            #                     print(processToken(iD[0], arguments, selectedToken))
            #         elif type(iD) == str:
            #             print(iD + " is a str")
            #         else:
            #             print(iD + " is not a list")
            #     return inputData

            #output = processLoop(result)

            def processLoop(inputData_):
                if type(inputData_) == list:
                    print(str(inputData_) + " is a list__")
                    for data in inputData_:

                        if type(data) == list:
                            print(str(data) + " is a list")
                            processLoop(data)

                        elif type(data) == str:
                            print(data + " is a str")

                            if "#" in data:
                                selectedToken = TokenType.ARGUMENT
                                print(processToken(data, arguments, selectedToken))
                            elif "@" in data:
                                selectedToken = TokenType.VARIABLE
                                print(processToken(data, arguments, selectedToken))
                            else:
                                selectedToken = TokenType.FUNCTION
                                print(processToken(data, arguments, selectedToken))
                        else:
                            print(str(data) + " is something else")


                elif (len(inputData_) == 1) and (type(inputData_[0]) == str):
                    print(inputData_ + " is a str__")
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

            output = processLoop(result)

            # if len(results) > 1:
            #     for r in results:
            #         selectedToken = TokenType.NONE
            #         if "#" in r[0]:
            #             selectedToken = TokenType.ARGUMENT
            #             print(processToken(r[0], arguments, selectedToken))
            #         elif "@" in r[0]:
            #             selectedToken = TokenType.VARIABLE
            #             print(processToken(r[0], arguments, selectedToken))
            #         else:
            #             selectedToken = TokenType.FUNCTION
            #             print(processToken(r, arguments, selectedToken))
            # else:
            #     selectedToken = TokenType.NONE
            #     if "#" in results[0]:
            #         selectedToken = TokenType.ARGUMENT
            #         print(processToken(results[0], arguments, selectedToken))
            #     elif "@" in results[0]:
            #         selectedToken = TokenType.VARIABLE
            #         print(processToken(results[0], arguments, selectedToken))
            #     else:
            #         selectedToken = TokenType.FUNCTION
            #         print(processToken(results[0], arguments, selectedToken))
        #else:
            #print(result)


    return input

def processToken(input, arguments, targetToken):
    returnString = ""
    print("running a thing!")
    print(str(input) + " is about to run!")
    if targetToken == TokenType.ARGUMENT:
        print("{RUNNING a ARGUMENT}")
    elif targetToken == TokenType.VARIABLE:
        print("{RUNNING a VARIABLE}")
    elif targetToken == TokenType.FUNCTION:
        print("{RUNNING a FUNCTION}")
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