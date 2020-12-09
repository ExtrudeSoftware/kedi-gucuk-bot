# Importing modules

import discord
from discord.ext import commands
from json import load
import random as ran
import os
import sys
import time
import asyncio
import requests as req
from bs4 import BeautifulSoup
import ast

# Uptime
start_time = time.time()

# Path
mainPath = os.path.join(os.path.dirname(__file__), "main.py") # for cogs
jpath = os.path.join(os.path.dirname(__file__), "settings.json") # for cogs

# Functions
def pastebinpost(poster:str, syntax:str, content:str):
    payload = {
        "poster":poster,
        "syntax":syntax,
        "content":content
    }

    r = req.post("https://pastebin.ubuntu.com/", payload)

    return "https://pastebin.ubuntu.com" + BeautifulSoup(r.text,"html.parser").find_all("a",{"class":"pturl"})[0].get("href")[:-6]
    

# Json Config
json = load(open(jpath))
token = json["token"]
prefix = json["prefix"]
author = json["author"]
botName = json["botName"]
botID = json["botID"]
version = json["version"]
description = json["description"]

