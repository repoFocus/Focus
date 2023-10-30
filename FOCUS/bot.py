import discord
from discord import app_commands, ui, Webhook
import fileread
import management
import requests
import time

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

swapW = None
transferW = None

currentChain = ""

config = fileread.getConfig()
emojis = fileread.getEmojis()

async def updateProfile():
        walletList = fileread.getWalletList()
        if client.user.name != "FOCUS":
            avatar = requests.get("https://cdn.discordapp.com/attachments/957246380915703828/1131348560022089898/image.png").content
            await client.user.edit(username="FOCUS", avatar=avatar)
        if len(walletList) > 1:
            activity = discord.Activity(type=discord.ActivityType.listening, name="{} wallets".format(len(walletList)))
            await client.change_presence(status=discord.Status.online, activity=activity)
        else:
            activity = discord.Activity(type=discord.ActivityType.listening, name="{} wallets".format(len(walletList)))
            await client.change_presence(status=discord.Status.online, activity=activity)

class DeleteThread(discord.ui.View):
    @discord.ui.button(label="Delete thread", style=discord.ButtonStyle.danger) 
    async def button_callback(self, button, interaction):
        await button.channel.delete()

class AddWallet(ui.Modal, title='Add wallet'):
    global currentChain
    adr = ui.TextInput(label='Address', placeholder="0x0000000000000000000000000000000000000000", style=discord.TextStyle.short)
    name = ui.TextInput(label='Name', placeholder="Joe", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        add = management.addWallet(self.adr, self.name, currentChain)
        if add == "Existing":
            await interaction.response.send_message(f':x: Error while adding *{self.adr}* as **{self.name}** to the list ! The adress is already in the list !', delete_after=10, ephemeral=True)
        elif add == "Error":
            await interaction.response.send_message(f':x: Error while adding *{self.adr}* as **{self.name}** to the list ! Try to put a correct address !', delete_after=10, ephemeral=True)
        elif add == "Over500":
            await interaction.response.send_message(f':x: You reach the limit of 500 address !', delete_after=10, ephemeral=True)
        elif add != "Error":
            await interaction.response.send_message(f':white_check_mark: Sucefully add *{self.adr}* as **{self.name}** to the list !', delete_after=10, ephemeral=True)
        await updateProfile()     

class RemoveWallet(ui.Modal, title='Remove wallet'):
    adr = ui.TextInput(label='Address', placeholder="0x0000000000000000000000000000000000000000", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        remove = management.removeWallet(self.adr)
        if remove == "Inexisting":
            await interaction.response.send_message(f':x: Error while removing *{self.adr}* to the list ! The address is not in the list !', delete_after=10, ephemeral=True)
        elif remove == "Error":
            await interaction.response.send_message(f':x: Error while removing *{self.adr}* to the list ! Try to put a correct address !', delete_after=10, ephemeral=True)
        elif remove != "Error":
            await interaction.response.send_message(f':white_check_mark: Sucefully remove *{self.adr}* from the list !', delete_after=10, ephemeral=True)
        await updateProfile()    

class Select(discord.ui.Select):
    
    def __init__(self):
        emojis = fileread.getEmojis()

        ethEmoji = client.get_emoji(emojis["ETH_EMOJI_ID"])
        arbEmoji = client.get_emoji(emojis["ARB_EMOJI_ID"])
        bnbEmoji = client.get_emoji(emojis["BNB_EMOJI_ID"])
        

        options=[
            discord.SelectOption(label="ETH",emoji=ethEmoji,description="Etherum Chain"),
             discord.SelectOption(label="ARB",emoji=arbEmoji,description="Arbitrum Chain"),
              discord.SelectOption(label="BNB",emoji=bnbEmoji,description="BNB Chain")
            ]
        super().__init__(placeholder="Select a chain",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        global currentChain
        if self.values[0] == "ETH":
            currentChain = "ETH"
        if self.values[0] == "ARB":
            currentChain = "ARB"
        if self.values[0] == "BNB":
            currentChain = "BNB"
        await interaction.response.send_modal(AddWallet())
            
        

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

@tree.command(name = "setup", description = "Setup the bot on a discord server.")
async def command(interaction):
    global swapW
    global transferW
    config = fileread.getConfig()

    if config["SETUPED"] == "False":
        if interaction.user.id == interaction.guild.owner_id:

            await interaction.response.send_message(f'Sucefully setup the server !', delete_after=10, ephemeral=True)

            guild = client.get_guild(interaction.guild.id)
            
            uniswapEmojiImage = requests.get("https://cdn.discordapp.com/attachments/1150204233707171903/1150204416071315568/1779-uniswap.png").content
            ethEmojiImage = requests.get("https://cdn.discordapp.com/attachments/1150204233707171903/1153003522271498320/5819-eth.png").content
            arbEmojiImage = requests.get("https://cdn.discordapp.com/attachments/1150204233707171903/1153022332332425266/62fb88dbd2721c64b22677c0_arbitrum_logo.png").content
            bnbEmojiImage = requests.get("https://cdn.discordapp.com/attachments/1150204233707171903/1153022582208069692/bnb-chain-binance-smart-chain-logo.png").content

            uniswapEmoji = await guild.create_custom_emoji(name="UniswapLogoButtonFocus", image=uniswapEmojiImage)
            ethEmoji = await guild.create_custom_emoji(name="EthLogoChainFocus", image=ethEmojiImage)
            arbEmoji = await guild.create_custom_emoji(name="ArbLogoChainFocus", image=arbEmojiImage)
            bnbEmoji = await guild.create_custom_emoji(name="BnbLogoChainFocus", image=bnbEmojiImage)

            category = await guild.create_category("focus")
            swap = await guild.create_text_channel("SWAP", category=category, topic="FOCUS - Here, swaps will be outpout")
            transfer = await guild.create_text_channel("TRANSFERS", category=category, topic="FOCUS - Here, transfers will be outpout")
            command = await guild.create_text_channel("COMMANDS", category=category, topic="FOCUS - Here, you will put your command")
            management.editJSONUrl(uniswapEmoji, ethEmoji, arbEmoji, bnbEmoji, swap, transfer, command, category, guild)

        else:
            await interaction.response.send_message(f'Only the owner of {interaction.guild.name} can setup the bot to this server !', delete_after=10, ephemeral=True)
    elif config["SETUPED"] == "True":
        if interaction.guild.id == config["GUILD_ID"]:
            await interaction.response.send_message(f'The server is actually setuped !\n<#{config["SWAP_ID"]}>\n<#{config["TRANSFERT_ID"]}>\n<#{config["COMMAND_ID"]}>', delete_after=20, ephemeral=True)
        else:
            await interaction.response.send_message(f'You can only use the bot on one server !', delete_after=10, ephemeral=True)

@tree.command(name = "add", description = "Add wallet")
async def command(interaction):
    config = fileread.getConfig()

    if config["SETUPED"] == "True":
        if interaction.guild.id == config["GUILD_ID"]:
            if interaction.channel.id == config["COMMAND_ID"]:
                await interaction.response.send_message(view=SelectView(), ephemeral=True)
            else:
                await interaction.response.send_message(f'Command need to be send in <#{config["COMMAND_ID"]}> !', delete_after=10, ephemeral=True)
        else:
            await interaction.response.send_message(f'You can only use the bot on one server !', delete_after=10, ephemeral=True)

    elif config["SETUPED"] == "False":
        await interaction.response.send_message(f'You need first to setup the server using */setup* !', delete_after=20, ephemeral=True)

@tree.command(name = "remove", description = "Remove wallet")
async def command(interaction):
    config = fileread.getConfig()

    if config["SETUPED"] == "True":
        if interaction.guild.id == config["GUILD_ID"]:
            if interaction.channel.id == config["COMMAND_ID"]:
                await interaction.response.send_modal(RemoveWallet())
            else:
                await interaction.response.send_message(f'Command need to be send in <#{config["COMMAND_ID"]}> !', delete_after=10, ephemeral=True)
        else:
            await interaction.response.send_message(f'You can only use the bot on one server !', delete_after=10, ephemeral=True)
    elif config["SETUPED"] == "False":
        await interaction.response.send_message(f'You need first to setup the server using */setup* !', delete_after=20, ephemeral=True)

@tree.command(name = "server", description = "Change the bot of server")
async def command(interaction):
    config = fileread.getConfig()

    if config["SETUPED"] == "True":
        if interaction.guild.id == config["GUILD_ID"]:
            if interaction.channel.id == config["COMMAND_ID"]:
                if interaction.user.id == interaction.guild.owner_id:
                    
                    management.clearJSON()
                    await interaction.response.send_message(f'The bot location have been reset ! [ADD](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)', delete_after=10, ephemeral=True)
                else:
                    await interaction.response.send_message(f'Only the owner of {interaction.guild.name} can moove the bot to another server !', delete_after=10, ephemeral=True)
            else:
                await interaction.response.send_message(f'Command need to be send in <#{config["COMMAND_ID"]}> !', delete_after=10, ephemeral=True)
        else:
            await interaction.response.send_message(f'Only the owner of the current bot guild is allowed to moove it !', delete_after=10, ephemeral=True)
    elif config["SETUPED"] == "False":
        await interaction.response.send_message(f'The bot is not setuped, you can moove him ! [ADD](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)', delete_after=20, ephemeral=True)

@tree.command(name = "list", description = "Show the wallet list")
async def command(interaction):
    config = fileread.getConfig()
    walletList = fileread.getWalletList()
    if config["SETUPED"] == "True":
        if interaction.guild.id == config["GUILD_ID"]:
            if interaction.channel.id == config["COMMAND_ID"]:
                if len(walletList) > 0:
                    pages = []
                    content = ""
                    for wallet in walletList:
                        futurContent = content + wallet.name + "```" + wallet.adr + "```\n\n"
                        if len(futurContent) < 2000:
                            content = futurContent
                        else:
                            pages.append(content)
                            content = ""

                    pages.append(content)
                    thread = await interaction.channel.create_thread(name="Wallet List", auto_archive_duration=60)
                    await interaction.response.send_message("Successfully sended the wallet list in <#{}>".format(thread.id), ephemeral=True)

                    for embedContent in pages:
                        await thread.send(embed=discord.Embed(description=embedContent))
                    await thread.send(view=DeleteThread())
                else:
                    await interaction.response.send_message("You have currently 0 wallet in your wallet list, try */add* !", delete_after=10, ephemeral=True)
            else:
                await interaction.response.send_message(f'Command need to be send in <#{config["COMMAND_ID"]}> !', delete_after=10, ephemeral=True)
        else:
            await interaction.response.send_message(f'You can only use the bot on one server !', delete_after=10, ephemeral=True)
    elif config["SETUPED"] == "False":
        await interaction.response.send_message(f'You need first to setup the server using */setup* !', delete_after=20, ephemeral=True)

@client.event
async def on_ready():
        config = fileread.getConfig()
        if config["SETUPED"] == "True":
                ethEmoji = client.get_emoji(emojis["ETH_EMOJI_ID"])
                arbEmoji = client.get_emoji(emojis["ARB_EMOJI_ID"])
                bnbEmoji = client.get_emoji(emojis["BNB_EMOJI_ID"])
                uniswapEmoji = client.get_emoji(emojis["UNISWAP_EMOJI_ID"])
                category = client.get_channel(config["CATEGORY_ID"])
                swap = client.get_channel(config["SWAP_ID"])
                transfert = client.get_channel(config["TRANSFERT_ID"])
                command = client.get_channel(config["COMMAND_ID"])

                await bnbEmoji.delete()
                await arbEmoji.delete()
                await ethEmoji.delete()
                await uniswapEmoji.delete()
                await category.delete()
                await swap.delete()
                await transfert.delete()
                await command.delete()

                management.clearJSON()
        
        
        await updateProfile()
        await tree.sync()
        print("Ready!")

client.run(config["BOT_TOKEN"])