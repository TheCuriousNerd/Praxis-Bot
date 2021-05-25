# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
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
from bot_functions import utilities_script as utilities

import credentials
import config

class Lights_Module():
    def __init__(self):
        super().__init__()
        self.bridge_:Bridge = Bridge('192.168.191.146')

    def main(self):
        print("\nStarting up [Lights_Module]...")
        self.bridge_.connect()

        self.bridge_.get_api()

        light_list = self.bridge_.lights
        group_list:list = []
        groups = self.bridge_.get_group()
        groupCount = 0

        #print("\n -Listing Lights...")
        for l in light_list:
            pass
            #print(l.name)
        #print("\n -Counting Groups...")
        for g in groups:
            #print(g)
            groupCount = int(g)


        for gc in range(groupCount):
            try:
                #print("group n:" + str(gc))
                group = self.bridge_.get_group(gc ,'name')
                #print(group)
                group_list.append(group)
                #print(" --done adding")
            except:
                pass
                #print(" --adding failed")

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
            #print(stuffz)

        # This will set the group Downstairs to the Stream scene
        #self.bridge_.run_scene("Downstairs", "Stream")

        print("-[Lights_Module] Setup Complete")

    def setLight():
        pass

    def setLights():
        pass

    def setGroup():
        pass

    def setGroups():
        pass

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
        print("Searching for color...")
        xy_color = [0, 0]
        for text in message:
            #print("testing word")
            if "red" in text.lower():
                xy_color = self.rgb_to_xy(1,0,0)
                print("-found: red")
            if "blue" in text.lower():
                print("-found: blue")
                xy_color = self.rgb_to_xy(0,0,1)
            if "green" in text.lower():
                print("-found: green")
                xy_color = self.rgb_to_xy(0,1,0)

            if "yellow" in text.lower():
                print("-found: yellow")
                xy_color = self.rgb_to_xy(
                    0.7,
                    0.64,
                    0)


            if "cyan" in text.lower():
                print("-found: cyan")
                xy_color = self.rgb_to_xy(0,1,1)
            if "aquamarine" in text.lower():
                print("-found: aquamarine")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(111,0,254),maxDigits),
                    round(utilities.rescale_value(218,0,254),maxDigits),
                    round(utilities.rescale_value(146,0,254),maxDigits))
            if "turquoise" in text.lower():
                print("-found: turquoise")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(172,0,254),maxDigits),
                    round(utilities.rescale_value(233,0,254),maxDigits),
                    round(utilities.rescale_value(232,0,254),maxDigits))

            if "orange" in text.lower():
                print("-found: orange")
                xy_color = self.rgb_to_xy(
                    1,
                    round(utilities.rescale_value(126,0,254),maxDigits),
                    0)


            if "magenta" in text.lower():
                print("-found: magenta")
                xy_color = self.rgb_to_xy(
                    1,
                    0,
                    1)

            if "purple" in text.lower():
                print("-found: purple")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(159,0,254),maxDigits),
                    round(utilities.rescale_value(32,0,254),maxDigits),
                    round(utilities.rescale_value(239,0,254),maxDigits))

            if "violet" in text.lower():
                print("-found: violet")
                xy_color = self.rgb_to_xy(
                    round(utilities.rescale_value(237,0,254),maxDigits),
                    round(utilities.rescale_value(129,0,254),maxDigits),
                    round(utilities.rescale_value(237,0,254),maxDigits))

        return xy_color


if __name__ == "__main__":
    testModule = Lights_Module()

    credentials_manager = credentials.Credentials_Module()
    credentials_manager.load_credentials()

    testModule.main()
    #testModule.raveMode()