from abc import ABCMeta, abstractmethod
from enum import Enum, auto

class AbstractCommandFunction(metaclass=ABCMeta):
    class FunctionType(Enum):
        NONE = auto()
        ver0 = auto()


    def __init__(
            self,
            functionName: str,
            n_args: int = 0,
            functionType = FunctionType.NONE,
            helpText:list=["No Help"]
        ):
        self.functionName = functionName
        self.n_args = n_args
        self.functionType = functionType
        self.helpText = helpText

    # no touch!
    def get_args(self, text: str) -> list:
        return text.split(" ")[0:self.n_args + 1]

    # no touch!
    def get_name(self) -> str:
        return self.functionName

    # no touch!
    def get_functionType(self):
        return self.functionType

    # no touch!
    def get_help(self):
        return self.helpText

    @abstractmethod
    def do_function(self, user, input):
        pass

class Function_Helpers():
    from json import loads
    from urllib.parse import urlencode
    import requests

    def send_Lights_Command(self, username, light_group, command, rest):
        # todo need to url-escape command and rest
        params = self.urlencode({'user_name': username, 'light_group': light_group, 'command': command, 'rest':rest})
        #standalone_lights
        url = "http://standalone_lights:42042/api/v1/exec_lights?%s" % params
        resp = self.requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = self.loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            return None

    def send_TTS(self, username, message):
        params = self.urlencode({'tts_sender': username, 'tts_text': message})
        #standalone_tts_core
        url = "http://standalone_tts_core:42064/api/v1/tts/send_text?%s" % params
        resp = self.requests.get(url)
        if resp.status_code == 200:
            print("Got the following message: %s" % resp.text)
            data = self.loads(resp.text)
            msg = data['message']
            if msg is not None:
                return msg
                # todo send to logger and other relevent services
        else:
            # todo handle failed requests
            pass