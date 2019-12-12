import discord
from discord.ext import commands, tasks
import os
import random
import json
import math
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

status = cycle(['PyBot v1.0!', 'with WoozyDragon', 'VLC Media Player', 'Ludo', 'Snakes and Ladders', 'Space Shuttle', 'ISRO', 'Human Legacy by Ivan Torrent', '?help | Commands Help!'])

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
    embed = discord.Embed(
        title="A new Member!",
        description=f"{member} has joined {member.guild.name}",
        color=0xFFFF
    )
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

    logchanl = discord.utils.get(member.guild.channels, name='logs')
    embeda = discord.Embed(
        title=f"Role Assigned to New Member",
        description=f"{role} role was given to {member} for joining the server",
        color=0x00FF00
    )
    await logchanl.send(embed=embeda)

    await member.create_dm()
    emb = discord.Embed(
        title=f"A Warm Welcome!",
        color=0xFFFF
    )
    emb.add_field(name='This is your Captain Speaking,', value=f'A Warm welcome to {member.guild.name}!', inline=False)
    emb.add_field(name='Things', value='We got a load of things to show to you in our server!', inline=False)
    emb.add_field(name='Rules', value='But before you start chatting and all, be sure to read the rules at #rules!', inline=False)
    await member.dm_channel.send(embed=emb)

@bot.command()
async def calchelp(ctx):
    """
    Displays help about some Calculator commands.
    """
    embed=discord.Embed(color=0xffa500)
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
    """
    Displays help about some Moderation Commands.
    """
    embed=discord.Embed(color=0xffa500)
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
    """
    Mutes the Mentioned user
    """
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    rolerem = discord.utils.get(ctx.guild.roles, name="Member")
    await user.add_roles(role)
    await user.remove_roles(rolerem)
    embeda = discord.Embed(
        title="Muted!",
        description="Sorry mate, but you were muted, heres why:-",
        color=0xFFFF
    )
    embed.add_field(name=f'You were muted in {ctx.guild.name} for : ', value=reason, inline=False)
    await user.send(embed=embed)
    await ctx.send(str(user) + f' has been muted by {ctx.author}')
    channel = discord.utils.get(ctx.guild.channels, name='logs')
    embeda = discord.Embed(
        title="Moderator Command Used!",
        color=0x00FF00
    )
    embeda.add_field(name='Mute Command Used', value=f'{ctx.author.mention} has used `MUTE` command to mute {user}', inline=False)
    embeda.add_field(name='Reason:', value=reason, inline=False)
    await channel.send(embed=embeda)


#Calculator!
#Addition...
@bot.command()
async def a(ctx, numi, numii):
    """Addition of Two Integers"""
    sum_value = int(numi) + int(numii)
    await ctx.send(str(numi) + ' + ' + str(numii) + ' = ' + str(sum_value))

#Multiplication
@bot.command()
async def m(ctx, numi, numii):
    """Multiplication of Two Integers"""
    sum_value = int(numi) * int(numii)
    await ctx.send(str(numi) + ' x ' + str(numii) + ' = ' + str(sum_value))

#Subtraction
@bot.command()
async def s(ctx, numi, numii):
    """Subtraction of Two Integers"""
    sum_value = int(numi) - int(numii)
    await ctx.send(str(numi) + ' - ' + str(numii) + ' = ' + str(sum_value))

#Division
@bot.command()
async def d(ctx, numi, numii):
    """Division of Two Integers"""
    sum_value = int(numi) / int(numii)
    await ctx.send(str(numi) + ' / ' + str(numii) + ' = ' + str(sum_value))

#Squared Numbers
@bot.command()
async def sq(ctx, num):
    """Squared Value of one integer"""
    squared_value = int(num) * int(num)
    await ctx.send(str(num) + ' squared is ' + str(squared_value))

#Pythogoreas Theorem
@bot.command()
async def pt(ctx, base, height):
    """Pythagoreas Theorem - Finds the 3rd side/Hypotenuse of a Right Angled Triangle [p^2 + b^2 = h^2]"""
    base_sq = int(base) * int(base)
    height_sq = int(height) * int(height)
    hypotenuse_sq = int(base_sq) + int(height_sq)
    await ctx.send('Third Side/Hypotenuse is = %f' % math.sqrt(hypotenuse_sq))

@bot.command()
async def rate(ctx, rating, *, remarks=None):
    """Rate the Server on a basis of 0-10"""
    ratescore = 100
    avg = int(rating) / int(ratescore)
    channel = discord.utils.get(ctx.guild.channels, name='server-ratings')
    embed = discord.Embed(
        title=f"Rating from {ctx.author}",
        description=f"{rating}/{ratescore}",
        color=0x000075
    )
    embed.add_field(name='Extra Remarks :-', value=remarks, inline=False)
    await channel.send(embed=embed)
    await ctx.send(f'Your rating has succesfully been recorded, {ctx.author.mention}')

