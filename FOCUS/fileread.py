import json
import data
import time

def getWalletList():
    walletList = []
    with open("adr.txt") as adr:
        lines = adr.readlines()

    name = ""
    adr = ""

    walletList = []

    for line in lines:
        j = 0
        i = 0
        for letter in line:
            if letter == ">":
                chain = line[i+1:]
            else:
                i = i + 1

        for letter in line: 
            if letter == ",":
                adr = line[:j]
                name = line[j+1:i-4]
            else:
                j = j + 1

        currentWallet = data.Wallet(name, adr, chain.rstrip("\n"), None, None)
        walletList.append(currentWallet)
    
    return walletList

def getConfig():
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)

    return config

def getEmojis():
    with open("emojis.json") as json_data_file:
        emojis = json.load(json_data_file)

    return emojis

def getAPIKeys():
    with open("keys.json") as json_data_file:
        keys = json.load(json_data_file)
    
    return keys