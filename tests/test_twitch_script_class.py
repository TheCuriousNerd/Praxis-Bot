# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

# Authors:
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

import unittest
import twitch_script_class
import twitch


testValidUrls = ['https://shady.ru', 'http://stolencards.zn', 'https://i.imgur.com/FL6slHd.jpg']
testInvalidUrls = ['this is just a sentence. With a period', 'gotta have some other stuff', 'bad punctuation. does produces false positives']


class TwitchBotTest(unittest.TestCase):
    def setUp(self):
        self.bot = twitch_script_class.Twitch_Module()

    def test_find_url(self):
        bot = self.bot
        for link in testInvalidUrls:
            msg = twitch.chat.Message("", "", link)
            t = bot.contains_url(msg)
            assert not t

        for link in testValidUrls:
            msg = twitch.chat.Message("", "", link)
            t = bot.contains_url(msg)
            assert t

    def test_find_slur(self):
        nonSlurMessage = twitch.chat.Message("", "", "hey look, a normal sentence")
        slurMessage = twitch.chat.Message("", "", "fag is a hateful word that shouldn't be used anymore")
        assert not self.bot.contains_slur(nonSlurMessage)
        assert self.bot.contains_slur(slurMessage)


if __name__ == '__main__':
    unittest.main()

