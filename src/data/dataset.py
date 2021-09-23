"""Module used to build the dataset"""

import csv
import client
import json
import numpy as np
from math import floor
import matplotlib.pyplot as plt
import pandas as pd
#import torch
#from torch.utils.data import Dataset, DataLoader
#from torchvision import transforms, utils

import warnings
warnings.filterwarnings("ignore")

crypto_pairs = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'AVAXUSDT', 'XRPUSDT', 'ADAUSDT', 'DOTUSDT', 'ATOMUSDT', 'BNBUSDT', 'LUNAUSDT', 'FTMUSDT', 'DOGEUSDT', 'FILUSDT', 'AXSUSDT', 'GALAUSDT', 'OMGUSDT', 'FTTUSDT', 'SLPUSDT', 'ALGOUSDT', 'LINKUSDT', 'MATICUSDT', 'CELRUSDT', 'EGLDUSDT', 'DYDXUSDT', 'CELOUSDT', 'COTIUSDT', 'LTCUSDT', 'NEARUSDT', 'TRXUSDT', 'VETUSDT', 'HBARUSDT', 'MLNUSDT', 'THETAUSDT', 'EOSUSDT', 'XTZUSDT', 'KAVAUSDT', 'ICPUSDT', 'ILVUSDT', 'ONEUSDT', 'IOSTUSDT', 'SRMUSDT', 'PONDUSDT', 'ALICEUSDT', 'SUSHIUSDT', 'CAKEUSDT', 'ETCUSDT', 'SHIBUSDT', 'CHZUSDT', 'BCHUSDT', 'MINAUSDT', 'PERPUSDT', 'UNIUSDT', 'IOTAUSDT', 'RUNEUSDT', 'C98USDT', 'TLMUSDT', 'RENUSDT', 'KSMUSDT', 'XECUSDT', 'AAVEUSDT', 'ARUSDT', 'CRVUSDT', 'SXPUSDT', 'AUDIOUSDT', 'XLMUSDT', 'CFXUSDT', 'FLOWUSDT', 'TWTUSDT', 'SANDUSDT', 'FETUSDT', 'HOTUSDT', 'GRTUSDT', 'XMRUSDT', 'CHRUSDT', 'NEOUSDT', 'MBOXUSDT', 'BTTUSDT', 'QNTUSDT', '1INCHUSDT', 'DENTUSDT', 'FORUSDT', 'TROYUSDT', 'ONTUSDT', 'ATAUSDT', 'ROSEUSDT', 'WAVESUSDT', 'RAYUSDT', 'EPSUSDT', 'KMDUSDT', 'TVKUSDT', 'IDEXUSDT', 'ZECUSDT', 'DASHUSDT', 'SNXUSDT', 'QTUMUSDT', 'LPTUSDT', 'FUNUSDT', 'BAKEUSDT', 'TKOUSDT', 'CTSIUSDT', 'COMPUSDT', 'ZENUSDT', 'OGNUSDT', 'BLZUSDT', 'ZILUSDT', 'REEFUSDT', 'ICXUSDT', 'DATAUSDT', 'MASKUSDT', 'VTHOUSDT', 'RSRUSDT', 'HARDUSDT', 'ENJUSDT', 'ARPAUSDT', 'NANOUSDT', 'RVNUSDT', 'MTLUSDT', 'XVSUSDT', 'DODOUSDT', 'WINUSDT', 'YFIUSDT', 'NMRUSDT', 'ALPHAUSDT', 'UNFIUSDT', 'CVCUSDT', 'MANAUSDT', 'VIDTUSDT', 'SUPERUSDT', 'WINGUSDT', 'SUNUSDT', 'DIAUSDT', 'IOTXUSDT', 'KEYUSDT', 'TOMOUSDT', 'TFUELUSDT', 'ANKRUSDT', 'HNTUSDT', 'LINAUSDT', 'TRUUSDT', 'SKLUSDT', 'ORNUSDT', 'COSUSDT', 'AVAUSDT', 'ELFUSDT', 'DEGOUSDT', 'LRCUSDT', 'INJUSDT', 'SCUSDT', 'YFIIUSDT', 'DNTUSDT', 'FLMUSDT', 'SFPUSDT', 'OCEANUSDT', 'CKBUSDT', 'CTXCUSDT', 'CLVUSDT', 'FISUSDT', 'SMTXUSDT', 'KEEPUSDT', 'ACMUSDT', 'PAXGUSDT', 'BANDUSDT', 'XEMUSDT', 'LTOUSDT', 'TRIBEUSDT', 'OMUSDT', 'FORTHUSDT', 'STXUSDT', 'TRBUSDT', 'LITUSDT', 'MIRUSDT', 'PNTUSDT', 'BZRXUSDT', 'AKROUSDT', 'ALPACAUSDT', 'DGBUSDT', 'MITHUSDT', 'WAXPUSDT', 'OXTUSDT', 'XVGUSDT', 'PSGUSDT', 'AUTOUSDT', 'MKRUSDT', 'DOCKUSDT', 'WTCUSDT', 'UTKUSDT', 'UMAUSDT', 'TCTUSDT', 'CTKUSDT', 'NKNUSDT', 'KNCUSDT', 'JSTUSDT', 'ZRXUSDT', 'BALUSDT', 'FIOUSDT', 'MDTUSDT', 'BARUSDT', 'MDXUSDT', 'REQUSDT', 'RAMPUSDT', 'STRAXUSDT', 'IRISUSDT', 'PHAUSDT', 'BADGERUSDT', 'FARMUSDT', 'BURGERUSDT', 'ONGUSDT', 'NUUSDT', 'TORNUSDT', 'ERNUSDT', 'AIONUSDT', 'BONDUSDT', 'RLCUSDT', 'GTCUSDT', 'STORJUSDT', 'POLSUSDT', 'FIROUSDT', 'POLYUSDT', 'REPUSDT', 'PERLUSDT', 'BEAUMUSDT', 'OGUSDT', 'LSKUSDT', 'GXSUSDT', 'DEXEUSDT', 'ANTUSDT', 'BNTUSDT', 'BTSUSDT', 'JUVUSDT', 'ASRUSDT', 'BTGUSDT', 'PUNDIXUSDT', 'KLAYUSDT', 'DCRUSDT', 'MFTUSDT', 'DUSKUSDT', 'MBLUSDT', 'GTOUSDT', 'DREPUSDT', 'WANUSDT', 'NBSUSDT', 'COCOSUSDT', 'ARDRUSDT', 'VITEUSDT', 'QUICKUSDT', 'HIVEUSDT', 'ATMUSDT', 'WNXMUSDT', 'NULSUSDT', 'STPTUSDT', 'GNOUSDT', 'RIFUSDT',]

