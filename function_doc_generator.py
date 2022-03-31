import commands.loader_functions as function_loader
from commands.command_functions import AbstractCommandFunction, Abstract_Function_Helpers

if __name__ == "__main__":
    loadedFunctions = function_loader.load_functions(AbstractCommandFunction.FunctionType.ver0)
    print("loadedFunctions: ")
    functionList = []
    for key_ in loadedFunctions.keys():
        functionList.append(key_)
    functionList.sort()

    print("\033c") #Clear the screen first
    print("\n# Function List")
    for f in functionList:
        print("\n## Function Name: $"+ type(loadedFunctions[f]).functionName)
        print("### Description: ")
        for line_ in type(loadedFunctions[f]).helpText:
            print(line_)