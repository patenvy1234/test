import datetime

import requests
from typing import *
import logging
logger = logging.getLogger()
class BinanceClient:
    def __init__(self,futures=False):

        self.futures = futures
        if self.futures:
            self._base_url = "https://fapi.binance.com"
        else:
            self._base_url = "https://api.binance.com"

        self.symbol = self.get_symbol()


    def make_request(self,endpoint,query_parameters):
        try:
            response = requests.get(self._base_url + endpoint,params=query_parameters)
        except Exception as e:
            logger.error("Connection while making request %s to %s",endpoint,e)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making request to %s : %s (status code = %s)",endpoint,response.json(),response.status_code)
            return None

    def get_symbol(self):
        params=dict()
        endpoint = "/api/v3/exchangeInfo"
        data = self.make_request(endpoint,params)
        symbol_list : list = [x["symbol"] for x in data["symbols"]]
        return symbol_list

    def get_historical_data(self,symbol: str,start_time = None,end_time = None ):
        endpoint = "/api/v3/klines"
        params = dict()
        params["symbol"] = symbol
        params["interval"] = "1m"
        params["limit"] = 1000
        if start_time is  not None:
            params["startTime"] = start_time
        if end_time is  not None:
            params["endTime"] = end_time

        all_candles = self.make_request(endpoint,params)
        candle_data = []
        if all_candles is not None:
            for candles in all_candles:
                candle_data.append((float(candles[0]),float(candles[1]),float(candles[2]),float(candles[3]),float(candles[4]),float(candles[5])))
            return candle_data



