from abc import ABC
from dataclasses import dataclass
import PyWinDDE
from config import  QUOTE_SOURCE
from utils import *
from module_callback import printer

@dataclass
class OptionData:
    data: dict
    
    def update_data(self, raw_data:str):
        raw_data = raw_data.split(';')
        for column, value in zip(NEED_DATA, raw_data):
            self.data[column] = value
        


class DDEQuoter:
    def __init__(self):
        self.router = PyWinDDE.DDEClient(QUOTE_SOURCE, "Quote")
        
    def connect(self, ticker: str, callback_func):
        return self.router.advise(item= ticker, callback = callback_func)



###  parser for parsing OptionData
class Executor:
    def __init__(self, parser) -> None:
        self.option_config = get_option_info()
        self.quoter = DDEQuoter()
        self._init_recorder()
        self.parser = parser
    
    def callback(self, value, item):
        ticker =  item.split('-')[0]
        self.option_record[ticker].update_data(value)
        print(ticker, self.option_record[ticker].data)
        
    
    def _init_recorder(self):
        self.option_record = {}
        for each_option in self.option_config:
            self.option_record[each_option] = OptionData({})
    
    def _execute(self):
        for each_option in self.option_config:
            xq_ticker = gen_ticker_format(each_option, NEED_DATA)
            self.quoter.connect(xq_ticker, self.callback)
    
    def execute(self):
        self._execute()
        PyWinDDE.WinMSGLoop()
        
        
    
    
        
        
            
    
    
    
    
    

    


    
        