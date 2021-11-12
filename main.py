import logging
import backtester
import datetime
from utils import TF_EQUIV
from collector import collect_all
from exchange.binance import BinanceClient
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s,%(levelname)s,%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("info.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    action = input("Choose the mode you want (backtest/optimize/data): ").lower()
    client = BinanceClient()
    while True:
        symb = input("enter the ticker whose data you want")
        if symb in client.get_symbol():
            break

    if action == "data":
        collect_all(client,symb)
    elif action == "backtest":
        available_strategies = ["obv"]

        while True:
            strategy = input(f"choose a strategy: ({', '.join(available_strategies)})").lower()
            if strategy in available_strategies:
                break


        while True:
            tf = input(f"choose a timeframe: ({', '.join(TF_EQUIV.keys())})").lower()
            if tf in TF_EQUIV.keys():
                break



        while True:
            from_time = input(f"Backtest from (yyyy-mm-dd) or press enter").lower()
            if from_time == "":
                from_time=0
                break
            try:
                from_time = int(datetime.datetime.strptime(from_time, "%Y-%m-%d").timestamp()*1000)
                break
            except ValueError:
                continue

        while True:
            to_time = input(f"Backtest to (yyyy-mm-dd) or press enter").lower()
            if to_time == "":
                to_time = int(datetime.datetime.now().timestamp()*1000)
                break
            try:
                to_time = int(datetime.datetime.strptime(from_time, "%Y-%m-%d").timestamp() * 1000)
                break
            except ValueError:
                continue
        backtester.run(symb,strategy,tf,from_time, to_time)


