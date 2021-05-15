# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
# Copyright (C) 2021

# Author Info Examples:
# Name / Email / Website
# Twitter / Twitch / Youtube

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

from time import sleep
import phue
from phue import Bridge

import random
import utilities_script as utilities

import credentials
import config

import flask
from flask import request

import os
import praxis_logging
praxis_logger_obj = praxis_logging.praxis_logger()
praxis_logger_obj.init(os.path.basename(__file__))
praxis_logger_obj.log("\n -Starting Logs: " + os.path.basename(__file__))

api = flask.Flask(__name__)
# enable/disable this to get web pages of crashes returned
api.config["DEBUG"] = False

class Lights_Module():
    def __init__(self):
        super().__init__()
        # The .python_hue is generated in the home directory by default.
        self.bridge_:Bridge = Bridge('192.168.191.42', config_file_path='credentials/.python_hue')

    def main(self):
        praxis_logger_obj.log("\nStarting up [Lights_Module]...")
        self.bridge_.connect()

        self.bridge_.get_api()

        light_list = self.bridge_.lights
        group_list:list = []
        groups = self.bridge_.get_group()
        groupCount = 0

        #praxis_logger_obj.log("\n -Listing Lights...")
        for l in light_list:
            pass
            #praxis_logger_obj.log(l.name)
        #praxis_logger_obj.log("\n -Counting Groups...")
        for g in groups:
            #praxis_logger_obj.log(g)
            groupCount = int(g)


        for gc in range(groupCount):
            try:
                #praxis_logger_obj.log("group n:" + str(gc))
                group = self.bridge_.get_group(gc ,'name')
                #praxis_logger_obj.log(group)
                group_list.append(group)
                #praxis_logger_obj.log(" --done adding")
            except:
                pass
                #praxis_logger_obj.log(" --adding failed")

        #self.bridge_.set_group(18, "bri", 254) #This is max Brightness
        #self.bridge_.set_group(18, "on", True) #This is will turn ON
        #xy_result = self.rgb_to_xy(0,0,1) #This will take an rgb value and make it xy
        #self.bridge_.set_group(16, "xy", xy_result) #This will make the lights in the group turn blue

        # The Following will make a rave
        #for rave in range(10):
            #rgb_r = random.random()
            #rgb_g = random.random()
            #rgb_b = random.random()
            #xy_result = self.rgb_to_xy(rgb_r, rgb_g, rgb_b) #This will take an rgb value and make it xy
            #self.bridge_.set_group(16, "xy", xy_result)
            #sleep(0.1)

        #for stuffz in self.bridge_.scenes:
            #praxis_logger_obj.log(stuffz)

        # This will set the group Downstairs to the Stream scene
        #self.bridge_.run_scene("Downstairs", "Stream")

        #self.bridge_.run_scene("Downstairs", "Stream")
        praxis_logger_obj.log("-[Lights_Module] Setup Complete")

    def setLight():
        pass

    def setLights():
        pass

    def setGroup():
        pass

    def setGroups():
        pass

    def rubiksCube(self):
        for rave in range(10):
            rgb_r = random.random()
            rgb_g = random.random()
            rgb_b = random.random()
            xy_result = self.rgb_to_xy(rgb_r, rgb_g, rgb_b) #This will take an rgb value and make it xy
            self.bridge_.set_group(16, "xy", xy_result, transitiontime=0.2)
            sleep(0.25)
        self.bridge_.run_scene("Downstairs", "Stream")

    def hydration(self):
        self.bridge_.run_scene("Downstairs", "hydration")
        sleep(4)
        self.bridge_.run_scene("Downstairs", "Stream")

    def raveMode(self):
        for rave in range(30):
            rgb_r = random.random()
            rgb_g = random.random()
            rgb_b = random.random()
            xy_result = self.rgb_to_xy(rgb_r, rgb_g, rgb_b) #This will take an rgb value and make it xy
            self.bridge_.set_group(16, "xy", xy_result)
            sleep(0.3)
        self.bridge_.run_scene("Downstairs", "Stream")

    def rgb_to_xy(self, red, green, blue):
        """ conversion of RGB colors to CIE1931 XY colors
        Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
        Args:
        red (float): a number between 0.0 and 1.0 representing red in the RGB space
        green (float): a number between 0.0 and 1.0 representing green in the RGB space
        blue (float): a number between 0.0 and 1.0 representing blue in the RGB space
        Returns:
        xy (list): x and y
        """
        # gamma correction
        red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
        green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
        blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

        # convert rgb to xyz
        x = red * 0.649926 + green * 0.103455 + blue * 0.197109
        y = red * 0.234327 + green * 0.743075 + blue * 0.022598
        z = green * 0.053077 + blue * 1.035763

        # convert xyz to xy
        x = x / (x + y + z)
        y = y / (x + y + z)

        # TODO check color gamut if known
        return [x, y]

    def color_string_parser(self, message):
        maxDigits = config.colorParse_maxDigits
        praxis_logger_obj.log("Searching for color...")
        xy_color = [0, 0]
        for text in message:
            #praxis_logger_obj.log("testing word")
            if "red" in text.lower():
                xy_color = self.rgb_to_xy(1,0,0)
                praxis_logger_obj.log("-found: red")
            if "blue" in text.lower():
                praxis_logger_obj.log("-found: blue")
                xy_color = self.rgb_to_xy(0,0,1)
            if "green" in text.lower():
                praxis_logger_obj.log("-found: green")
                xy_color = self.rgb_to_xy(0,1,0)

            if "yellow" in text.lower():
                praxis_logger_obj.log("-found: yellow")
                xy_color = self.rgb_to_xy(
                    0.7,
                    0.64,
                    0)


            if "cyan" in text.lower():
                praxis_logger_obj.log("-found: cyan")
                xy_color = self.rgb_to_xy(0,1,1)
            if "aquamarine" in text.lower():
                praxis_logger_obj.log("-found: aquamarine")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(111,0,254),maxDigits),
                    round(utilities.rescale_value(218,0,254),maxDigits),
                    round(utilities.rescale_value(146,0,254),maxDigits))
            if "turquoise" in text.lower():
                praxis_logger_obj.log("-found: turquoise")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(172,0,254),maxDigits),
                    round(utilities.rescale_value(233,0,254),maxDigits),
                    round(utilities.rescale_value(232,0,254),maxDigits))

            if "orange" in text.lower():
                praxis_logger_obj.log("-found: orange")
                xy_color = self.rgb_to_xy(
                    1,
                    round(utilities.rescale_value(126,0,254),maxDigits),
                    0)


            if "magenta" in text.lower():
                praxis_logger_obj.log("-found: magenta")
                xy_color = self.rgb_to_xy(
                    1,
                    0,
                    1)

            if "purple" in text.lower():
                praxis_logger_obj.log("-found: purple")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(159,0,254),maxDigits),
                    round(utilities.rescale_value(32,0,254),maxDigits),
                    round(utilities.rescale_value(239,0,254),maxDigits))

            if "violet" in text.lower():
                praxis_logger_obj.log("-found: violet")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(237,0,254),maxDigits),
                    round(utilities.rescale_value(129,0,254),maxDigits),
                    round(utilities.rescale_value(237,0,254),maxDigits))

        return xy_color


