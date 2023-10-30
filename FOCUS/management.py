import fileread
import json

config = fileread.getConfig()
emojis = fileread.getEmojis()

def isWalletListUnder500():

    walletList = fileread.getWalletList()
    if len(walletList) < 500:
        return True
    else:
        return False


def clearJSON():
    
    emojis["UNISWAP_EMOJI_ID"] = ""
    emojis["ETH_EMOJI_ID"] = ""
    emojis["ARB_EMOJI_ID"] = ""
    emojis["BNB_EMOJI_ID"] = ""

    config["GUILD_ID"] = ""
    config["SWAP_ID"] = ""
    config["TRANSFERT_ID"] = ""
    config["COMMAND_ID"] = ""
    config["CATEGORY_ID"] = ""
    config["SETUPED"] = "False"

    with open("config.json", "w") as json_data_file:
        json_data_file.write(json.dumps(config, indent=4))

    with open("emojis.json", "w") as json_data_file:
        json_data_file.write(json.dumps(emojis, indent=4))

def editJSONUrl(uniswapEmoji, ethEmoji, arbEmoji, bnbEmoji, swapCh, transfertCh, commandCh, category, guild):

    emojis["UNISWAP_EMOJI_ID"] = uniswapEmoji.id
    emojis["ETH_EMOJI_ID"] = ethEmoji.id
    emojis["ARB_EMOJI_ID"] = arbEmoji.id
    emojis["BNB_EMOJI_ID"] = bnbEmoji.id


    config["GUILD_ID"] = guild.id
    config["SWAP_ID"] = swapCh.id
    config["TRANSFERT_ID"] = transfertCh.id
    config["COMMAND_ID"] = commandCh.id
    config["CATEGORY_ID"] = category.id
    config["SETUPED"] = "True"

    with open("config.json", "w") as json_data_file:
        json_data_file.write(json.dumps(config, indent=4))

    with open("emojis.json", "w") as json_data_file:
        json_data_file.write(json.dumps(emojis, indent=4))
    
def addWallet(adr,name,chain):

    if isWalletListUnder500():
        currentAdr = str(adr)
        currentName = str(name)
        cleanedAdr = ""
        cleanedName = ""

        iNeedToAdd = True
        for letter in currentAdr:
            if letter != " " or letter != "," or letter != ">":
                cleanedAdr = cleanedAdr + letter
            
        for letter in currentName:
            if letter == ",":
                cleanedName = cleanedName + " "
            elif letter == ">":
                cleanedName = cleanedName + "-"
            else:
                cleanedName = cleanedName + letter

        if cleanedAdr.startswith("0x"):
            if chain == "ETH" or chain == "ARB":
                print("yo")
                if len(cleanedAdr[2:]) == 40:
                    print("yo")
                    
                    walletList = fileread.getWalletList()
            
                    for wallet in walletList:
                        if wallet.adr == cleanedAdr and wallet.chain == chain:
                            iNeedToAdd = False
                        
                    
                else:
                    return "Error"
        else:
            return "Error"


        if iNeedToAdd:
            with open("adr.txt", "w") as file:

                for wallet in walletList:
                    file.write(str(wallet.adr) + "," + str(wallet.name) + ">" + str(wallet.chain) + "\n")
                file.write(str(cleanedAdr) + "," + str(cleanedName) + ">" + str(chain) + "\n")
        else:
            return "Existing"
    else:
        return "Over500"

def removeWallet(adr):
    currentAdr = str(adr)
    cleanedAdr = ""

    iNeedToRemove = False

    for letter in currentAdr:
        if letter != " " or letter != "," or letter != ">":
            cleanedAdr = cleanedAdr + letter
    if cleanedAdr.startswith("0x"):


        if len(cleanedAdr[2:]) == 40:

            walletList = fileread.getWalletList()
            
            for wallet in walletList:
                if wallet.adr == cleanedAdr:
                    walletList.remove(wallet)
                    iNeedToRemove = True
                
        else:
            return "Error"
    else:
        return "Error"

    if iNeedToRemove:                
        with open("adr.txt", "w") as file:

            for wallet in walletList:
                file.write(str(wallet.adr) + "," + str(wallet.name) + ">" + str(wallet.chain) + "\n")
    else:
        return "Inexisting"