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
    embed.add_field(name='?modhelp', value='Help for Moderator Commands', inline=False)
    embed.add_field(name='?calchelp', value='Help for Calculator Commands', inline=False)
    await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def calchelp(ctx):
    embed=discord.Embed(color=0x00ff00)
    embed.set_author(name='PyBot Calculator Help')
    embed.add_field(name='?a', value='Addition [?a 11 12]', inline=False)
    embed.add_field(name='?s', value='Subtraction [?s 15 13]', inline=False)
    embed.add_field(name='?m', value='Multiplication [?m 15 13]', inline=False)
    embed.add_field(name='?d', value='Division [?d 15 13]', inline=False)
    await ctx.send(embed=embed)

@commands.has_role("Staff")
@bot.command(pass_context = True)
async def modhelp(ctx):
    embed=discord.Embed(color=0x0000ff)
    embed.set_author(name='PyBot Moderation Help')
    embed.add_field(name='?purge', value='Mass deletes messages [?purge 11]', inline=False)
    embed.add_field(name='?warn', value='Warns the mentioned user [?warn @<user> <reason>]', inline=False)
    embed.add_field(name='?kick', value='Kicks the mentioned user [?kick @<user> <reason>]', inline=False)
    embed.add_field(name='?ban', value='Bans the mentioned user [?ban @<user> <reason>]', inline=False)
    await ctx.send(embed=embed)

#Calculator!
#Addition...
@bot.command()
async def a(ctx, numi, numii):
    sum_value = int(numi) + int(numii)
    await ctx.send(str(numi) + ' + ' + str(numii) + ' = ' + str(sum_value))

#Multiplication
@bot.command()
async def m(ctx, numi, numii):
    sum_value = int(numi) * int(numii)
    await ctx.send(str(numi) + ' x ' + str(numii) + ' = ' + str(sum_value))

#Subtraction
@bot.command()
async def s(ctx, numi, numii):
    sum_value = int(numi) - int(numii)
    await ctx.send(str(numi) + ' - ' + str(numii) + ' = ' + str(sum_value))

#Division
@bot.command()
async def d(ctx, numi, numii):
    sum_value = int(numi) / int(numii)
    await ctx.send(str(numi) + ' / ' + str(numii) + ' = ' + str(sum_value))

@bot.command(pass_context = True)
async def clear(ctx,amount):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} message has been deleted."if(int(amount)is 1)else(f"{amount} messages have been deleted."),delete_after=5)
        channel = bot.get_channel(650348478056235014)
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='Mod Command Used!')
        embed.add_field(name='Clear Command used', value=f'{ctx.author.mention} has used `purge` command.')
        await channel.send(embed=embed)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Couldn\'t clear messages', value='Please pass in a amount to clear the messages!', inline=False)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, user: discord.User, *, reason=None):
    await ctx.channel.purge(limit=1)
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name=f'Warning')
    embeda.add_field(name='You were warned in Elite Programmers group for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await ctx.send(str(user) + ' has succesfully been warned for ' + reason)
    channel = bot.get_channel(650348478056235014)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Warn Command used', value=f'{ctx.author.mention} has warned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)  
    
@commands.has_role("Staff")
@bot.command(pass_context=True)
async def kick(ctx, user:discord.Member, *, reason=None):
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name='Kicked!')
    embeda.add_field(name='You were kicked from Elite Programmers Group for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.kick(reason=reason)
    await ctx.send(str(user) + ' has succesfully been kicked for : ' + reason)
    channel = bot.get_channel(650348478056235014)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Kick Command used', value=f'{ctx.author.mention} has kicked ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)
        
@commands.has_role("Staff")
@bot.command(pass_context=True)
async def ban(ctx, user:discord.Member, *, reason=None):
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name='Kicked!')
    embeda.add_field(name='You were kicked from Elite Programmers Group for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.ban(reason=reason)
    await ctx.send(str(user) + ' has succesfully been banned for : ' + reason)
    channel = bot.get_channel(650348478056235014)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Ban Command used', value=f'{ctx.author.mention} has banned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

#Note to Self : Use ff0000 as the hex for red color.
#embed = discord.Embed(color=0xff0000)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArguments):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Arguments required!', value='Please pass in all required arguments!', inline=False)
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Command Not Found!', value='The command you requested for was not found in the code, please refer to `?help` for my commands!', inline=False)
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Permissions', value='You don\'t have the permissions to run this command!', inline=False)
        await ctx.send(embed=embed)



bot.run(os.getenv('token'))
