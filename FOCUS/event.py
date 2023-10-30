import data
import requests
import fileread
import scrapping as scrap
import main
import json
import time
import os
import concurrent.futures
from datetime import datetime


walletList = fileread.getWalletList()
config = fileread.getConfig()
keys = fileread.getAPIKeys()

def updateWalletList():
	global walletList
	newWalletList = fileread.getWalletList()
	for wallet in newWalletList:
		for oldWallet in walletList:
			if wallet.adr == oldWallet.adr and wallet.chain == oldWallet.chain:
				wallet.previousTA = oldWallet.previousTA
	
	walletList = newWalletList

def fetchWalletData(currentWallet, config, index):
    if currentWallet:
			
            url = 'https://api.etherscan.io/api?module=account&action=txlist&address={}&page=1&offset=50&sort=desc&apikey={}'.format(currentWallet.adr, keys[str(index)])
            
            resp = requests.get(url)
            currentWallet.resp = json.loads(resp.text)
            
            return currentWallet

def run(nombreClesAPI, walletListLen):
		with concurrent.futures.ThreadPoolExecutor(max_workers=nombreClesAPI) as executor:
			print("Scanning...\t", datetime.now())
			for walletIndex in range(0, len(walletList), nombreClesAPI):
				current_group = walletList[walletIndex:walletIndex+nombreClesAPI]
				index = 1
				for wallet in current_group:
					executor.submit(fetchWalletData, wallet, config, index)
					if index < nombreClesAPI:
						index = index + 1
					elif index == nombreClesAPI:
						index = 1
					if walletListLen > nombreClesAPI:	
						time.sleep(1/nombreClesAPI)
					else:
						time.sleep(1/walletListLen)
			print("Fully scanned !\t", datetime.now())
                        
while True:
	if config["SETUPED"] == "True":
		config = fileread.getConfig()
		updateWalletList()
		if walletList == []:
				os.system("cls")
				time.sleep(10)
		else:
		
			i = 0
			run(len(keys), len(walletList))
			for wallet in walletList:
				config = fileread.getConfig()
				if config["SETUPED"] == "True":
					transacBT = []
					if wallet.previousTA:
						if wallet.resp:
							if wallet.resp["message"] == "OK":

								if str(wallet.resp["result"][0]["hash"]) == wallet.previousTA:
									print(wallet.chain, "| No new transaction for", wallet.name, "\n")
									
								else:
									index = 0
									
									while True:
										if index != 50:
											oldTA = scrap.run(wallet.resp, index)
											if oldTA != "Error":
												old = data.Transaction(wallet, oldTA)

												if str(wallet.resp["result"][index]["hash"]) != wallet.previousTA:
													transacBT.append(old)
													index = index + 1

												else:
													
													if transacBT != []:
														print(wallet.chain, "| New transaction for", wallet.name, "\n")
														transacBT.reverse()
														for transac in transacBT:
															main.run(transac)
													else:
														main.run(old)
													wallet.previousTA = wallet.resp["result"][0]["hash"]
													break
											else:
												
												break
												
										else:
											
											break
							else:
								print("doomed", wallet.name)
						else:
							print("doomed 2", wallet.name)			

					else:
							try:
								os.system("cls")
								print("Setuped {}/{} wallet".format(walletList.index(wallet)+1, len(walletList)))
								wallet.previousTA = wallet.resp["result"][0]["hash"]
							except:
								print("No transaction for", wallet.name)
				else:
					break
	else:
			os.system("cls")
			config = fileread.getConfig()
			print("Server not setuped Yet")
			time.sleep(10)