# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from distutils.command import config
import json
from logging import exception
import random
from tkinter import E
from urllib import response
from urllib.parse import urlencode
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest

from .models import Chyron_Entry, PraxisBot_Commands_v0, PraxisBot_Settings
from .forms import Chyron_EntryForm, PraxisBot_Commands_v0_Form, PraxisBot_Settings_Form
import requests
import initial_model_entries

from django.contrib.auth.models import User

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    load_template = request.path.split('/')[-1]
    context = index_dashboard(request, context, load_template)
    try:
        print("PraxisBot_Settings lookup")
        print(PraxisBot_Settings.objects.filter(id=1))
        settingsLookup = PraxisBot_Settings.objects.get(id=1)
        print(settingsLookup.initialSetup)
        if settingsLookup.initialSetup == False:
            initial_model_entries.main_setup()
            settingsLookup.initialSetup = True
            settingsLookup.save()
    except:
        print("PraxisBot_Settings making a new one")
        settings = PraxisBot_Settings()
        settings.id = 1
        settings.initialSetup = False
        settings.save()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if 'index' in load_template:
            context = index_dashboard(request, context, load_template)
        if 'chyron' in load_template:
            context = chyron(request, context, load_template)
        if 'commands' in load_template:
            context = commands(request, context, load_template)
        if 'settings' in load_template:
            context = settings(request, context, load_template)

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

#def testerino(request, pk):
    #print("testerino")
    #return HttpResponse("testerino")

def testerino():
    print("testerino")


def index_dashboard(request, context:dict, load_template):

    try:
        print("PraxisBot_Settings lookup")
        print(PraxisBot_Settings.objects.filter(id=1))
        settingsLookup = PraxisBot_Settings.objects.get(id=1)
        print(settingsLookup.initialSetup)
        if settingsLookup.initialSetup == False:
            initial_model_entries.main_setup()
            settingsLookup.initialSetup = True
            settingsLookup.save()
    except:
        print("PraxisBot_Settings making a new one")
        settings = PraxisBot_Settings()
        settings.id = 1
        settings.initialSetup = False
        settings.save()

    try:
        url = "http://%s:%s/api/v1/containers/get_status" % ("standalone-core-manager", str(42002))
        results = requests.get(url)
        data = results.text
        print(data)
        print(type(data))
        loaded_data = json.loads(data)
        print(loaded_data)
        print(type(loaded_data))
        #print(json.loads(msg))
        errorStatusText = "unknown status"
        context['standalone_core_manager'] = loaded_data['standalone-core-manager']
        context['standalone_eventlog'] = loaded_data['standalone-eventlog']
        context['standalone_user_client'] = loaded_data['standalone-user-client']
        context['standalone_websource'] = loaded_data['standalone-websource']
        context['standalone_lights'] = loaded_data['standalone-lights']
        context['standalone_tts_core'] = loaded_data['standalone-tts-core']
        context['standalone_channelrewards'] = loaded_data['standalone-channelrewards']
        context['standalone_command'] = loaded_data['standalone-command']
        context['standalone_discord_script'] = loaded_data['standalone-discord-script']
        context['standalone_twitch_script'] = loaded_data['standalone-twitch-script']
        context['standalone_twitch_pubsub'] = loaded_data['standalone-twitch-pubsub']
    except Exception as e:
        print(e)
        errorStatusText = "Core Missing! 😰"
        context['standalone_core_manager'] = errorStatusText
        context['standalone_eventlog'] = errorStatusText
        context['standalone_user_client'] = errorStatusText
        context['standalone_websource'] = errorStatusText
        context['standalone_lights'] = errorStatusText
        context['standalone_tts_core'] = errorStatusText
        context['standalone_channelrewards'] = errorStatusText
        context['standalone_command'] = errorStatusText
        context['standalone_discord_script'] = errorStatusText
        context['standalone_twitch_script'] = errorStatusText
        context['standalone_twitch_pubsub'] = errorStatusText


    # Various Bot tips and tricks for the user in the dashboard
    hotTipsList = [
        "You can use the Praxis-Bot to control your lights, turn on/off your lights, and set your lights to a specific color (Currently just Phillips Hue).",
        "You can nest functions in your custom commands. For example, you could use a math function which takes in a dice roll function as well as the user's arguments for the command.",
        "If you want to add a custom function, add it to /commands/implemented_functions/ folder then you can use it in your custom commands.",
    ]

    #This loads a random tip from hotTipsList
    context['dashboard_hot_tips'] = hotTipsList[random.randint(0, len(hotTipsList) - 1)]

    return context







