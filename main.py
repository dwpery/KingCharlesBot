import os
import discord
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()
intents.members = True

status = cycle(['Glory to Zedland!','Welcome to Zedland!'])

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready.")
    change_status.start()
    channel = bot.get_channel(1115005311984599120)
    messages = []
    async for message in channel.history(limit=1):
      messages.append(message.content)
    if not messages:
      text= "React with the following emojis to get the corresponding pronoun roles\n\n🔵 He/Him/His\n🟣 She/Her/Hers\n⚪ They/Them/Theirs\n\nDM <@" + str(683620285811130375) + "> for others"
      Moji = await channel.send(text)
      await Moji.add_reaction('🔵')
      await Moji.add_reaction('🟣')
      await Moji.add_reaction('⚪')

@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'Welcome, {member.mention} to Zedland (A community for Hereford Sixth Form College Students)! Take the {discord.utils.get(member.guild.channels, name="✋-zedlandic-oath").mention}, tell us your {discord.utils.get(member.guild.channels, name="📚-subjects").mention} and get your {discord.utils.get(member.guild.channels, name="👥-pronouns").mention} to become a citizen!')

@bot.event
async def on_member_remove(member):
    await member.guild.system_channel.send(f"{member.mention} has renounced their Zedlandic Citizenship and left the server!")

@bot.event
async def on_raw_reaction_add(payload):
    channel_id = 1115005311984599120  # ID of the channel with the pronoun message
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

@bot.event
async def on_raw_reaction_remove(payload):
    channel_id = 1115005311984599120  # ID of the channel with the pronoun message
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

bot.run(token)
