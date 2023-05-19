import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
token = os.environ['token']


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    oath_channel = discord.utils.get(member.guild.channels, name="✋-zedlandic-oath")

    await channel.send(
        f'Welcome, {member.mention} to Zedland! Take the {oath_channel.mention} to become a citizen!'
    )


@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(
        f'{member.mention} has renounced their Zedlandic citizenship')


keep_alive()
bot.run(token)
