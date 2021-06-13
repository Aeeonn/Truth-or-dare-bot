import os
import json
import discord
# import crayons
import random
import discord
from discord import Colour
import utils
from datetime import datetime, timedelta

from discord.ext import commands
from discord.utils import oauth_url

import asyncio
from asyncio import sleep

from discord.utils import get
import aiohttp

bot = commands.Bot(command_prefix='+', case_insensitive=True)
bot.remove_command('help')
bot.owner_id = '706669771889967135'


def readJSON(file, key):
    a_file = open(file, "r")
    json_object = json.load(a_file)
    a_file.close()
    return json_object[key]


def owner_or_has_permissions(**perms):
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        permissions = ctx.channel.permissions_for(ctx.author)
        missing = [perm for perm, value in perms.items(
        ) if getattr(permissions, perm, None) != value]
        if not missing:
            return True
        raise commands.MissingPermissions(missing)

    return commands.check(predicate)


@bot.before_invoke
async def log_command(ctx):
    if ctx.invoked_subcommand:
        return
    ts = utils.get_timestamp()
    msg = ctx.message.content.replace(
        ctx.prefix, "", 1)
    chan = f"#{ctx.channel}"
    guild = f"({ctx.guild})"
    user = f"{ctx.author}"
    print(f"{ts} {msg!s} in {chan} {guild} by {user}")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# HELP COMMAND
@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title=f"Bot help commands!",
                          description=f"", color=12320855)
    embed.add_field(name="🎮 Game Commands",
                    value="`coinflip`, `truth`, `dare`", inline=False)

    await ctx.send(embed=embed)


# DARE COMMAND
@bot.command(aliases=["dares", "d"])
async def dare(ctx):
    with open("data/dares.json", "r", encoding="utf-8") as f:
        data_dares = json.load(f)

        qn = random.randint(1, len(data_dares) - 1)

        embed = discord.Embed(title=f"Dare #{qn}", description="\n\n> **{}**".format(
            readJSON("data\\dares.json", "dare" + str(qn))), color=discord.Colour.random())

        await ctx.send(embed=embed)


# TRUTH COMMAND
@bot.command(aliases=["truths", "t"])
async def truth(ctx):
    with open("data/wyr.json", "r", encoding="utf-8") as f:
        data_truths = json.load(f)

        qn = random.randint(1, len(data_truths) - 1)

        embed = discord.Embed(title=f"Truth #{qn}", description="\n\n> **{}**".format(
            readJSON("data\\wyr.json", "wyr" + str(qn))), color=discord.Colour.random())

        await ctx.send(embed=embed)


# WOULD YOU RATHER
@bot.command(aliases=["wouldyourather"])
async def wyr(ctx):
    with open("data/wyr.json", "r", encoding="utf-8") as f:
        data_wyr = json.load(f)

        qn = random.randint(1, len(data_wyr) - 1)

        embed = discord.Embed(title=f"Would You Rather #{qn}", description="\n\n> **{}**".format(
            readJSON("data\\wyr.json", "wyr" + str(qn))), color=discord.Colour.random())

        await ctx.send(embed=embed)


# PARANOIA COMMAND
@bot.command(aliases=["p", "para"])
async def paranoia(ctx, user: discord.User):
    with open("data/paranoia.json", "r", encoding="utf-8") as f:
        data_paranoia = json.load(f)
        qn = random.randint(0, len(data_paranoia) - 1)
        message = f"```fix\n{data_paranoia[qn]['paranoia']}\n```"

        embed = discord.Embed(
            title=f"Paranoia from {ctx.message.author.name}", description=f"The dare you got is: \n\n{message}")
        await user.send(embed=embed)


# COINFLIP COMMAND
@bot.command(aliases=["cf"])
async def coinflip(ctx):
    choice = random.randint(0, 1)
    if choice == 1:
        result = "Heads"
    else:
        result = "Tails"
    embed = discord.Embed(title=f"{result}",
                          description=f"")
    await ctx.send(embed=embed)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Lmao"))
        await asyncio.sleep(300)


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    ts = utils.get_timestamp()
    print(f"{ts} Logged in as {bot.user} (ID {bot.user.id})")
    owner = bot.get_user(bot.owner_id)
    try:
        print("Ready!")
        bot.loop.create_task(status_task())
    except discord.HTTPException:
        pass


@bot.event
async def on_command_error(ctx, error):
    ts = utils.get_timestamp()
    print(f"{ts} {error.__class__.__name__} {error}")
    if isinstance(error, commands.NotOwner):
        await ctx.send("**Restricted command.**", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace(
            'guild', 'server').title() for perm in error.missing_perms]
        await ctx.send(f"You are missing {missing} permission(s) to run this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(error)


def get_token(*, test=False):
    token = os.getenv(
        "")
    if token:
        return token
    path = ".token"
    if test:
        path += "-test"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


if __name__ == '__main__':
    import sys
    test = "--test" in sys.argv
    if test:
        bot.command_prefix = "-"
    bot.run(get_token(test=test))
