import discord
from discord.ext import commands
import os
from discord.utils import get

def get_prefix(bot, msg):
    prefixes = ['?']

    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot=commands.Bot(case_insensitive=True,command_prefix=get_prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("{} has successfully booted and running!".format(bot.user.name))

@bot.command(pass_context = True)
async def help(ctx):
    embed=discord.Embed(color=0xFFFF)
    embed.set_author(name='PyBot Help')
    embed.add_field(name='No help added!', value='Bot is refreshed', inline=False)
    await ctx.send(embed=embed)



bot.run('NjQ5NTIzMDEyNTIwOTAyNjcx.XeNwLw.Y1R3m2ZxnevOQRNlQv2r-W8FOAE')
