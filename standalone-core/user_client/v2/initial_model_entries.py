from apps.home.models import *

def main_setup():
    setup_default_commands()


def setup_default_commands():
    initialCommandList = [
        ("!math", "(#*) = ($math (#*))"),
        ("!convertunit", "(#0) (#1) = ($math_unitConversion (#*)) (#2)"),
        ("!curdaytime", "The current date and time is: ($datetime (#*))"),
        ("!cryptoprice", "The current price of (#0) against (#1) is ($getCryptoPrice ((#0) (#1)))"),
        ("!speak", "($play (#*))"),
    ]
    for command in initialCommandList:
        setup_command(command[0], command[1])

def setup_command(command, response):
    newCMD = PraxisBot_Commands_v0()
    newCMD.command = command
    newCMD.response = response
    newCMD.isEnabled = True
    newCMD.save()