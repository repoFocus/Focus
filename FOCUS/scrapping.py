import data
from decimal import Decimal

def run(jsonResponse, index):
    if jsonResponse["message"] == "OK":
        try:
            blockNumber = jsonResponse["result"][index]["blockNumber"]
            timeStamp = jsonResponse["result"][index]["timeStamp"]
            transacHash = jsonResponse["result"][index]["hash"]
            nonce = jsonResponse["result"][index]["nonce"]
            blockHash = jsonResponse["result"][index]["blockHash"]
            transacIndex = jsonResponse["result"][index]["transactionIndex"]
            transacFrom = jsonResponse["result"][index]["from"]
            transacTo = jsonResponse["result"][index]["to"]
            value = jsonResponse["result"][index]["value"]
            gas = jsonResponse["result"][index]["gas"]
            gasPrice = jsonResponse["result"][index]["gasPrice"]
            isError = jsonResponse["result"][index]["isError"]
            txreceipt_status = jsonResponse["result"][index]["txreceipt_status"]
            transacInput = jsonResponse["result"][index]["input"]
            contractAddress = jsonResponse["result"][index]["contractAddress"]
            cumulativeGasUsed = jsonResponse["result"][index]["cumulativeGasUsed"]
            gasUsed = jsonResponse["result"][index]["gasUsed"]
            confirmations = jsonResponse["result"][index]["confirmations"]
            methodId = jsonResponse["result"][index]["methodId"]
            functionName = jsonResponse["result"][index]["functionName"]

            


            i = 0
            value = Decimal(value) / Decimal(10**18)
            value = str(value)
            defValue = None    
            for letter in value:
                if letter == ".":
                    defValue = value[:i+3]
                else:
                    i = i +1
        
        
            JSON = data.JSONinfo(blockNumber, timeStamp, transacHash, nonce, blockHash, transacIndex, transacFrom, transacTo, defValue, gas, gasPrice, isError, txreceipt_status, transacInput, contractAddress, cumulativeGasUsed, gasUsed, confirmations, methodId, functionName)
            return JSON
        except:
            return "Error"
    else:
        pass