@commands.has_role("Staff")
@bot.command()
async def clear(ctx,amount:int=0):
    """Used to clear a certain amount of messages"""
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} message has been deleted."if(int(amount)is 1)else(f"{amount} messages have been deleted."),delete_after=5)
        channel = discord.utils.get(ctx.guild.channels, name='logs')
        embed = discord.Embed(
            title="Moderator Command Used!",
            description="Purge Command Used",
            color=0x00FF00
        )
        embed.add_field(name='Moderator', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Channel', value=f'#{ctx.channel}', inline=False)
        embed.add_field(name='Amount', value=f'{amount}', inline=False)
        await channel.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    """Flip a Coin"""
    flip = [
        'You got **heads**',
        'You got **tails**'
    ]

    await ctx.send(random.choice(flip))

@bot.command()
async def diceroll(ctx):
    """Roll a Dice"""
    roll = [
        '1','2','3','4','5','6'
    ]

    await ctx.send(random.choice(roll))

@commands.has_role("Staff")
@bot.command()
async def warn(ctx, user: discord.User, *, reason=None):
    """Warns the Mentioned user"""
    await ctx.channel.purge(limit=1)
    embeda = discord.Embed(
        title="Warning",
        description=f"Here's all information about your warning",
        color=0xFFFF
    )
    embeda.add_field(name=f'Server', value=f'{ctx.guild.name}', inline=False)
    embeda.add_field(name=f'Moderator', value=f'{ctx.author.mention}', inline=False)
    embeda.add_field(name='Reason', value=reason, inline=False)
    await user.send(embed=embeda)
    await ctx.send(str(user) + ' has succesfully been warned for ' + reason)
    channel = discord.utils.get(ctx.guild.channels, name='logs')
    embed = discord.Embed(
        title="Moderator Command Used!",
        color=0x00FF00
    )
    embed.add_field(name='Warn Command used', value=f'{ctx.author} has warned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.command()
async def pms(ctx, user: discord.User, *, message=None):
    """Sends a Private/Direct Message to the Mentioned User"""
    embed = discord.Embed(
        title="You got Mail!",
        description="You have (1) new message.",
        color=0xffff00
    )
    embed.add_field(name='Message contents :-', value=message, inline=False)
    embed.add_field(name='Sender :-', value=f'{ctx.author.mention}', inline=False)
    embed.add_field(name='Server :-', value=f'{ctx.guild.name}', inline=False)
    embed.set_footer(text='PyBot Messaging Service (PMS)')
    await user.send(embed=embed)
    await ctx.send(f'{ctx.author.mention}, Succesfully sent your message to ' + str(user) + ' which says : ' + str(message))

@bot.command(pass_context = True)
async def suggest(ctx, *, suggest=None):
    """Used to suggest for the server"""
    channel = discord.utils.get(ctx.guild.channels, name='suggestions')
    embed = discord.Embed(color=0xffff00)
    embed.set_author(name=f'{ctx.author}')
    embed.add_field(name='Suggestion:', value=suggest, inline=False)
    embed.set_footer(text='PyBot Suggestions')
    await channel.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def kick(ctx, user:discord.Member, *, reason=None):
    """Kicks the Mentioned User"""
    embeda = discord.Embed(
        title="Kicked!",
        description="Here's all information about your kick",
        color=0xFFFF
    )
    embeda.add_field(name=f'Server', value=f'{ctx.guild.name}', inline=False)
    embeda.add_field(name='Moderator', value=f'{ctx.author.mention}', inline=False)
    embeda.add_field(name='Reason', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.kick(reason=reason)
    await ctx.send(str(user) + ' has succesfully been kicked for : ' + reason)
    channel = discord.utils.get(ctx.guild.channels, name='logs')
    embed = discord.Embed(
        title="Moderator Command Used!",
        color=0x00FF00
    )
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Kick Command used', value=f'{ctx.author} has kicked ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def ban(ctx, user:discord.Member, *, reason=None):
    """Bans the Mentioned User"""
    embeda = discord.Embed(
        title="Banned!",
        description="Here's all information regarding your ban.",
        color=0xFFFF
    )
    embeda.add_field(name=f'Server', value=f'{ctx.guild.name}', inline=False)
    embeda.add_field(name='Moderator', value=f'{ctx.author.mention}', inline=False)
    embeda.add_field(name='Reason', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.ban(reason=reason)
    await ctx.send(str(user) + ' has succesfully been banned for : ' + reason)
    channel = discord.utils.get(ctx.guild.channels, name='logs')
    embed = discord.Embed(
        title="Moderator Command Used!",
        color=0x00FF00
    )
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Ban Command used', value=f'{ctx.author} has banned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error!",
            description="Command not found!",
            color=0xff0000
        )
        embed.add_field(name=f'{ctx.author}', value='The command you requested for was not found in the code, please refer to `?help` for my commands!', inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="Error!",
            description="Lacking Permissions!",
            color=0xff0000
        )
        embed.add_field(name='Permissions', value='You don\'t have the permissions to run this command!', inline=False)
        embed.add_field(name='If you need help...', value='If you need any kind of help, feel free to contact any staff member, thanks :)', inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description="Argument Missing!",
            color=0xff0000
        )
        embed.add_field(name=f"{ctx.author}", value="Main arguments needed to run this command are missing, please refer to the `?help` command for details on this command and which things are required for it to work.", inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Error!",
            description="Invalid Argument",
            color=0xff0000
        )
        embed.add_field(name=f'{ctx.author}', value="Please enter valid arguments which are needed for the command to run, you can refer to `?help` for details on this command. Thanks.", inline=False)
        await ctx.send(embed=embed)

if len(extensions) > 0:
    for ext in extensions:
        try:
            bot.load_extension(ext)
            print(f"Extension {ext} loaded successfully")
        except Exception:
            print(f"Extension {ext} failed to load")

bot.run(os.getenv('token'))
