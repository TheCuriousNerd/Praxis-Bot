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

from channel_rewards.channelRewards_base import AbstractChannelRewards


#New
def load_rewards(channelRewardsType: AbstractChannelRewards.ChannelRewardsType) -> Dict[str, AbstractChannelRewards]:
    print(" -Loading ", channelRewardsType ," ChannelRewards...\n")
    ChannelRewards = compile_and_load(channelRewardsType)
    return ChannelRewards

#New
def compile_and_load_file(path: str, channelRewardsType: AbstractChannelRewards.ChannelRewardsType):
    module_name = os.path.split(path)[1].replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.load_module(module_name)

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and name.startswith("ChannelReward"):
            ChannelReward_inst = obj()
            if channelRewardsType == ChannelReward_inst.get_ChannelRewardType():
                print(" ---Successfully loaded %s: %s" % (channelRewardsType, ChannelReward_inst.get_ChannelRewardName()))
                return ChannelReward_inst.get_ChannelRewardName(), ChannelReward_inst
            elif channelRewardsType != ChannelReward_inst.get_ChannelRewardType():
                print(" -%s ChannelRewardsType did not match: %s for: %s" % (ChannelReward_inst.get_ChannelRewardType(), channelRewardsType, ChannelReward_inst.get_ChannelRewardName()))
    return "", None


#New
def compile_and_load(ChannelRewardType: AbstractChannelRewards.ChannelRewardsType) -> Dict[str, AbstractChannelRewards]:
    dic = {}
    implementations = get_implementations_dir()
    for dirName, subdirList, fileList in os.walk(implementations):
        for file in fileList:
            name = os.path.join(dirName, file)
            print("compiling: %s" % name)
            name, reward = compile_and_load_file(name, ChannelRewardType)
            if reward is not None and reward.ChannelRewardType is ChannelRewardType:
                dic[name] = reward
        break
    return dic

def get_base_dir() -> str:
    cwd = os.getcwd()
    split = os.path.split(cwd)
    current = split[len(split) - 1]
    if current == 'channel_rewards':
        return check_dir(cwd)
    elif current == 'Praxis-Bot' or current == 'Praxis':
        return check_dir(os.path.join(cwd, "channel_rewards"))
    else:
        print("could not find working directory for Praxis-Bot/channel_rewards")
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
    rewards = load_rewards()