def build_dataset():
    """Build dataset by downloading from Binance API"""

    # Get the current server time
    server_time = client.CLIENT.get_server_time()["serverTime"]
    for cp in crypto_pairs:
        print(cp)
        filename = 'src/data/csv' + cp + '.csv'

        tmp = []

        # Get the first ever kline time
        first_kline = client.CLIENT.get_klines(symbol=cp, interval=client.CLIENT.KLINE_INTERVAL_1MINUTE, startTime=0, limit=1)
        start_time = int(first_kline[0][0])
        act_time = start_time
        steps = 1000
        percentage=0
        total_steps = server_time - start_time
        while act_time < server_time:
            current_steps = act_time - start_time + 1
            if (act_time + steps > server_time):
                steps = server_time - act_time - 1
            if (percentage < floor((current_steps / total_steps) * 100)):
                percentage = floor((current_steps / total_steps) * 100)
                print(percentage, '% ', flush=True)
            klines = client.CLIENT.get_klines(symbol=cp, interval=client.CLIENT.KLINE_INTERVAL_1MINUTE, startTime=act_time, limit=steps)  
            for k in klines:
                tmp.append([k[0], k[1], k[2], k[3], k[4], k[6]])
            act_time += steps * 60000
        with open(filename, 'w+', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerows(tmp)
        
        print(cp, ' done')
