import asyncio
import datetime
import os

import discord
from discord.ext import commands


class CloseTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="close", aliases=["delete", "remove"])
    @commands.guild_only()
    async def close(self, ctx):
        if not ctx.message.channel.name.startswith("ticket-"):
            message = await ctx.send(f"Ticketチャンネルではありません！")
            await asyncio.sleep(5)
            await message.delete()
        else:
            creator = discord.utils.get(ctx.guild.members, id=int(ctx.message.channel.name.replace("ticket-", "")))
            with open(f"{ctx.channel.name}.txt", mode='a') as f:
                f.write(f"{creator}'s ticket was opened at {ctx.channel.created_at} and "
                        f"closed at {datetime.datetime.utcnow()} by {ctx.author}.\n\n")
                async for msg in ctx.message.channel.history(oldest_first=True):
                    f.write(f"[{msg.created_at}] {msg.author}: {msg.clean_content}\n")
            await ctx.channel.delete()
            notify = discord.utils.get(ctx.guild.text_channels, name="ticket-notify")
            if notify is not None:
                with open(f"{ctx.channel.name}.txt", mode='rb') as f:
                    notifyembed = discord.Embed(
                        title="Ticketがクローズされました",
                        timestamp=datetime.datetime.utcnow(),
                        color=discord.Color.red()
                    )
                    notifyembed.add_field(
                        name="Ticket作成者",
                        value=f"{creator.mention}\n"
                              f"({creator.id})"
                    )
                    notifyembed.add_field(
                        name="クローズしたユーザー",
                        value=f"{ctx.author.mention}\n"
                              f"({ctx.author.id})"
                    )
                    notifyembed.add_field(
                        name="チャンネル",
                        value=ctx.channel.name,
                        inline=False
                    )
                    await notify.send(embed=notifyembed, file=discord.File(f))
                with open(f"{ctx.channel.name}.txt", mode="rb") as f:
                    try:
                        channel = await creator.create_dm()
                        await channel.send(embed=notifyembed, file=discord.File(f))
                    except discord.Forbidden:
                        pass
            os.remove(f"{ctx.channel.name}.txt")


def setup(bot):
    bot.add_cog(CloseTicket(bot))
