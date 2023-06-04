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
    Channel = bot.get_channel(1115005311984599120)
    text= "React with the following emojis to get the corresponding pronoun roles\n\n🔵 He/Him/His\n🟣 She/Her/Hers\n⚪ They/Them/Theirs\n\nDM <@" + str(id) + "> for others"
    Moji = await Channel.send(text)
    await Moji.add_reaction('🔵')
    await Moji.add_reaction('🟣')
    await Moji.add_reaction('⚪')

    
@bot.event
async def on_reaction_add(reaction, user):
    Channel = bot.get_channel(1115005311984599120)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "🔵":
      Role = discord.utils.get(user.guild.roles, name="he/him/his")
      await user.add_roles(Role)
    if reaction.emoji == "🟣":
      Role = discord.utils.get(user.guild.roles, name="she/her/hers")
      await user.add_roles(Role)
    if reaction.emoji == "⚪":
      Role = discord.utils.get(user.guild.roles, name="they/them/theirs")
      await user.add_roles(Role)


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
