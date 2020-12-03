# Importing modules

import discord
from discord.ext import commands
from json import load

# Json Config

json = load(open("settings.json"))
token = json["token"]
prefix = json["prefix"]
author = json["author"]
botName = json["botName"]
botID = json["botID"]
version = json["version"]
description = json["description"]