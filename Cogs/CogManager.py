from discord.ext import commands


class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, module: str):
        try:
            self.bot.load_extension(f"Cogs.{module}")
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(f"Loaded!")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, module: str):
        try:
            self.bot.unload_extension(f"Cogs.{module}")
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(f"Unloaded!")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, module: str):
        try:
            self.bot.unload_extension(f"Cogs.{module}")
            self.bot.load_extension(f"Cogs.{module}")
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(f"Reloaded!")


def setup(bot):
    bot.add_cog(CogManager(bot))
