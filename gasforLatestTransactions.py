from web3 import Web3
import asyncio
from asyncio import run_coroutine_threadsafe
import numpy as np
import json
import json.decoder
from db import MySQLDB
import pandas as pd
from statistics import mean, median
import time

_db = MySQLDB()

# web3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8546",websocket_timeout=360, websocket_kwargs={"max_size": 650000000}))


# alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/6AAf8nSk2xYkiBZ7YHT3_FmeAaOWO_NS"
# alchemy_url = "https://mainnet.infura.io/v3/fa92b0b9e654467bacbba6197882ce7a"
alchemy_url = "wss://mainnet.infura.io/ws/v3/fa92b0b9e654467bacbba6197882ce7a"
# web3 = Web3(Web3.HTTPProvider(alchemy_url))
web3 = Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/fa92b0b9e654467bacbba6197882ce7a",websocket_timeout=360, websocket_kwargs={"max_size": 650000000}))

# loop = asyncio.get_event_loop()
latest_block=0
while True:
# while web3.eth.get_block_number()> latest_block:
    if web3.eth.get_block_number()> latest_block:
        latest_block = web3.eth.get_block_number()
        print(str(latest_block) +' Block Number')

    # print(latest_block)
        transactions = web3.eth.get_block("latest")
        gasUsed = dict(transactions)['gasUsed']
        baseFeePerGas = dict(transactions)['baseFeePerGas']
    # HexBytes = dict(transactions)['HexBytes']
    # print(HexBytes)
    # print(transactions)
        trx = dict(transactions)['transactions']
        maxPriorityFeePerGas = []
        for i in trx:
            trxdetail = web3.eth.getTransaction(i.hex())
        # print(trxdetail)
            try:
                maxPriorityFeePerGas.append(dict(trxdetail)['maxPriorityFeePerGas'])
            except:
                continue    
    # print(maxPriorityFeePerGas)
        # maxPriorityFeePerGas = max(maxPriorityFeePerGas)
        # minpriorityfee = min(maxPriorityFeePerGas)
        meanpriorityfee = int(mean(maxPriorityFeePerGas))
        # maxPriorityFeePerGas = int(dict(d)['maxPriorityFeePerGas'])
        # print(maxPriorityFeePerGas)
        

# for i in trx:
#     print(dict(transactions)['transactions'])
# print(web3.eth.getTransaction('0xad453536ae19b79bf06a6751f7bfa11f0ca2edd63a10b03b9b9ea46184362c2a'))
        print(gasUsed)
        print(baseFeePerGas)
        if gasUsed>15000000:
            newbaseFeePerGas = baseFeePerGas*0.125 + baseFeePerGas
        elif gasUsed<15000000:
            newbaseFeePerGas = baseFeePerGas
        print(newbaseFeePerGas)
        d = [(latest_block,gasUsed,baseFeePerGas,newbaseFeePerGas,meanpriorityfee)]
        print(d)
        _db.updatePrice_in_db_ethgas(d)
        time.sleep(1)



    # loop.run_forever()

    


# txrec= web3.eth.getTransaction('0x303c14157aae7c57dbed1be5ca72c6a94e1408f02657298f20832ea01c944565')
# gas = int(dict(txrec)['gasPrice'])
# print(gas)
