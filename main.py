import os
import discord
import json
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()
intents.members = True

status = cycle(['Enjoy your time!','Welcome to the server!'])

bot = commands.Bot(command_prefix='/', intents=intents)
levels = {}

# Loads and saves XP and Level data to json file

def load_data():
    with open("levels.json", "r") as file:
        try:
            data = json.load(file)
        except:
            data = {}
    return data

def save_data(data):
    with open("levels.json", "w") as file:
        json.dump(data, file, indent=4)

# Adds pronouns message if one does not exist already

@bot.event
async def on_ready():
    print("Bot is ready.")
    change_status.start()

    channel = bot.get_channel(ID)
    messages = []
    async for message in channel.history(limit=1):
      messages.append(message.content)
    if not messages:
      text= "React with the following emojis to get the corresponding pronoun roles\n\n🔵 He/Him/His\n🟣 She/Her/Hers\n⚪ They/Them/Theirs\n\nDM <@" + str(683620285811130375) + "> for others"
      Moji = await channel.send(text)
      await Moji.add_reaction('🔵')
      await Moji.add_reaction('🟣')
      await Moji.add_reaction('⚪')

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands synced")
    except Exception as e:
        print(e)

# Changes status

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

# Message for when a member joins

@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'Welcome, {member.mention} to the server!')
    await update_channel_name()

# Message for when a user leaves

@bot.event
async def on_member_remove(member):
    await member.guild.system_channel.send(f"{member.mention} has left the server!")
    await update_channel_name()

# Sets channel name to members value

async def update_channel_name():
    guild = bot.get_guild(ID)
    channel = guild.get_channel(ID)
    member_count = len(guild.members) - 3

    if isinstance(channel, discord.VoiceChannel):
        await channel.edit(name=f'Citizens: {member_count}')

# Adds XP for messages

@bot.event
async def on_message(message):
    if not message.author.bot:
        user_id = str(message.author.id)
        if user_id not in levels:
            levels[user_id] = {
                "xp": 0,
                "level": 0
            }
        levels[user_id]["xp"] += 1
        if levels[user_id]["xp"] >= 10*levels[user_id]["level"]:
            levels[user_id]["level"] += 1
            levels[user_id]["xp"] = 0  # Reset XP to 0 after leveling up
            await bot.get_channel(1159107761372667904).send(f"Congratulations {message.author.mention}! You have reached level {levels[user_id]['level']}!")
        save_data(levels)
        await bot.process_commands(message)

# Slash command setup

@bot.tree.command(name="level", description="Check your level!")
async def level(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in levels:
        user_level = levels[user_id]["level"]
        user_xp = levels[user_id]["xp"]

        if (10*levels[user_id]["level"])-user_xp <= 0:
            await interaction.response.send_message(f"You are at level {user_level}!")
        else:
            await interaction.response.send_message(f"You are at level {user_level}, {(10*levels[user_id]['level'])-user_xp} more XP to reach the next level!")
    else:
        await interaction.response.send_message("You haven't earned any XP yet!")

# Prints out a leaderboard when user types /leaderboard

@bot.tree.command(name="leaderboard", description="A full list of all members and their level")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)

    guild = bot.get_guild(1096497428322078873)

    output = ""
    for index, (user_id, user_data) in enumerate(sorted_users, start=1):
        user = guild.get_member(int(user_id))
        nickname = user.nick if user and user.nick else user.name if user else "Unknown User"
        level = user_data['level']
        xp = user_data['xp']

        output += f"{index}. {nickname} - Level {level}, {xp}XP\n----\n"

    if (output) :
        await interaction.response.send_message(output)
    else:
        await interaction.response.send_message("No users found")

# Adds pronoun roles based off of reaction

@bot.event
async def on_raw_reaction_add(payload):
    channel_id = ID 
    if payload.channel_id != channel_id:
        return

    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if user.bot:
        return

    emoji = str(payload.emoji)
    if emoji == "🔵":
        role = discord.utils.get(guild.roles, name="he/him/his")
    elif emoji == "🟣":
        role = discord.utils.get(guild.roles, name="she/her/hers")
    elif emoji == "⚪":
        role = discord.utils.get(guild.roles, name="they/them/theirs")
    else:
        role = None

    if role is not None:
        await user.add_roles(role)

# Removes pronoun roles based off of reaction

@bot.event
async def on_raw_reaction_remove(payload):
    channel_id = ID 
    if payload.channel_id != channel_id:
        return

    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if user.bot:
        return

    emoji = str(payload.emoji)
    if emoji == "🔵":
        role = discord.utils.get(guild.roles, name="he/him/his")
    elif emoji == "🟣":
        role = discord.utils.get(guild.roles, name="she/her/hers")
    elif emoji == "⚪":
        role = discord.utils.get(guild.roles, name="they/them/theirs")
    else:
        role = None

    if role is not None:
        await user.remove_roles(role)

# Runs bot and loads XP and Level data

levels = load_data()
bot.run(TOKEN) # Replace with your Bot Token
