import pandas as pd 
import os 
import re
from libs import PyWinDDE
# connect DDE 
XQ_Option_DDE = PyWinDDE.DDEClient("XQLITE", "Quote")

data = {}

data['vol'] = 0
data['inout'] = 0

def cal_vol_rate() :
    print(data['inout'],data['vol'],round((data['inout'] -50)/50*data['vol'] ))


def inout_callback(value,item) :
    value = re.findall(r"[-+]?\d*\.\d+|\d+",str(value))[0]
    data['inout'] = float(value)
    cal_vol_rate()

def vol_callback(value,item) :
    value = str(value)
    data['vol'] = float(value)
    cal_vol_rate()
    
def printer(value, item):
    # print(value, item)
    print(value, type(value), item)

XQ_Option_DDE.advise(f"TXON05C20600.TF-InOutRatio,TotalVolume,Bid",callback = printer)
# XQ_Option_DDE.advise(f"TXON05C20600.TF-TotalVolume",callback = printer)


PyWinDDE.WinMSGLoop()

