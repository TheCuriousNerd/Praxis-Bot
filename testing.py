
from commands.command_functions import Abstract_Function_Helpers
from sqlalchemy.engine.row import LegacyRow
from sqlalchemy.engine.cursor import LegacyCursorResult

import importlib

def main():
    obj = Abstract_Function_Helpers()
    print("\n")
    print(obj.get_command("!math"))
    print("\n")
    print(type(obj.get_command("!math")))
    print("\n")
    result:LegacyCursorResult = obj.get_command("!math")

    #for r in result:
    for key in result.keys():
        print(key)
        print(result.__getattribute__(key))
    #print(obj.update_lastUsed("!math"))



if __name__ == "__main__":
    main()
    # (source, username, userID, command, rest, bonusData)
    #result = standalone_command.handle_command("testSpace", "Alex", "", "!math", "2+2", "")
    #print(result)