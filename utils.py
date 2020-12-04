# Importing modules

import discord
from discord.ext import commands
from json import load
import random as ran
import os
import sys

# Path
mainPath = os.path.join(os.path.dirname(__file__), "main.py") # for cogs
jpath = os.path.join(os.path.dirname(__file__), "settings.json") # for cogs


# Json Config

json = load(open(jpath))
token = json["token"]
prefix = json["prefix"]
author = json["author"]
botName = json["botName"]
botID = json["botID"]
version = json["version"]
description = json["description"]

