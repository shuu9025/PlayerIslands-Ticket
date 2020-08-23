import asyncio

from discord.ext import commands


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await asyncio.sleep(1)
        if message.author == self.bot.user:
            return
        if message.channel.id == 699965047316676689:
            await message.delete()


def setup(bot):
    bot.add_cog(OnMessage(bot))
