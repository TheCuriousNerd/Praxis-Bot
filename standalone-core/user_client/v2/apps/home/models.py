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
    text = models.CharField(max_length=500)
    tag = models.CharField(max_length=200)
    isEnabled = models.BooleanField(default=False)

    def __str__(self):
        return self.text + " " + self.tag + " " + str(self.isEnabled)


class PraxisBot_EventLog(models.Model):
    """
    This model will hold the data for the Event Log
    """
    id = models.AutoField(primary_key=True)
    event = models.CharField(max_length=300)
    eventType = models.CharField(max_length=300)
    sourceService = models.CharField(max_length=300) # ie Twitch, Discord, etc.
    user = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.event + " " + self.eventType + " " + self.sourceService + " " + self.user + " " + str(self.time) + " " + self.message

class PraxisBot_Commands_v0(models.Model):
    """
    This model will hold the data for the Command
    """
    id = models.AutoField(primary_key=True)
    command = models.CharField(max_length=200)
    response = models.CharField(max_length=500)
    isEnabled = models.BooleanField(default=False)

    def __str__(self):
        return self.command + " " + self.response + " " + str(self.isEnabled)


class PraxisBot_CommandSyntax_v0_StoredVariables(models.Model):
    """
    This model will hold the data for the Command Syntax
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    data = models.TextField(max_length=1000)
    lastUpdated = models.DateTimeField(auto_now_add=True)
    isEnabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.data + " " + self.lastUpdated + " " + str(self.isEnabled)