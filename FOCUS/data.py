class TransactionAction:
    def __init__(self, firstCoin, secondCoin, on, value, transacTo, transacFrom, typeTA):

        self.firstCoin = firstCoin
        self.secondCoin = secondCoin

        self.on = on

        self.value = value
        self.transacTo = transacTo
        self.transacFrom = transacFrom

        self.typeTA = typeTA
        
    def __str__(self):
        if self.typeTA == "Swap":
            if self.secondCoin.dx != None and self.firstCoin.dx != None:
                TransactionAction = "Swap *{}* **[{}]({})** For *{}* **[{}]({})** On __{}__ \n```{} (${}) @ {}\n{} (${}) @ ${}```".format(self.firstCoin.value, self.firstCoin.name, self.firstCoin.dx, self.secondCoin.value, self.secondCoin.name, self.secondCoin.dx, self.on, self.firstCoin.name, self.firstCoin.price, self.firstCoin.fdv, self.secondCoin.name, self.secondCoin.price, self.secondCoin.fdv)
                return TransactionAction
            elif self.secondCoin.dx != None:
                TransactionAction = "Swap *{}* **{}** For *{}* **[{}]({})** On __{}__\n```{} (${}) @ ${}```".format(self.firstCoin.value, self.firstCoin.name, self.secondCoin.value, self.secondCoin.name, self.secondCoin.dx, self.on, self.secondCoin.name, self.secondCoin.price, self.secondCoin.fdv)
                return TransactionAction
            elif self.firstCoin.dx  != None:
                TransactionAction = "Swap *{}* **[{}]({})** For *{}* **{}** On __{}__\n```{} (${}) @ ${}```".format(self.firstCoin.value, self.firstCoin.name, self.firstCoin.dx, self.secondCoin.value, self.secondCoin.name, self.on, self.firstCoin.name, self.firstCoin.price, self.firstCoin.fdv)
                return TransactionAction
            else:
                TransactionAction = "Swap *{}* **{}** For *{}* **{}** On __{}__\n".format(self.firstCoin.value, self.firstCoin.name, self.secondCoin.value, self.secondCoin.name, self.on)
                return TransactionAction
        elif self.typeTA == "Transfer":
            TransactionAction = "Transfer the value of {} **ETH** To [{}](https://debank.com/profile/{}/history)".format(self.value, self.transacTo, self.transacTo)
            return TransactionAction

class DiscordMessage:
    def __init__(self, content, tx, coins, footer, channelID):
        self.content = content
        self.tx = tx
        self.coins = coins
        self.footer = footer
        self.channelID = channelID

class Coin:
    def __init__(self, dx, adr, value, fdv, price, name, json):
        self.dx = dx
        self.adr = adr
        self.value = value
        self.fdv = fdv
        self.price = price
        self.name = name
        self.json = json

class JSONinfo:
    def __init__(self, blockNumber, timeStamp, transacHash, nonce, blockHash, transacIndex, transacFrom, transacTo, value, gas, gasPrice, isError, txreceipt_status, transacInput, contractAddress, cumulativeGasUsed, gasUsed, confirmations, methodId, functionName):

        self.blockNumber = blockNumber
        self.timeStamp = timeStamp
        self.transacHash = transacHash
        self.nonce = nonce
        self.blockHash = blockHash
        self.transacIndex = transacIndex
        self.transacFrom = transacFrom
        self.transacTo = transacTo
        self.value = value
        self.gas = gas
        self.gasPrice = gasPrice
        self.isError = isError
        self.txreceipt_status = txreceipt_status
        self.transacInput = transacInput
        self.contractAddress = contractAddress
        self.cumulativeGasUsed = cumulativeGasUsed
        self.gasUsed = gasUsed
        self.confirmations = confirmations
        self.methodId = methodId
        self.functionName = functionName

class Wallet:
    def __init__(self, name, adr, chain, previousTA, resp):
        self.name = name
        self.adr = adr
        self.chain = chain
        self.previousTA = previousTA
        self.resp = resp

class Transaction:
    def __init__(self, wallet, JSON):
        self.wallet = wallet
        self.JSON = JSON