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

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)
    channel = discord.utils.get(member.guild.channels, name='welcome')
    embed = discord.Embed(color=0xFFFF)
    embed.set_author(name='Welcome to the Server!')
    embed.add_field(name=f'New member!', value=f'{member} has joined this server!', inline=False)
    await channel.send(embed=embed)

@bot.command(pass_context = True)
async def help(ctx):
    embed=discord.Embed(color=0xFFFF)
    embed.set_author(name='PyBot Help')
    embed.add_field(name='No help added!', value='Bot is refreshed', inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def purge(ctx,amount:int=10):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"<:clear:613146626558525495> {amount} message has been deleted."if(int(amount)is 1)else(f"<:clear:613146626558525495> {amount} messages have been deleted."),delete_after=5)
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='Mod Command Used!')
        embed.add_field(name='Purge Command used', value=f'{ctx.author} has used `purge` command.')
        await ctx.send(bot.get_channel('650348478056235014'), embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, user: discord.User, *, reason=None):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(color=0xFFFF)
    embed.set_author(name=f'Warning')
    embed.add_field(name='You were warned in Elite Programmers group for :', value=reason, inline=False)
    await user.send(embed=embed)
    await ctx.send(str(user) + ' has succesfully been warned for ' + reason)

bot.run(process.env.token)
