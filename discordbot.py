import asyncio
import logging

import discord
from discord.ext import commands

logger = logging.getLogger("discord")
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="-")
bot.remove_command("help")
bot.load_extension("Cogs.create")
bot.load_extension("Cogs.delete")
bot.load_extension("Cogs.help")
bot.load_extension("Cogs.CogManager")
bot.load_extension("Cogs.onmessage")
bot.load_extension("Cogs.change")
bot.load_extension("Cogs.closeschedule")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="-new"))


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(description=str(error), color=discord.Color.red())
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await msg.delete()

bot.run("Put your bot token here.")
