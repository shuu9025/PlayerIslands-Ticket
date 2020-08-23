from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx):
        await ctx.send(f"`-new <要件>`でTicketを作成します。\n"
                       f"`-close`でTicketをクローズします。\n"
                       f"Created by shuu_9025#1141")


def setup(bot):
    bot.add_cog(Help(bot))
