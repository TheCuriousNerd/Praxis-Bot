import commands.loader_functions as function_loader
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

if __name__ == "__main__":
    loadedFunctions = function_loader.load_functions(AbstractCommandFunction.FunctionType.ver0)
    print("loadedFunctions: ")
    functionList = []
    for key_ in loadedFunctions.keys():
        functionList.append(key_)
    functionList.sort()
    print(functionList)

    print("\033c") #Clear the screen first
    print("\n# Function List")
    for f in functionList:
        print("\n## Function Name: <br>&#160;&#160;&#160; $"+ type(loadedFunctions[f]).functionName)
        try:
            print("Warnings: <br>")
            for line__ in type(loadedFunctions[f]).warningText:
                print(line__ + "<br>")
        except:
            pass
        print("Description: <br>")
        for line_ in type(loadedFunctions[f]).helpText:
            print(line_ + "<br>")