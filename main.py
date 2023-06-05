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
    channel = bot.get_channel(1115005311984599120)
    messages = await channel.history(limit=123).flatten()
    if messages == []:
      text= "React with the following emojis to get the corresponding pronoun roles\n\n🔵 He/Him/His\n🟣 She/Her/Hers\n⚪ They/Them/Theirs\n\nDM <@" + str(683620285811130375) + "> for others"
      Moji = await channel.send(text)
      await Moji.add_reaction('🔵')
      await Moji.add_reaction('🟣')
      await Moji.add_reaction('⚪')

    
@bot.event
async def on_raw_reaction_add(payload):
    channel_id = 1115005311984599120
    if payload.channel_id != channel_id:
        return

    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if user.bot:
        return

    role_emojis = {
        "🔵": "he/him/his",
        "🟣": "she/her/hers",
        "⚪": "they/them/theirs"
    }

    role_name = role_emojis.get(str(payload.emoji))
    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role is not None:
            await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    channel_id = 1115005311984599120  # Replace with your desired channel ID
    if payload.channel_id != channel_id:
        return

    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if user.bot:
        return

    role_emojis = {
        "🔵": "he/him/his",
        "🟣": "she/her/hers",
        "⚪": "they/them/theirs"
    }

    role_name = role_emojis.get(str(payload.emoji))
    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role is not None:
            await user.remove_roles(role)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    oath_channel = discord.utils.get(member.guild.channels, name="✋-zedlandic-oath")
    subjects_channel = discord.utils.get(member.guild.channels, name="📚-subjects")

    await channel.send(
        f'Welcome, {member.mention} to Zedland! Take the {oath_channel.mention} and tell us your {subjects_channel.mention} to become a citizen!'
    )


@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(
        f'{member.mention} has renounced their Zedlandic citizenship')


keep_alive()
bot.run(token)
