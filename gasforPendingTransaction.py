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

web3 = Web3(Web3.IPCProvider())
transactions = web3.eth.get_block("pending")
# print(transactions)

trx = dict(transactions)['transactions']
maxPriorityFeePerGas = []
for i in trx:
    try:
        trxdetail = web3.eth.getTransaction(i.hex())
        # print(trxdetail)
        maxPriorityFeePerGas.append(dict(trxdetail)['maxPriorityFeePerGas'])
    except:
            continue    
maxPriorityFeePerGas = max(maxPriorityFeePerGas)
print(maxPriorityFeePerGas)


