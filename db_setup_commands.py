from commands import loader as command_loader
from commands.command_base import AbstractCommand

from bot_functions import utilities_db as db_utility


loadedCommands = {}


def db_setup():
    db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    db_obj.dbConnection.execute('DROP TABLE command_responses_v0')
    if db_obj.doesTableExist("command_responses_v0") == False:
        print("Making Table")
        results = db_obj.execQuery(
            'CREATE TABLE command_responses_v0 ('
            'id SERIAL, '
            'command TEXT, '
            'response TEXT);')
    db_obj.closeConnection()


# def create_basicCommands():
#     db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
#     if db_obj.doesTableExist("command_responses_v0") == True:
#         results = db_obj.execQuery(
#             'INSERT INTO command_responses_v0 '
#             '(command, response) '
#             'VALUES (\'test\',\'This is a $(test) command @(user)\');'
#             )
#         print(results)
#     db_obj.closeConnection()

def create_basicCommands():
    create_basicCommand("!testerino", "A Testerino is Detected $(testerino $(#0))")

    create_basicCommand("!chyron", "$(chyron $(#*))")
    create_basicCommand("!roll", "$(roll $(#*))")
    create_basicCommand("!lights", "$(lights $(#*))")
    create_basicCommand("!text", "$(text $(#*))")
    create_basicCommand("!tts", "$(tts $(#*))")

def create_basicCommand(commandName:str, commandReponse:str):
    db_obj = db_utility.Praxis_DB_Connection(autoConnect=True)
    if db_obj.doesTableExist("command_responses_v0") == True:
        results = db_obj.execQuery(
            'INSERT INTO command_responses_v0 '
            '(command, response) '
            'VALUES (\'%s\',\'%s\');' % (commandName, commandReponse)
            )
        print(results)
    db_obj.closeConnection()

def init():
    # todo load entire command library and cache it here
    load_commands()

def load_commands():
    global loadedCommands
    loadedCommands = command_loader.load_commands(AbstractCommand.CommandType.Ver3)

def handle_command(command, argz):
    cmd:AbstractCommand = loadedCommands[command]
    if cmd is not None:
        cmd_response = cmd.do_command(
            AbstractCommand.CommandSource.default,
            "test_user",
            "0",
            command,
            argz,
            None)
        return cmd_response
    else:
        return None

if __name__ == '__main__':
    db_setup()

    create_basicCommands()
    init()

    #results = handle_command("!test", "")