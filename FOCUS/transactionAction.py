import cfscrape
import requests
from bs4 import BeautifulSoup
import data as data_
import time
import fileread
from datetime import datetime

config = fileread.getConfig()

def transformNumber(number):
    if type(number) == int:
        abbreviations = [(1e6, 'm'), (1e3, 'k')]

        for value, suffix in abbreviations:
            if number >= value:
                abbreviated_number = '{:.1f}{}'.format(number / value, suffix)
                return abbreviated_number

        return str(number)
    elif type(number) == str:
        if number == "":
            return "N/A"

def run(JSON):  
        
        content = ""

        TransacObject = []
        currentTransaction = []

        transacData = []
        tokenData = []
        tmpArray = []

        url = "https://etherscan.io/tx/" + JSON.transacHash

        scraper = cfscrape.create_scraper()
        response = scraper.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        isSucces = soup.find(class_="badge bg-success bg-opacity-10 border border-success border-opacity-25 text-green-600 fw-medium text-start text-wrap py-1.5 px-2")
        if isSucces:
                nbTransac = soup.find(id="wrapperContent")
                
                if nbTransac:
                    
                            data = nbTransac.find_all(class_="me-1")
                            token = nbTransac.find_all("a")
                            for info in data:
                                transacData.append(str(info.text.strip()))

                            for tokens in token:
                                tokenAdr = tokens["href"]
                                tokenName = tokens.text
                                if tokenAdr.startswith("/token/0x"):
                                    tmpArray.append(tokenAdr[7:49])
                                    tmpArray.append(tokenName)

                            tokenData = [tmpArray[i:i+2] for i in range(0, len(tmpArray), 2)]
                        
                for elements in transacData:
                    if elements == "":
                        transacData.remove(elements)

                allTransaction = [transacData[i:i+8] for i in range(0, len(transacData), 8)]
                if allTransaction != []:
                    
                    
                    for transacFromAllTransaction in allTransaction:
                        currentTransaction.clear()

                        firstCoin = data_.Coin(None, None, None, None, None, None, None)
                        secondCoin = data_.Coin(None, None, None, None, None, None, None)

                        for info in transacFromAllTransaction:
                            currentTransaction.append(info)

                        
                        if currentTransaction[0]:
                                if currentTransaction[0] == "Swap":    
                                            for token in tokenData:
                                                if token[1] == "USDT" or token[1] == "USDC":
                                                    pass
                                                else:
                                                    if token[1] == currentTransaction[2]:
                                                            firstCoin.adr = token[0] 
                                                    
                                                    if token[1] == currentTransaction[5]:
                                                            secondCoin.adr = token[0]
                                                    
                                            i = 3
                                            for letter in currentTransaction[1]:
                                                if letter == ".":
                                                    for decimals in currentTransaction[1]:
                                                            if decimals == ".":
                                                                firstCoin.value = currentTransaction[1][:i]
                                                            else:
                                                                    i = i +1
                                                    break
                                                else:
                                                    firstCoin.value = currentTransaction[1]
                                                    pass

                                            i = 3
                                            for letter in currentTransaction[4]:
                                                if letter == ".":
                                                    
                                                    for decimals in currentTransaction[4]:
                                                            if decimals == ".":
                                                                secondCoin.value = currentTransaction[4][:i]
                                                            else:
                                                                i = i +1
                                                            
                                                    break
                                                else:
                                                    secondCoin.value = currentTransaction[4]
                                                    pass
                                            
                                            if firstCoin.value == "0.00":
                                                firstCoin.value == "~0"
                                                
                                            if secondCoin.value == "0.00":
                                                secondCoin.value = "~0"

                                            if secondCoin.adr != None and firstCoin.adr != None:
                            
                                                    firstURL = requests.get("https://api.dexscreener.com/latest/dex/tokens/" + firstCoin.adr)
                                                    firstCoin.json = firstURL.json()

                                                    secondURL = requests.get("https://api.dexscreener.com/latest/dex/tokens/" + secondCoin.adr)
                                                    secondCoin.json = secondURL.json()

                                                    if secondCoin.json["pairs"] != None and firstCoin.json["pairs"] != None:

                                                        TAdex = currentTransaction[7].lower()

                                                        for pair in firstCoin.json["pairs"]:
                                                            if TAdex.startswith(pair["dexId"]):

                                                                for fields in pair:

                                                                    if fields == "baseToken":
                                                                        for field in pair["baseToken"]:
                                                                            if field == "symbol":
                                                                                firstCoin.name = pair["baseToken"]["symbol"]
                                                                    if fields == "url":
                                                                        firstCoin.dx = pair["url"]
                                                                    if fields == "fdv":
                                                                        firstCoin.fdv = transformNumber(int(pair["fdv"]))
                                                                    if fields == "priceUsd":
                                                                        firstCoin.price = pair["priceUsd"]
                                                        
                                                        if firstCoin.dx == None:
                                                            firstCoin.dx = firstCoin.json["pairs"][0]["url"]

                                                        if firstCoin.fdv == None:
                                                            try:
                                                                firstCoin.fdv = transformNumber(int(firstCoin.json["pairs"][0]["fdv"]))
                                                            except:
                                                                firstCoin.fdv = "N/A"

                                                        if firstCoin.price == None:
                                                                firstCoin.price = firstCoin.json["pairs"][0]["priceUsd"]

                                                        if firstCoin.name == None:
                                                            firstCoin.name == currentTransaction[2]



                                                        for pair in secondCoin.json["pairs"]:
                                                            if TAdex.startswith(pair["dexId"]):

                                                                for fields in pair:

                                                                    if fields == "baseToken":
                                                                        for field in pair["baseToken"]:
                                                                            if field == "symbol":
                                                                                secondCoin.name = pair["baseToken"]["symbol"]
                                                                    if fields == "url":
                                                                        secondCoin.dx = pair["url"]
                                                                    if fields == "fdv":
                                                                        secondCoin.fdv = transformNumber(int(pair["fdv"]))
                                                                    if fields == "priceUsd":    
                                                                        secondCoin.price = pair["priceUsd"]
                                                        
                                                        if secondCoin.dx == None:
                                                            secondCoin.dx = secondCoin.json["pairs"][0]["url"]

                                                        if secondCoin.fdv == None:
                                                            try:
                                                                secondCoin.fdv = transformNumber(int(secondCoin.json["pairs"][0]["fdv"]))
                                                            except:
                                                                secondCoin.fdv = "N/A"
                                                        if secondCoin.price == None:
                                                            secondCoin.price = secondCoin.json["pairs"][0]["priceUsd"]

                                                        if secondCoin.name == None:
                                                            secondCoin.name = currentTransaction[5]


                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac) 

                                                    else:
                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac)

                                            elif secondCoin.adr != None:
                                                    secondURL = requests.get("https://api.dexscreener.com/latest/dex/tokens/" + secondCoin.adr)
                                                    secondCoin.json = secondURL.json()
                                                    
                                                    if secondCoin.json["pairs"] != None:
                                                        
                                                        TAdex = currentTransaction[7].lower()

                                                        for pair in secondCoin.json["pairs"]:
                                                            if TAdex.startswith(pair["dexId"]):
                                                                
                                                                for fields in pair:

                                                                    if fields == "baseToken":
                                                                        for field in pair["baseToken"]:
                                                                            if field == "symbol":
                                                                                secondCoin.name = pair["baseToken"]["symbol"]
                                                                    if fields == "url":
                                                                        secondCoin.dx = pair["url"]
                                                                    if fields == "fdv":
                                                                        secondCoin.fdv = transformNumber(int(pair["fdv"]))
                                                                    if fields == "priceUsd":                                                      
                                                                        secondCoin.price = pair["priceUsd"]
                                                        
                                                        if secondCoin.dx == None:
                                                            secondCoin.dx = secondCoin.json["pairs"][0]["url"]

                                                        if secondCoin.fdv == None:
                                                            try:
                                                                secondCoin.fdv = transformNumber(int(secondCoin.json["pairs"][0]["fdv"]))
                                                            except:
                                                                secondCoin.fdv = "N/A"

                                                        if secondCoin.price == None:
                                                            secondCoin.price = secondCoin.json["pairs"][0]["priceUsd"]

                                                        if secondCoin.name == None:
                                                            secondCoin.name = currentTransaction[5]
                                                        
                                                        firstCoin.name = currentTransaction[2]

                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac)  

                                                    else:
                                                        
                                                        firstCoin.name = currentTransaction[2]

                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac)

                                            elif firstCoin.adr != None:
                                                    firstURL = requests.get("https://api.dexscreener.com/latest/dex/tokens/" + firstCoin.adr)
                                                    firstCoin.json = firstURL.json()
                                                    
                                                    TAdex = currentTransaction[7].lower()
                                                    if firstCoin.json["pairs"] != None:

                                                        for pair in firstCoin.json["pairs"]:
                                                            if TAdex.startswith(pair["dexId"]):

                                                                for fields in pair:

                                                                    if fields == "baseToken":
                                                                        for field in pair["baseToken"]:
                                                                            if field == "symbol":
                                                                                firstCoin.name = pair["baseToken"]["symbol"]
                                                                    if fields == "url":
                                                                        firstCoin.dx = pair["url"]
                                                                    if fields == "fdv":
                                                                        firstCoin.fdv = transformNumber(int(pair["fdv"]))
                                                                    if fields == "priceUsd":
                                                                        firstCoin.price = pair["priceUsd"]

                                                        
                                                        if firstCoin.dx == None:
                                                            firstCoin.dx = firstCoin.json["pairs"][0]["url"]

                                                        if firstCoin.fdv == None:
                                                            try:
                                                                firstCoin.fdv = transformNumber(int(firstCoin.json["pairs"][0]["fdv"]))
                                                            except:
                                                                firstCoin.fdv = "N/A"

                                                        if firstCoin.price == None:
                                                            firstCoin.price = firstCoin.json["pairs"][0]["priceUsd"]

                                                        if firstCoin.name == None:
                                                            firstCoin.name == currentTransaction[2]
                                                        
                                                        secondCoin.name = currentTransaction[5]

                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac) 

                                                    else:

                                                        secondCoin.name = currentTransaction[5]

                                                        Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                        TransacObject.append(Transac) 

                                            if firstCoin.adr == None and secondCoin.adr == None:

                                                    firstCoin.name = currentTransaction[2]
                                                    secondCoin.name = currentTransaction[5]

                                                    Transac = data_.TransactionAction(firstCoin, secondCoin, currentTransaction[7], None, None, None, "Swap") 
                                                    TransacObject.append(Transac) 
                                else:
                                    print("Not supported tx type", currentTransaction)
                                    return "Error"
                                    
                else:
                        Transac = data_.TransactionAction(None, None, None, JSON.value, JSON.transacTo, JSON.transacFrom, "Transfer") 
                        TransacObject.append(Transac) 
                        print("Transfer")

                global swapContent
                global transfertContent
                config = fileread.getConfig()
                swapContent = ""
                transfertContent = ""
                swapEmbed = []
                transfertEmbed = []
                coins = []
                discordMessages = []

                for TAobject in TransacObject:
                    if TAobject.typeTA == "Swap":
                        if len(swapContent) + len(str(TAobject)) + 1 < 2000:
                            swapContent = swapContent + str(TAobject) + "\n"

                            if TAobject.firstCoin.adr:
                                alreadyAdded = False
                                for coin in coins:
                                    if coin.adr == TAobject.firstCoin.adr:
                                        alreadyAdded = True
                                if alreadyAdded == False:
                                    coins.append(TAobject.firstCoin)

                            if TAobject.secondCoin.adr:
                                alreadyAdded = False
                                for coin in coins:
                                    if coin.adr == TAobject.secondCoin.adr:
                                        alreadyAdded = True
                                if alreadyAdded == False:
                                    coins.append(TAobject.secondCoin)
                        else:
                            swapID = config["SWAP_ID"]
                            if swapID != "":
                                swapMessage = data_.DiscordMessage(swapContent, "https://etherscan.io/tx/" + JSON.transacHash, coins, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), swapID)
                                discordMessages.append(swapMessage)
                                swapContent = ""
                                swapContent = swapContent + str(TAobject) + "\n"

                    elif TAobject.typeTA == "Transfer":
                        if len(transfertContent) + len(str(TAobject)) + 1 < 2000:
                            transfertContent = transfertContent + str(TAobject) + "\n"
                        else:
                            transfertID = config["TRANSFERT_ID"]
                            if transfertID != "":
                                transfertMessage = data_.DiscordMessage(transfertContent, "https://etherscan.io/tx/" + JSON.transacHash, [], datetime.today().strftime('%Y-%m-%d %H:%M:%S'), transfertID)
                                discordMessages.append(transfertMessage)
                                transfertContent = ""
                                transfertContent = transfertContent + str(TAobject) + "\n"

                if swapContent:
                    swapID = config["SWAP_ID"]
                    if swapID != "":
                        swapMessage = data_.DiscordMessage(swapContent, "https://etherscan.io/tx/" + JSON.transacHash, coins, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), swapID)
                        discordMessages.append(swapMessage)
                
                if transfertContent:
                    transfertID = config["TRANSFERT_ID"]
                    if transfertID != "":
                        transfertMessage = data_.DiscordMessage(transfertContent, "https://etherscan.io/tx/" + JSON.transacHash, coins, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), transfertID)
                        discordMessages.append(transfertMessage)

                if discordMessages != []:
                    return discordMessages

                if swapEmbed == [] and transfertEmbed == []:
                    print("Error")
                    return "Error"
        else:
            return "Error"