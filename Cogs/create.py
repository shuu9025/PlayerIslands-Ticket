import asyncio
import datetime

import discord
from discord.ext import commands

from Exceptions import NotLinkedException
from utilty import id_to_uuid, uuid_to_mcid, getservername


class CreateTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="new", aliases=["create", "ticket"])
    @commands.guild_only()
    async def new(self, ctx, *, content="なし"):
        if ctx.message.channel.id != 699965047316676689:
            message = await ctx.send("Ticketチャンネルではありません！")
        else:
            channel = discord.utils.get(ctx.guild.text_channels, name=f"ticket-{ctx.author.id}")
            if channel is None:
                owner = ctx.guild.get_role(686761216567148550)
                admin = ctx.guild.get_role(686760653754859601)
                mod = ctx.guild.get_role(690605575998013471)
                helper = ctx.guild.get_role(691893306619199488)
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                              manage_permissions=True),
                    owner: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    admin: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    mod: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    helper: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                }
                if content.startswith("mod") or content.startswith("moderator"):
                    del overwrites[helper]
                elif content.startswith("admin"):
                    del overwrites[helper]
                    del overwrites[mod]
                channel = await ctx.guild.create_text_channel(
                    name=f"ticket-{ctx.author.id}",
                    category=ctx.message.channel.category,
                    overwrites=overwrites
                )
                embed = discord.Embed(
                    title="Ticketを作成しました",
                    description=content,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(
                    name="プレイヤー名",
                    value=f"取得中…"
                )
                embed.add_field(
                    name="サーバー名",
                    value=f"取得中…"
                )
                embed.add_field(
                    name="注意",
                    value="少なくともサーバー名、エラー、MCIDを記入してください。\n"
                          "必要な情報が記載されていない場合、サポートを受けることはできません。",
                    inline=False
                )
                embed.set_author(
                    name=str(ctx.author.name),
                    icon_url=ctx.author.avatar_url
                )
                ticketmessage = await channel.send(content=ctx.author.mention, embed=embed)
                notify = discord.utils.get(ctx.guild.text_channels, name="ticket-notify")
                notifyembed = discord.Embed(
                    title="Ticketが作成されました",
                    description=content,
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Color.blue()
                )
                notifyembed.add_field(
                    name="作成者",
                    value=f"{ctx.author.mention}\n"
                          f"({ctx.author.id})"
                )
                notifyembed.add_field(
                    name="MCID",
                    value=f"取得中…",
                    inline=False
                )
                notifyembed.add_field(
                    name="サーバー名",
                    value=f"取得中…"
                )
                notifyembed.add_field(
                    name="チャンネル",
                    value=channel.mention
                )
                notifymessage = await notify.send(embed=notifyembed)
                message = await ctx.send(f"Ticketチャンネルを作成しました: {channel.mention}")
                try:
                    uuid = await id_to_uuid(ctx.author.id)
                    mcid = await uuid_to_mcid(uuid)
                    servername = await getservername(mcid)
                except:
                    uuid = "None"
                    mcid = "None"
                    servername = "None"
                notifyembed.clear_fields()
                notifyembed.add_field(
                    name="作成者",
                    value=f"{ctx.author.mention}\n"
                          f"({ctx.author.id})"
                )
                notifyembed.add_field(
                    name="MCID",
                    value=f"`{mcid}`\n"
                          f"(`{uuid}`)",
                    inline=False
                )
                notifyembed.add_field(
                    name="サーバー名",
                    value=f"{servername}"
                )
                notifyembed.add_field(
                    name="チャンネル",
                    value=channel.mention
                )
                embed.clear_fields()
                embed.add_field(
                    name="プレイヤー名",
                    value=f"`{mcid}`\n"
                          f"(`{uuid}`)"
                )
                embed.add_field(
                    name="サーバー名",
                    value=f"{servername}"
                )
                embed.add_field(
                    name="注意",
                    value="少なくともサーバー名、エラー、MCIDを記入してください。\n"
                          "必要な情報が記載されていない場合、サポートを受けることはできません。",
                    inline=False
                )
                await ticketmessage.edit(embed=embed)
                await notifymessage.edit(embed=notifyembed)
            else:
                message = await ctx.send(f"既にTicketチャンネルが作成されています: {channel.mention}")
        await asyncio.sleep(10)
        await message.delete()


def setup(bot):
    bot.add_cog(CreateTicket(bot))
