import asyncio
import datetime
import os

import discord
from discord.ext import commands, tasks

from utilty import user_friendly_time


class CloseSchedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    @commands.command()
    @commands.guild_only()
    async def closeschedule(self, ctx, close_time: user_friendly_time):
        if not ctx.message.channel.name.startswith("ticket-"):
            message = await ctx.send(f"Ticketチャンネルではありません！")
            await asyncio.sleep(5)
            await message.delete()
            return
        now = datetime.datetime.utcnow()
        closeat = now + close_time
        await ctx.channel.edit(topic=closeat.strftime("%Y/%m/%d %H:%M:%S"))
        await ctx.send(f"クローズ予約: {(closeat + datetime.timedelta(hours=9)).strftime('%Y/%m/%d %H:%M:%S')} (JST) にTicketを自動でクローズします。")

    @tasks.loop(seconds=1.0)
    async def loop(self):
        now = datetime.datetime.utcnow()
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if isinstance(channel, discord.TextChannel):
                    if channel.topic in [None, ""]:
                        continue
                    try:
                        closetime = datetime.datetime.strptime(channel.topic, "%Y/%m/%d %H:%M:%S")
                        if now >= closetime:
                            print(f"{channel.name} ({channel.id})")
                            creator = discord.utils.get(guild.members,
                                                        id=int(channel.name.replace("ticket-", "")))
                            with open(f"{channel.name}.txt", mode='a') as f:
                                f.write(f"{creator}'s ticket was opened at {channel.created_at} and "
                                        f"auto closed at {datetime.datetime.utcnow()}.\n\n")
                                async for msg in channel.history(oldest_first=True):
                                    f.write(f"[{msg.created_at}] {msg.author}: {msg.clean_content}\n")
                            await channel.delete()
                            notify = discord.utils.get(guild.text_channels, name="ticket-notify")
                            if notify is not None:
                                with open(f"{channel.name}.txt", mode='rb') as f:
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
                                        value=f"{guild.me.mention}\n"
                                              f"({guild.me.id})"
                                    )
                                    notifyembed.add_field(
                                        name="チャンネル",
                                        value=channel.name,
                                        inline=False
                                    )
                                    await notify.send(embed=notifyembed, file=discord.File(f))
                                with open(f"{channel.name}.txt", mode="rb") as f:
                                    try:
                                        dmchannel = await creator.create_dm()
                                        await dmchannel.send(embed=notifyembed, file=discord.File(f))
                                    except discord.Forbidden:
                                        pass
                            os.remove(f"{channel.name}.txt")
                    except ValueError:
                        continue


def setup(bot):
    bot.add_cog(CloseSchedule(bot))
