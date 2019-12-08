import discord
from discord.ext import commands, tasks
import os
import random
import json
from discord.utils import get
from itertools import cycle

extension_file = "extensions.json"
with open(extension_file) as file:
    extensions = json.load(file)["extensions"]


def get_prefix(bot, msg):
    prefixes = ['?']

    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot=commands.Bot(case_insensitive=True,command_prefix=get_prefix)
bot.remove_command('help')

status = cycle(['PyBot v1.0!', 'with WoozyDragon', 'VLC Media Player', 'Ludo', 'Snakes and Ladders', 'Space Shuttle', 'ISRO', 'Human Legacy by Ivan Torrent'])

@bot.listen()
async def on_ready():
    change_status.start()
    print("Bot is ready for action")

@tasks.loop(seconds=12)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.listen()
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)
    channel = discord.utils.get(member.guild.channels, name='welcome')
    embed = discord.Embed(color=0xFFFF)
    embed.set_author(name='Welcome to the Server!')
    embed.add_field(name=f'New member!', value=f'{member} has joined this server!', inline=False)
    await channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(color=0xFFFF)
    embed.set_author(name='PyBot Help')
    embed.add_field(name='?modhelp', value='Help for Moderator Commands', inline=False)
    embed.add_field(name='?calchelp', value='Help for Calculator Commands', inline=False)
    embed.add_field(name='?pms', value='PyBot Messaging Service (PMS) [?pms @<user.mention> <your_message_here>]', inline=False)
    embed.add_field(name='?coinflip', value='Flips a coin for you', inline=False)
    embed.add_field(name='?diceroll', value='Rolls a dice', inline=False)
    embed.add_field(name='?suggest', value='Suggest for the server [?suggest <suggestion>]', inline=False)
    embed.add_field(name='?facts', value='Shows some facts about coding', inline=False)
    embed.set_footer(text='PyBot v1')
    await ctx.send(embed=embed)

@bot.command()
async def calchelp(ctx):
    embed=discord.Embed(color=0x00ff00)
    embed.set_author(name='PyBot Calculator Help')
    embed.add_field(name='?a', value='Addition [?a 11 12]', inline=False)
    embed.add_field(name='?s', value='Subtraction [?s 15 13]', inline=False)
    embed.add_field(name='?m', value='Multiplication [?m 15 13]', inline=False)
    embed.add_field(name='?d', value='Division [?d 15 13]', inline=False)
    embed.add_field(name='?sq', value='Squared Number [?sq 15]', inline=False)
    await ctx.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def modhelp(ctx):
    embed=discord.Embed(color=0x0000ff)
    embed.set_author(name='PyBot Moderation Help')
    embed.add_field(name='?clear', value='Mass deletes messages [?clear 11]', inline=False)
    embed.add_field(name='?warn', value='Warns the mentioned user [?warn @<user> <reason>]', inline=False)
    embed.add_field(name='?kick', value='Kicks the mentioned user [?kick @<user> <reason>]', inline=False)
    embed.add_field(name='?ban', value='Bans the mentioned user [?ban @<user> <reason>]', inline=False)
    embed.add_field(name='?mute', value='Mutes the mentioned user [?mute @<user> <reason>]', inline=False)
    await ctx.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def mute(ctx, user:discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    rolerem = discord.utils.get(ctx.guild.roles, name="Member")
    await user.add_roles(role)
    await user.remove_roles(rolerem)
    embed = discord.Embed(color=0xFFFF)
    embed.set_author(name='Muted!')
    embed.add_field(name='You were muted in Elite Programmers Group for : ', value=reason, inline=False)
    await user.send(embed=embed)
    await ctx.send(str(user) + f' has been muted by {ctx.author}')
    channel = bot.get_channel(650348478056235014)
    embeda = discord.Embed(color=0xFFFFFF)
    embeda.set_author(name='Mod Command Used!')
    embeda.add_field(name='Mute Command Used', value=f'{ctx.author.mention} has used `MUTE` command to mute ' + str(user))
    embeda.add_field(name='Reason:', value=reason, inline=False)
    await channel.send(embed=embeda)


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

#Squared Numbers
@bot.command()
async def sq(ctx, num):
    squared_value = int(num) * int(num)
    await ctx.send(str(num) + ' squared is ' + str(squared_value))

@commands.has_role("Staff")
@bot.command()
async def clear(ctx,amount:int=0):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} message has been deleted."if(int(amount)is 1)else(f"{amount} messages have been deleted."),delete_after=5)
        channel = bot.get_channel(650348478056235014)
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='Mod Command Used!')
        embed.add_field(name='Clear Command used', value=f'{ctx.author.mention} has used `purge` command.')
        await channel.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    flip = [
        'You got **heads**',
        'You got **tails**'
    ]

    await ctx.send(random.choice(flip))

@bot.command()
async def diceroll(ctx):
    roll = [
        '1','2','3','4','5','6'
    ]

    await ctx.send(random.choice(roll))

@commands.has_role("Staff")
@bot.command()
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
    embed.add_field(name='Warn Command used', value=f'{ctx.author} has warned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.command()
async def pms(ctx, user: discord.User, *, message=None):
    embed = discord.Embed(color=0xffc0cb)
    embed.set_author(name='You got Mail!')
    embed.add_field(name='Message contents :-', value=message, inline=False)
    embed.add_field(name='Sender :-', value=f'{ctx.author.mention}', inline=False)
    embed.set_footer(text='PyBot Messaging Service (PMS)')
    await user.send(embed=embed)
    await ctx.send(f'{ctx.author.mention}, Succesfully sent your message to ' + str(user) + ' which says : ' + str(message))

@bot.command(pass_context = True)
async def suggest(ctx, *, suggest=None):
    channel = bot.get_channel(648929055151882241)
    embed = discord.Embed(color=0xffff00)
    embed.set_author(name=f'{ctx.author}')
    embed.add_field(name='Suggestion:', value=suggest, inline=False)
    embed.set_footer(text='PyBot Suggestions')
    msg = await channel.send(embed=embed)
    await msg.add_reaction('<:checkmark:653071400495743011>')
    await msg.add_reaction('<:crossmark:653071861244100618>')

@bot.command()
async def facts(ctx):
    fact = [
        'There are still some spacecraft operating on the 70s programs!',
        'There are 698 different coding languages available! If it were a country, it\'d come in 3rd place, behind Indonesia(700)!!!',
        'By far, Python is considered the EASIEST Language to learn, ever made!'
    ]
    await ctx.send(random.choice(fact))

@commands.has_role("Staff")
@bot.command()
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
    embed.add_field(name='Kick Command used', value=f'{ctx.author} has kicked ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def ban(ctx, user:discord.Member, *, reason=None):
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name='Banned!')
    embeda.add_field(name='You were Banned from Elite Programmers Group for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.ban(reason=reason)
    await ctx.send(str(user) + ' has succesfully been banned for : ' + reason)
    channel = bot.get_channel(650348478056235014)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Ban Command used', value=f'{ctx.author} has banned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Command Not Found!', value='The command you requested for was not found in the code, please refer to `?help` for my commands!', inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Permissions', value='You don\'t have the permissions to run this command!', inline=False)
        await ctx.send(embed=embed)



if len(extensions) > 0:
    for ext in extensions:
        try:
            bot.load_extension(ext)
            print(f"Extension {ext} loaded successfully")
        except Exception:
            print(f"Extension {ext} failed to load")

bot.run(os.getenv('token'))
