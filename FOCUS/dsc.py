import discord
from discord import Embed, app_commands, ui
import fileread
import os

config = fileread.getConfig()
emojis = fileread.getEmojis()

async def notif(notifs, wallet):
    print("yo")
    token = config["BOT_TOKEN"]
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    class Buttons(discord.ui.View):
        def __init__(self):
            super().__init__()
        
    @client.event
    async def on_ready():
        for notif in notifs:
            print("yo")
            channel = client.get_channel(int(notif.channelID))

            if channel:
                print("yo")
                embed = discord.Embed(colour=3447003, description=notif.content)
                embed.set_author(name=wallet.name, url="https://debank.com/profile/{}/history".format(wallet.adr))
                embed.set_footer(text=notif.footer)

                view=Buttons()
                view.add_item(discord.ui.Button(label="TX", style=discord.ButtonStyle.link, url=notif.tx))
                for coin in notif.coins:
                    guild = client.get_guild(config["GUILD_ID"])
                    emoji = await guild.fetch_emoji(emojis["UNISWAP_EMOJI_ID"])
                    view.add_item(discord.ui.Button(label=" Buy " + coin.name, style=discord.ButtonStyle.link, url="https://app.uniswap.org/#/swap?outputCurrency=" + coin.adr, emoji=emoji))
                print("aaa")
                await channel.send(embed=embed, view=view)
                print("zzz")
    

        await client.close()

   
    await client.start(token)