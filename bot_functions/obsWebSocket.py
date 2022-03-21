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

import asyncio
import simpleobsws
import json
import config

loop = asyncio.get_event_loop()
#loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
idParams = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
targetURL = "ws://%s:%s" % (config.obsWebSocket_address[0].get("ip"), config.obsWebSocket_address[0].get("port"))
ws = simpleobsws.WebSocketClient(url=targetURL, password=config.obsWebSocket_address[0].get("password")) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def default_request():
    await ws.connect() # Make the connection to OBS-Websocket
    result = await ws.call('GetVersion') # We get the current OBS version. More request data is not required
    print(result) # Print the raw json output of the GetVersion request
    await asyncio.sleep(1)
    requests = result['available-requests'].split(',')

    #data = {'source':'test_source', 'volume':0.5}
    #result = await ws.call('SetVolume', data) # Make a request with the given data
    #print(result)
    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.
    return requests

async def make_custom_request(request, data=None):
    print("\n===========================================")
    print(request)
    print("Data to use:")
    print(data)
    print(type(data))
    try:
        await ws.connect() # Make the connection to OBS-Websocket
        print("Connected to OBS-Websocket")
        await ws.wait_until_identified() # Wait until the connection is fully established.
        print("Identified with OBS-Websocket")
    except Exception as e:
        print(e)
        return e


    print('Making request:')
    try:
        if data!=None:
            #data = {'source':'tinycam', 'volume':0.5}
            print("data for OBS")

            print(request)
            if request == "SetSceneItemEnabled":
                if data.get("sceneItemId") == None:
                    sceneItemList = ("GetSceneItemList",{'sceneName':data.get('sceneName')})
                    requestList = simpleobsws.Request(sceneItemList[0], sceneItemList[1])
                    resultList:simpleobsws.RequestResponse = await ws.call(requestList)
                    if resultList.ok():
                        items = resultList.responseData.get("sceneItems")
                        for i in items:
                            #print(i)
                            #print(i.get("sourceName"))
                            if i.get("sourceName") == data.get("sourceName"):
                                id = i.get("sceneItemId")
                                #print("Found source: " + data.get("sourceName"))
                                #print("Source ID: " + str(id))
                                data["sceneItemId"] = id
                                break


            requestObj = simpleobsws.Request(request, data)
            result = await ws.call(requestObj) # Make a request with the given data
            if result.ok():
                print(result)
            await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.
            return result
    except Exception as e:
        print("\n" + str(e) + "\n")
        return e


























async def on_event(data):
    print('New event! Type: {} | Raw Data: {}'.format(data['update-type'], data)) # Print the event data. Note that `update-type` is also provided in the data

async def on_switchscenes(data):
    print("\n===========================================\n\n")
    print('Scene switched to "{}". It has these sources: {}'.format(data['scene-name'], data['sources']))



def getRequests():
    return loop.run_until_complete(default_request())

def makeRequest(request, data):
    try:
        return loop.run_until_complete(make_custom_request(request, data))
        #return "True"
    except Exception as e:
        return e



# def listenForData():
#     print("\n\nListener:")

#     loop = asyncio.get_event_loop()
#     ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='MYSecurePassword', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.
#     loop.run_until_complete(ws.connect())
#     ws.register(on_event) # By not specifying an event to listen to, all events are sent to this callback.
#     ws.register(on_switchscenes, 'SwitchScenes')
#     loop.run_forever()



if __name__ == "__main__":
    #print("\n\nRequests:")
    #loop.run_until_complete(get_requests())

    #makeRequest("ToggleStudioMode")
    #listenForData()
    pass
