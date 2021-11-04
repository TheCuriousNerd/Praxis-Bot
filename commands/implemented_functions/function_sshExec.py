# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

# Authors:
#   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
#       Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd

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

from abc import ABCMeta

from json import loads
from urllib.parse import urlencode
import requests

from commands.command_base import AbstractCommand
from commands.command_functions import AbstractCommandFunction

from commands.command_functions import Abstract_Function_Helpers

from bot_functions import utilities_script as utility

import paramiko

class Function_sshExec(AbstractCommandFunction, metaclass=ABCMeta):
    """
    This is v0 of Functions
    """
    functionName = "superExec"
    helpText = ["This is a v0 function.",
        "\nExample:","testFunction"]

    def __init__(self):
        super().__init__(
            functionName = Function_sshExec.functionName,
            n_args = 0,
            functionType = AbstractCommandFunction.FunctionType.ver0,
            helpText = Function_sshExec.helpText,
            bonusFunctionData = None
            )

    def do_function(self, user, functionName, args, bonusData):
        output = self.do_work(user, functionName, args, bonusData)

        return output

    def do_work(self, user, functionName, args, bonusData):
        isFileTransfer = False
        isContainerCommand = False

        if args[0] == "file":
            isFileTransfer = True
        if (args[0] == "stop") or (args[0] == "start") or (args[0] == "restart"):
            isContainerCommand = True


        return "work"

    class ssh_connection():
        def __init__(self, host, port, username, password):
            self.host = host
            self.port = port
            self.username = username
            self.password = password

            self.ssh_session = None

        def connect(self):
            self.ssh_session = paramiko.SSHClient()
            self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_session.connect(self.host, self.port, self.username, self.password)

        def close(self):
            self.ssh_session.close()

        def send_command(self, command):
            stdin, stdout, stderr = self.ssh_session.exec_command(command)
            return stdout.read()

    class fileTransfer():
        def __init__(self, host, port, username, password):
            self.host = host
            self.port = port
            self.username = username
            self.password = password

            self.sftp_session = None

        def connect(self):
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username = self.username, password = self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            self.sftp_session = sftp

        def close(self):
            self.sftp_session.close()

        def send_file(self, local_file, remote_file):
            self.sftp_session.put(local_file, remote_file)

        def get_file(self, remote_file, local_file):
            self.sftp_session.get(remote_file, local_file)
