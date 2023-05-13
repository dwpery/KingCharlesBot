import os
import discord
from discord.ext import commands
from numpy import random
from keep_alive import keep_alive

client = commands.Bot(command_prefix="/")
token = os.environ['token']

# Makes sure the bot loads


@client.event
async def on_ready():
    print("loaded")


# Basic intro to the Bot's commands
"""
@client.command()
async def hello(ctx):
    await ctx.send(
        "Idea Bot is ready and waiting, just type !idea for an idea in one of your text channels!"
    )
"""

# Authorizes and runs the bot

keep_alive()
client.run(token)
