 import time
import settings
import json
from email.mime import base
from web3.middleware import local_filter_middleware
from db import MySQLDB
from pair import UniswapPair
import time
# from multiprocessing import Process, Manager
import multiprocessing
from multiprocessing import Process, Manager, Pool
from web3 import Web3
import pandas as pd


start = time.time()
# web3 = Web3(Web3.WebsocketProvider("ws://127.0.0.1:8546",websocket_timeout=360, websocket_kwargs={"max_size": 650000000}))

web3 = Web3(Web3.IPCProvider())

_db = MySQLDB()
contractuni = UniswapPair(address=settings.UNI_ROUTER, abi=settings.get_v2()).contract()
contractsushi=UniswapPair(address=settings.SUSHI_ROUTER, abi=settings.get_v2()).contract()
contractuniv3=UniswapPair(address=settings.CONTRACT_ADD, abi=settings.get_v3()).contract()

def updateReservesForUni_v2(pairaddr):
    
    reserve_data_v2=[]

    for i in range (len(pairaddr)):
        try:
            
            pairaddr_v2=pairaddr.iloc[i,0]
            pairaddr_v2=web3.toChecksumAddress(pairaddr_v2)
            
            pairaddr_v2_contract = web3.eth.contract(address=pairaddr_v2,abi=settings.get_token_abi())
            reserves = pairaddr_v2_contract.functions.getReserves().call()
            
            reserve0 = reserves[0]
            reserve1 = reserves[1]
            reserve_data_v2.append((reserve0,reserve1,pairaddr_v2))
    
        
        
        except Exception as e:
            # print(e)
            continue
    
    # return reserve_data_v2
    reserve_data_v2
    # _db.updateReserves_in_db_uni(reserve_data_v2)
    _db.insertReserves_in_db_uni(reserve_data_v2)
    _db.updateReserves_from_temp_univ2()
    _db.truncate_temp_univ2()

def updateReservesForSushi(pairaddr):
    reserve_data_v2=[]

    for i in range (len(pairaddr)):
        try:
            pairaddr_v2=pairaddr.iloc[i,0]
            pairaddr_v2=web3.toChecksumAddress(pairaddr_v2)
    
            pairaddr_v2_contract = web3.eth.contract(address=pairaddr_v2,abi=settings.get_token_abi())
            reserves = pairaddr_v2_contract.functions.getReserves().call()
    
            reserve0 = reserves[0]
            reserve1 = reserves[1]
            reserve_data_v2.append((reserve0,reserve1,pairaddr_v2))
    
        
        
        except Exception as e:
               # print(e)
            continue
    
    # return reserve_data_v2
    # _db.updateReserves_in_db_sushi(reserve_data_v2)
    _db.insertReserves_in_db_sushi(reserve_data_v2)
    _db.updateReserves_from_temp_sushi()
    _db.truncate_temp_sushi()   

def updateReservesForUni_v3(data_df):
    
    addresses=[]


    pairAddress_v3_df = data_df["pairAddress_v3"]
    token0Address_v3_df = data_df["token0Address_v3"]
    token1Address_v3_df = data_df["token1Address_v3"]
    fee_df = data_df["fee_v3"]
    token0_dec_df = data_df["token0Dec_v3"]
    token1_dec_df = data_df["token1Dec_v3"]

    for i in range(len(data_df)):

        try:

            address = web3.toChecksumAddress(pairAddress_v3_df.iloc[i])
           
            token0Address =web3.toChecksumAddress(token0Address_v3_df.iloc[i])
            token1Address =web3.toChecksumAddress(token1Address_v3_df.iloc[i])
            fee = fee_df.iloc[i]

            token0_symbol = web3.eth.contract(address=token0Address, abi=settings.get_token_abi())
            token1_symbol = web3.eth.contract(address=token1Address, abi=settings.get_token_abi())

            reserveA = token0_symbol.functions.balanceOf(address).call()
            reserveB = token1_symbol.functions.balanceOf(address).call()
            # token0_dec=token0_dec_df.iloc[i]
            # token1_dec=token1_dec_df.iloc[i]
            # token0reserve = reserveA/10**token0_dec
            # token1reserve = reserveB/10**token1_dec
            # amountsout = contractuniv3.functions.getamountout(w3.toChecksumAddress(pairs.iloc[i]["token0Address"]),w3.toChecksumAddress(pairs.iloc[i]["token1Address"]),int(pairs.iloc[i]["fee"]),10**token0,0).call()
            # price=amountsout/(10**token1)
            # amountsout = contractuniv3.functions.getamountout(w3.toChecksumAddress(pairs.iloc[i]["token1Address"]),w3.toChecksumAddress(pairs.iloc[i]["token0Address"]),int(pairs.iloc[i]["fee"]),10**token1,0).call()
            # priceinverse=amountsout/(10**token0)
            addresses.append((reserveA,reserveB,address,fee))
        except Exception as e:
            # print(e)
            continue

    # _db.updateReserves_in_db_univ3(addresses) 
    _db.insertReserves_in_db_v3(addresses)
    _db.updateReserves_from_temp_v3()
    _db.truncate_temp_v3()


if __name__=="__main__":
    start_time = time.time()
    data = _db.fetch_master_table()
    pairAddress_v2 = data["pairAddress_v2"]    
    df_pairAddress_v2 = pd.DataFrame(pairAddress_v2)
    df_pairAddress_v2 = df_pairAddress_v2.drop_duplicates()
    # df_pairAddress_v2 = [df_pairAddress_v2]

    pairAddress_sushi = data["pairAddress_sushi"]
    df_pairAddress_sushi = pd.DataFrame(pairAddress_sushi)
    df_pairAddress_sushi = df_pairAddress_sushi.drop_duplicates()
    # df_pairAddress_sushi = [df_pairAddress_sushi]


    # pairdetails_v3 = data[""]
    df_pairdetails_v3 = data
    df_pairdetails_v3 = df_pairdetails_v3.drop_duplicates()
    # df_pairdetails_v3 = [df_pairdetails_v3]


    with Pool() as p:
        reserves = p.map(updateReservesForUni_v2, [df_pairAddress_v2])
        reserves = p.map(updateReservesForSushi, [df_pairAddress_sushi])
        reserves = p.map(updateReservesForUni_v3, [df_pairdetails_v3])
    print("--- %s seconds ---" % (time.time() - start_time))
    
