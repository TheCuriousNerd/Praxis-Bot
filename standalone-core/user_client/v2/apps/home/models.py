# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from cProfile import label
from email import message
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PraxisBot_Settings(models.Model):
    """
    PraxisBot Settings
    """
    id = models.AutoField(primary_key=True)
    initialSetup = models.BooleanField(default=False)


class Chyron_Entry(models.Model):
    """
    This model will hold the data for the Chyron
    """
    id = models.AutoField(primary_key=True)
    prefix = models.CharField(max_length=500, blank=True, null=False, default="")
    text = models.CharField(max_length=1000, blank=True, null=False, default="")
    tag = models.CharField(max_length=200)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.text + " " + self.tag + " " + str(self.is_enabled)


class PraxisBot_EventLog(models.Model):
    """
    This model will hold the data for the Event Log
    """
    id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=300)
    eventType = models.CharField(max_length=300)
    source_service = models.CharField(max_length=300) # ie Twitch, Discord, etc.
    user = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.event + " " + self.eventType + " " + self.source_service + " " + self.user + " " + str(self.time) + " " + self.message

class PraxisBot_Commands_v0(models.Model):
    """
    This model will hold the data for the Command
    """
    id = models.AutoField(primary_key=True)
    command = models.CharField(max_length=200)
    response = models.CharField(max_length=500)
    is_enabled = models.BooleanField(default=False)

    last_used = models.IntegerField(default=0) # This will be Unix Time

    allowed_services = models.CharField(max_length=500, blank=True, null=False, default="")
    cooldown_length = models.IntegerField(default=0)

    is_restricted = models.BooleanField(default=False)
    allowed_users = models.CharField(max_length=500, blank=True, null=False, default="")
    allowed_groups = models.CharField(max_length=500, blank=True, null=False, default="")

    def __str__(self):
        return self.command + " " + self.response + " " + str(self.is_enabled)


class PraxisBot_Commands_v0_SavedVariables(models.Model):
    """
    This model will hold the data for the Command Syntax
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    data = models.TextField(max_length=1000, blank=True, default="")
    last_used = models.IntegerField(default=0) # This will be Unix Time
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.data + " " + self.last_used + " " + str(self.is_enabled)


class PraxisBot_Users(models.Model):
    """
    This model will define Praxis-Bot Users
    """
    id = models.AutoField(primary_key=True)
    randID = models.CharField(max_length=300)
    nickname = models.CharField(max_length=300)
    pin = models.CharField(max_length=300, blank=True, default="")
    isAdmin = models.BooleanField(default=False)
    isMod = models.BooleanField(default=False)
    groups = models.CharField(max_length=500, blank=True, default="")
    isBanned = models.BooleanField(default=False)
    isMuted = models.BooleanField(default=False)
    isSubscriber = models.BooleanField(default=False)
    isDonator = models.BooleanField(default=False)
    isVIP = models.BooleanField(default=False)
    discordID = models.CharField(max_length=300, blank=True, default="")
    twitchID = models.CharField(max_length=300, blank=True, default="")
    twitterID = models.CharField(max_length=300, blank=True, default="")
    pgpPublicKey = models.TextField(max_length=16384, blank=True, default="")

    def __str__(self):
        return ""

class PraxisBot_UserGroups(models.Model):
    """
    This model will define Praxis-Bot UserGroups
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)