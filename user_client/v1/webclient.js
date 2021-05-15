// Copyright (C) 2021

// Authors:
//  Name / Email / Website
//      Twitter / Twitch / Youtube / Github

// Authors:
//   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
//      Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd

// This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU Affero General Public License as
//   published by the Free Software Foundation, either version 3 of the
//   License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU Affero General Public License for more details.

//   You should have received a copy of the GNU Affero General Public License
//   along with this program.  If not, see <https://www.gnu.org/licenses/>.


refresh = () => response = fetch('http://127.0.0.1:42055/')
.then((response) => {
    return response.text();
})

ConnectionTest = async () => {
    var a = await refresh();
    console.log(a)
    return a
}

async function BotStatus() {
    var connectionStatus = await ConnectionTest();
    document.getElementById("BotStatus").innerHTML = connectionStatus;
}
BotStatus();


async function setValue(request_type, command, isEnabled) {
    let newCommandState = {
        'request_type': request_type,
        'command_name': command,
        'is_enabled': isEnabled
    }
    let params = "?command_name="+encodeURIComponent(newCommandState.command_name)+"&"+"is_enabled="+encodeURIComponent(newCommandState.is_enabled);
        let targetURL = "http://127.0.0.1:42055/api/v1/user_client/set"+params;
        //console.log(targetURL)
        let a = await fetch_GetList(targetURL);
        //console.log("return: "+a);

}

fetch_GetList = (fetchURL) => response = fetch(fetchURL)
.then((response) => {
    return response.text();
})



GetList = async (listType) => {
    if (true) {
        let ListRequestOBJ = {
            'request_name': listType,
            'request_type': "list"
        }
        let params = "?request_name="+encodeURIComponent(ListRequestOBJ.request_name)+"&"+"request_type="+encodeURIComponent(ListRequestOBJ.request_type);
        let targetURL = "http://127.0.0.1:42055/api/v1/user_client/get"+params;
        //console.log(targetURL)
        let a = await fetch_GetList(targetURL);
        //console.log("return: "+a);
        return a
    }
    else {
        return None
    }
}

async function GetList_OBJ(ListName) {
    let returnedList = await GetList(ListName);
    let obj_main = JSON.parse(returnedList);
    //console.log(returnedList);
    //console.log(obj_main);
    //console.log(typeof obj_main['message'])

    //console.log(obj_main.message);
    //var obj_temp = JSON.parse(obj_main.message['!lights']);

    let data = atob(obj_main.message);
    console.log(ListName, data);
    let notDictionary = JSON.parse(data);
    //let notDictionary = true
    return notDictionary
}

async function updateCommandList() {
    $("#CommandRowWrapper").empty();
    let returnedCommands = await GetList_OBJ("Commands");
    for (var x in returnedCommands){
        //console.log(x)
        var commandName = returnedCommands[x].command
        var isCommandEnabled = ""
        if (returnedCommands[x].isCommandEnabled == "true") {
            isCommandEnabled = "checked"
        }
        var template = ""+
        "<div class=\"rowsInMain row card\" style=\"margin-right: 20px;margin-left: 20px;margin-top: 30px;margin-bottom: 30px;\">" +
        "<div class=\"col s12 switch\" style=\"top: -20px;position: relative;padding-left: 10px;\"><label>Enabled:<input "+ isCommandEnabled +" disabled type=\"checkbox\"><span class=\"lever\"></span></label></div>" +
        "<div class=\"col s4\"><p>Command Name:</p>" +
        "<div class=\"input-field inline\" style=\"width: 80%;\">" +
        "<p style =\"color:grey;\">Command</p>" +
        "<input disabled id=\"\" type=\"text\" value=\""+ commandName +"\" class=\"validate\">" +
        "</div></div></div></div>"
        $("#CommandRowWrapper").append(template);
    }
    //var commandName = "!testerino"
    //var isCommandEnabled = "" // if == "checked" will start off with the isEnabled bool enabled

}

updateCommandList();




async function updateRewardList() {
    $("#RewardRowWrapper").empty();
    console.log("about to update the rewards list");
    let returnedRewards = await GetList_OBJ("Rewards");
    for (var x in returnedRewards){
        //console.log(x)
        let rewardName = returnedRewards[x].channelRewardName
        var isRewardEnabled = ""
        if (returnedRewards[x].isRewardEnabled == "true") {
            isRewardEnabled = "checked"
        }
        let template = ""+
        "<div class=\"rowsInMain row card\" style=\"margin-right: 20px;margin-left: 20px;margin-top: 30px;margin-bottom: 30px;\">" +
        "<div class=\"col s12 switch\" style=\"top: -20px;position: relative;padding-left: 10px;\"><label>Enabled:<input "+ isRewardEnabled +" disabled type=\"checkbox\"><span class=\"lever\"></span></label></div>" +
        "<div class=\"col s4\"><p>Reward Name:</p>" +
        "<div class=\"input-field inline\" style=\"width: 80%;\">" +
        "<p style =\"color:grey;\">Reward</p>" +
        "<input disabled id=\"\" type=\"text\" value=\""+ rewardName +"\" class=\"validate\">" +
        "</div></div></div></div>"
        $("#RewardRowWrapper").append(template);
    }
    //var commandName = "!testerino"
    //var isCommandEnabled = "" // if == "checked" will start off with the isEnabled bool enabled

}
updateRewardList();



