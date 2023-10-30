import transactionAction as ta
import dsc as discord
import asyncio

def run(transaction):

    JSON = transaction.JSON
    wallet = transaction.wallet

    if JSON:
        notifs = ta.run(JSON)

    if notifs != "Error":
        asyncio.run(discord.notif(notifs, wallet))