RGB_Lights = Lights_Module()

def init():
    RGB_Lights.main()

def do_lights_command(user="", lightGroup="all", command = "", rest = ""):
        returnString = "None"
        praxis_logger_obj.log("about to do something ......")
        praxis_logger_obj.log("about to do something with: " + command + " " + rest)
        #bot.return_message("\nRGB Command Detected!")
        if rest is not "":
            tempFix = command + " " + rest
        else:
            tempFix = command

        tempParsedMessage = tempFix.split(" ")
        sceneCommand = False
        if (len(tempParsedMessage)) > 2:
            praxis_logger_obj.log("RGB Command!")
            rgb_r = float(tempParsedMessage[1])
            rgb_g = float(tempParsedMessage[2])
            rgb_b = float(tempParsedMessage[3])
            xy_result = RGB_Lights.rgb_to_xy(rgb_r, rgb_g, rgb_b)
            praxis_logger_obj.log("got XY")
            RGB_Lights.bridge_.set_group(16, "xy", xy_result)
            #bot.return_message("sent color to [Lights_Module]")
        else:
            if "stream" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.bridge_.run_scene("Downstairs", "Stream")
            elif "normal" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.bridge_.run_scene("Downstairs", "Bright")
            elif "haxor" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.bridge_.run_scene("Downstairs", "hacker vibes")
            elif "off" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.bridge_.set_group("Downstairs", "on", False)
            elif "on" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.bridge_.set_group("Downstairs", "on", True)
            elif "rubikscube" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.rubiksCube()
            elif "hydration" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.hydration()
            elif "ravemode" in tempParsedMessage:
                sceneCommand = True
                RGB_Lights.raveMode()
            else:
                #bot.return_message("Color Command!")
                xy_result = RGB_Lights.color_string_parser(tempParsedMessage)
                #bot.return_message("got XY")
                RGB_Lights.bridge_.set_group(16, "xy", xy_result)
                #bot.return_message("sent color to [Lights_Module]")

            if sceneCommand == True:
                praxis_logger_obj.log("Scene Command!")

        returnString = user + " changed the light's color!"

        return flask.make_response("{\"message\":\"%s\"}" % returnString, 200, {"Content-Type": "application/json"})



@api.route('/api/v1/exec_lights', methods=['GET'])
def exec_lights():
    if 'user_name' not in request.args:
        user_name="User"
    else:
        user_name=request.args['user_name']
    if 'light_group' not in request.args:
        return flask.make_response('{\"text\":"Argument \'light_group\' not in request"}', 400)
    if 'command' not in request.args:
        return flask.make_response('{\"text\":"Argument \'scene_name\' not in request"}', 400)

    praxis_logger_obj.log("about to do something ......")
    RGB_Lights.main()
    return do_lights_command(user_name, request.args['light_group'], request.args['command'], request.args['rest'])

if __name__ == "__main__":
    init()
    api.run(host='0.0.0.0', port=42042)
    #testModule.raveMode()