def chyron(request:WSGIRequest, context, load_template):
    if 'chyron' in load_template:
        try:
            chyron_list = Chyron_Entry.objects.all().order_by('id')
            #context['chyron_list'] = chyron_list
        except:
            context['chyron_list'] = " No chyron entries found "



        try:

            if request.method == 'GET':
                print("GET")
                #print(request.GET.keys())
                #print(request.get_full_path())
            if(request.GET.get('Deletebtn')):
                testerino()
                print(request.GET.get('hidden_id'))
                print(type(request.GET.get('hidden_id')))
                targetID = int(request.GET.get('hidden_id'))
                Chyron_Entry.objects.filter(id=targetID).delete()
        except:
            print("testerino failed?")



        if request.method != 'POST':
            context['chyron_form'] = Chyron_EntryForm()
        if request.method == 'POST':
            print("POST chyron_page")
            try:
                if request.POST.get('newChyronEntry_Btn'):
                    print(request)
                    print(request.POST)
                    context['chyron_form'] = Chyron_EntryForm()
                    form = Chyron_EntryForm(request.POST)
                    if form.is_valid():
                        print("valid form")
                        print(request.POST.get('text'))
                        print(request.POST.get('tag'))
                        form.save()
            except Exception as e:
                print("chyron_page error")
                context['chyron_form'] = e


            #updateChyron_Btn
            try:
                if request.POST.get('updateChyron_Btn'):
                    print(request)
                    print(request.POST)
                    url="http://%s:%s/api/v1/chyron/update_file" % ("standalone-command", str(42010))
                    resp = requests.get(url)

            except Exception as e:
                context['chyron_form'] = e

            try:
                context['chyron_form'] = Chyron_EntryForm()
                if request.POST.get('Updatebtn'):
                    print("Updatebtn")
                    print(request)
                    print(request.POST)

                    isItEnabled = request.POST.get('is_enabled')
                    prefix = request.POST.get('prefix')
                    text = request.POST.get('text')
                    tag = request.POST.get('tag')
                    id = request.POST.get('hidden_id')
                    print(text)
                    print(tag)
                    print(isItEnabled)
                    print(id)
                    targetID = int(id)
                    if isItEnabled:
                        isItEnabled = True
                    else:
                        isItEnabled = False
                    Chyron_Entry.objects.filter(id=targetID).update(prefix=prefix, text=text, tag=tag, is_enabled=isItEnabled)


            except Exception as e:
                print("chyron_page error")
                context['chyron_form'] = e
    return context


def commands(request:WSGIRequest, context, load_template):
    if 'commands' in load_template:
        try:
            commands_list = PraxisBot_Commands_v0.objects.all().order_by('id')
            context['commands_list'] = commands_list
        except:
            context['commands_list'] = " No command entries found "



        try:

            if request.method == 'GET':
                print("GET")
                #print(request.GET.keys())
                #print(request.get_full_path())
            if(request.GET.get('Deletebtn')):
                testerino()
                print(request.GET.get('hidden_id'))
                print(type(request.GET.get('hidden_id')))
                targetID = int(request.GET.get('hidden_id'))
                PraxisBot_Commands_v0.objects.filter(id=targetID).delete()
        except:
            print("testerino failed?")


        if request.method != 'POST':
            context['commands_form'] = PraxisBot_Commands_v0_Form()
        if request.method == 'POST':
            print("POST command_page")
            try:
                if request.POST.get('newCommandEntry_Btn'):
                    print(request)
                    print(request.POST)
                    context['commands_form'] = PraxisBot_Commands_v0_Form()
                    form = PraxisBot_Commands_v0_Form(request.POST)
                    if form.is_valid():
                        print("valid form")
                        print(request.POST.get('command'))
                        print(request.POST.get('response'))
                        form.save()
            except Exception as e:
                print("command_page error")
                context['commands_form'] = e

            try:
                context['commands_form'] = PraxisBot_Commands_v0_Form()
                if request.POST.get('UpdateCommand_Btn'):
                    print("UpdateCommand_Btn")
                    print(request)
                    print(request.POST)

                    isItEnabled = request.POST.get('is_enabled')
                    command = request.POST.get('command')
                    response = request.POST.get('response')
                    id = request.POST.get('hidden_id')
                    print(command)
                    print(response)
                    print(isItEnabled)
                    print(id)
                    targetID = int(id)
                    if isItEnabled:
                        isItEnabled = True
                    else:
                        isItEnabled = False
                    PraxisBot_Commands_v0.objects.filter(id=targetID).update(command=command, response=response, is_enabled=isItEnabled)


            except Exception as e:
                print("commands_page error")
                context['commands_form'] = e

    return context


def settings(request:WSGIRequest, context:dict, load_template):
    if 'settings' in load_template:
        curUser = request.user
        context['userName'] = curUser

        if request.POST.get('UpdateUserAccount_Btn'):
            newPass = request.POST.get('password_account_settings')
            print(newPass)
            targetUser:User = User.objects.get(username__exact=curUser)
            targetUser.set_password(newPass)
            targetUser.save()


    return context