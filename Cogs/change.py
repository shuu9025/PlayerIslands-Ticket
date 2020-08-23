import asyncio

import discord
from discord.ext import commands


class TicketChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def change(self, ctx, changeto):
        if not ctx.message.channel.name.startswith("ticket-"):
            message = await ctx.send(f"Ticketチャンネルではありません！")
            await asyncio.sleep(5)
            await message.delete()
            return
        owner = ctx.guild.get_role(686761216567148550)
        admin = ctx.guild.get_role(686760653754859601)
        mod = ctx.guild.get_role(690605575998013471)
        helper = ctx.guild.get_role(691893306619199488)
        creator = discord.utils.get(ctx.guild.members, id=int(ctx.message.channel.name.replace("ticket-", "")))
        pi_bot = ctx.guild.get_member(543087007656574986)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            creator: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_permissions=True),
            owner: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            mod: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            helper: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            pi_bot: discord.PermissionOverwrite(read_messages=True)
        }
        if changeto.lower() == "helper":
            pass
        elif changeto.lower() in ["mod", "moderator"]:
            del overwrites[helper]
        elif changeto.lower() == "admin":
            del overwrites[helper]
            del overwrites[mod]
            del overwrites[pi_bot]
        else:
            await ctx.send(f"helper, mod, moderator, adminのいずれかを指定してください！")
        await ctx.message.channel.edit(overwrites=overwrites)
        await ctx.send(f"権限設定を変更しました: {changeto.lower()}")


def setup(bot):
    bot.add_cog(TicketChange(bot))
