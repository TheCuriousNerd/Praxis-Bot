# The main repository of Praxis_Bot can be found at: <https://github.com/TheCuriousNerd/Praxis_Bot>.
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

from abc import ABCMeta, abstractmethod
from enum import Enum, auto


class AbstractChannelRewards(metaclass=ABCMeta):
    """
    This is the base class for channel points. In order to load a channel point redemption a few conditions must be met:
    1) The class name MUST begin with 'ChannelPoint' i.e. CommandTTS, CommandBan, etc...
    2) the class MUST extend AbstractCommand

    Generally, it would be advisable to define the ChannelPointPrize redemption name as a variable of the
    class and to then call super().__init__(command)
    """

    class ChannelRewardsType(Enum):
        NONE = auto()
        channelPoints = auto()
        twitch_bits = auto()
        twitch_subs = auto()

    class ChannelRewardsSource(Enum):
        default = 0
        Praxis = 1
        Twitch = 2
        Discord = 3

    def __init__(self, ChannelRewardName: str, n_args: int = 0, ChannelRewardType=ChannelRewardsType.NONE, helpText:list=["No Help"], isChannelRewardEnabled = True):
        self.ChannelRewardName = ChannelRewardName
        self.n_args = n_args
        self.ChannelRewardType = ChannelRewardType
        self.help = helpText
        self.isChannelRewardEnabled = isChannelRewardEnabled

    # no touch!
    def get_args(self, text: str) -> list:
        return text.split(" ")[0:self.n_args + 1]

    # no touch!
    def get_ChannelRewardName(self) -> str:
        return self.ChannelRewardName

    # no touch!
    def get_ChannelRewardType(self):
        return self.ChannelRewardType

    # no touch!
    def get_help(self):
        return self.help

    # no touch!
    def is_ChannelReward_enabled(self):
        return self.isChannelRewardEnabled

    @abstractmethod
    def do_ChannelReward(self, source, user, command, rewardPrompt, userInput, bonusData):
        pass