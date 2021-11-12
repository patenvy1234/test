import time
from utils import *
from database import HDF5client
from typing import *
from exchange.binance import BinanceClient
import logging
logger = logging.getLogger()
def collect_all(client ,symbol):
    hd_f5 = HDF5client()
    hd_f5.create_table(symbol)
    # data = hd_f5.get_data(symbol,from_time=0,to_time=int(time.time()*1000))
    # data = resample_timeframe(data, "4h")
    # print(data)
    # return
    oldest_ts,most_recent_ts=hd_f5.get_first_last_timestamp(symbol)
    # print(oldest_ts,most_recent_ts)

    if oldest_ts is None:
        data = client.get_historical_data(symbol, end_time=int(time.time()*1000-60000))
        if len(data) == 0:
            logger.warning("binance %s: no initial data found", symbol)
        else:
            logger.info("binance %s : collected %s initial data from %s to %s",symbol,len(data),ms_to_date(data[0][0]),ms_to_date(data[-1][0]))

        oldest_ts = data[0][0]
        most_recent_ts = data[-1][0]

        hd_f5.write_data(symbol,data)
    # most recent data


    while True:
        data = client.get_historical_data(symbol, start_time=int(most_recent_ts+60000))

        if data is None:
            time.sleep(4)
            continue
        if len(data) < 2:
            break
        data = data[:-1]
        if data[-1][0] > most_recent_ts:
            most_recent_ts = data[-1][0]
        logger.info("binance %s : collected %s most_recent data from %s to %s", symbol, len(data),
                        ms_to_date(data[0][0]), ms_to_date(data[-1][0]))

        hd_f5.write_data(symbol, data)
        time.sleep(1.1)

    # oldest data

    while True:
        data = client.get_historical_data(symbol, end_time=int(oldest_ts - 60000))

        if data is None:
            time.sleep(4)
            continue
        if len(data) == 0:
            logger.info("binance %s : stopped older data collection because no data found:" , symbol)
            break

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]
        logger.info("binance %s : collected %s old data from %s to %s", symbol, len(data),
                        ms_to_date(data[0][0]), ms_to_date(data[-1][0]))

        hd_f5.write_data(symbol, data)
        time.sleep(1.1)
