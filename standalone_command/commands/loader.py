# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

# Authors:
#   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
#       Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd
#   Virgil / hocestpotest@gmail.com
#       Github: hoc-est-potest

# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import importlib
import importlib.util
import inspect
import os
import sys
from typing import Dict

from ..commands.command_base import AbstractCommand


#New
def load_commands(commandType: AbstractCommand.CommandType) -> Dict[str, AbstractCommand]:
    print(" -Loading ", commandType ," Commands...\n")
    commands = compile_and_load(commandType)
    return commands

#New
def compile_and_load_file(path: str, commandType: AbstractCommand.CommandType):
    module_name = os.path.split(path)[1].replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.load_module(module_name)

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and name.startswith("Command"):
            command_inst = obj()
            if commandType == command_inst.get_commandType():
                print(" ---Successfully loaded %s: %s" % (commandType, command_inst.get_command()))
                return command_inst.get_command(), command_inst
            elif commandType != command_inst.get_commandType():
                print(" -%s CommandType did not match: %s for: %s" % (command_inst.get_commandType(), commandType, command_inst.get_command()))
    return "", None


#New
def compile_and_load(commandType: AbstractCommand.CommandType) -> Dict[str, AbstractCommand]:
    dic = {}
    implementations = get_implementations_dir()
    for dirName, subdirList, fileList in os.walk(implementations):
        for file in fileList:
            name = os.path.join(dirName, file)
            print("compiling: %s" % name)
            name, command = compile_and_load_file(name, commandType)
            if command is not None and command.command_type is commandType:
                dic[name] = command
        break
    return dic

def get_base_dir() -> str:
    cwd = os.getcwd()
    split = os.path.split(cwd)
    current = split[len(split) - 1]
    if current == 'commands':
        return check_dir(cwd)
    elif current == 'Praxis-Bot' or current == 'Praxis':
        return check_dir(os.path.join(cwd, "commands"))
    else:
        print("could not find working directory for Praxis-Bot/commands")
        raise Exception


def get_implementations_dir() -> str:
    return check_dir(os.path.join(get_base_dir(), "implemented"))


def get_compiled_dir() -> str:
    return check_dir(os.path.join(get_base_dir(), "compiled"))


def check_dir(path: str) -> str:
    if not os.path.exists(path):
        os.mkdir(path, 0x777)
    return path


if __name__ == "__main__":
    cmds = load_commands()