GetEventList = async () => {
    if (true) {
        let ListRequestOBJ = {
            'request_name': "EventHistory",
            'request_type': "list",
            'request_data': "50"
        }
        let params = "?request_name="+encodeURIComponent(ListRequestOBJ.request_name)
        +"&"+"request_type="+encodeURIComponent(ListRequestOBJ.request_type)
        +"&"+"request_data="+encodeURIComponent(ListRequestOBJ.request_data);
        let targetURL = "http://127.0.0.1:42055/api/v1/user_client/get"+params;
        //console.log(targetURL)
        let a = await fetch_GetList(targetURL);
        //console.log("return: "+a);
        return a
    }
    else {
        return None
    }
}

async function GetEventList_OBJ() {
    let returnedList = await GetEventList();
    let obj_main = JSON.parse(returnedList);
    //console.log(returnedList);
    console.log(obj_main);
    //console.log(typeof obj_main['message'])

    //console.log(obj_main.message);
    //var obj_temp = JSON.parse(obj_main.message['!lights']);

    let data = atob(obj_main.message);
    console.log("Event List OBJ: ", data);
    let notDictionary = JSON.parse(data);
    //let notDictionary = true
    return notDictionary
}

async function updateEventList() {
    $("#EventHistoryWrapper").empty();
    let returnedEvents = await GetEventList_OBJ();


    // let template = ""+
    // "<div class=\"rowsInMain row card\">"+
    // "<div class=\"col s3\"><p>Event:"+ "eventName" +"</p></div>"+
    // "<div class=\"col s3\"><p>User:"+ "eventSender" +"</p></div>"+
    // "<div class=\"col s3\"><p>Message:"+ "eventData" +"</p></div>"+
    // "<a onclick=\"reRunEvent()\" class=\"btn waves-effect waves-light green right col s1\" style=\"position: absolute; right: 0; top: 0; width: 3em;\">"+
    // "<i class=\"material-icons\">refresh</i>"+
    // "</a></div>"
    // $("#EventHistoryWrapper").append(template);
    // $("#EventHistoryWrapper").append(template);
    // $("#EventHistoryWrapper").append(template);
    // $("#EventHistoryWrapper").append(template);
    // $("#EventHistoryWrapper").append(template);
    // $("#EventHistoryWrapper").append(template);

    console.log(returnedEvents)
    try {
        for (var x in returnedEvents){
            console.log(x)
            let eventName = returnedEvents[x].eventName
            let eventTime = returnedEvents[x].eventTime
            let eventType = returnedEvents[x].eventType
            let eventSender = returnedEvents[x].eventSender
            let eventData = returnedEvents[x].eventData

            //console.log(eventName)
            //console.log(eventTime)
            //console.log(eventType)
            //console.log(eventSender)

            //let reRunEvent_Params = String("reRunEvent(\"" + eventName + "\", \"" + eventTime + "\", \"" + eventType + "\", \"" + eventSender + "\", \"" + eventData+"\")")
            let reRunEvent_Params = `reRunEvent(&quot;${eventName}&quot;, &quot;${eventTime}&quot;, &quot;${eventType}&quot;, &quot;${eventSender}&quot;, &quot;${eventData}&quot;)`
            //let reRunEvent_Params = `reRunEvent('${eventName}', '${eventTime}', '${eventType}', '${eventSender}', '${eventData}')`
            console.log(reRunEvent_Params)
            //let reRunEvent_Params = String("reRunEvent()")
            let template = ""+
            "<div class=\"rowsInMain row card\">"+
            "<div class=\"col s12\" style=\"position:absolute;top:0;color:grey;\">Time: "+ eventTime +"</div>"+
            "<div class=\"col s12 m3\"><p>Event: <br>"+ eventName +"</p><br></div>"+
            "<div class=\"col s12 m3\"><p>User: <br>"+ eventSender +"</p><br></div>"+
            "<div class=\"col s12 m3\"><p>Message: <br>"+ eventData +"</p><br></div>"+
            '<a onclick="'+ reRunEvent_Params +'" class="hide btn waves-effect waves-light green right col s1" style="position: absolute; right: 0; top: 0; width: 3em;">'+
            "<i class=\"material-icons\">refresh</i>"+
            "</a></div>"
            $("#EventHistoryWrapper").prepend(template);
        }
    }finally {

    }

}
updateEventList();



fetch_RerunEvent = (fetchURL) => response = fetch(fetchURL)
.then((response) => {
    return response.text();
})

RerunEvent_OBJ = async (eventToRun) => {
    if (true) {
        let exampleEvent = {
            'eventName': "",
            'eventTime': "",
            'eventType': "",
            'eventSender': "",
            'eventData': ""
        }
        let params = ""+
        "?eventName="+encodeURIComponent(eventToRun['eventName'])+
        "&"+"eventTime="+encodeURIComponent(eventToRun['eventTime'])+
        "&"+"eventType="+encodeURIComponent(eventToRun['eventType'])+
        "&"+"eventSender="+encodeURIComponent(eventToRun['eventSender'])+
        "&"+"eventData="+encodeURIComponent(eventToRun['eventData']);
        let targetURL = "http://127.0.0.1:42055/api/v1/user_client/event_log/reRunEvent"+params;
        //console.log(targetURL)
        let a = await fetch_RerunEvent(targetURL);
        //console.log("return: "+a);
        return a
    }
    else {
        return None
    }
}



async function reRunEvent(eventName, eventTime, eventType, eventSender, eventData) {
    var newEvent = {
        'eventName': eventName,
        'eventTime': eventTime,
        'eventType': eventType,
        'eventSender': eventSender,
        'eventData': eventData
    }
    let response = await RerunEvent_OBJ(newEvent);
    console.log(response)
    let main = JSON.parse(response);
    let data = main.message
    console.log("response: ", data);
}