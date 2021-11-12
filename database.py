import h5py
import logging
import numpy as np
import pandas as pd
import time
logger = logging.getLogger()
class HDF5client:
    def __init__(self):
        self.hf = h5py.File(f"data/binance.h5",'a')
        self.hf.flush()

    def create_table(self,symbol):
        if symbol not in self.hf.keys():
            self.hf.create_dataset(symbol,(0,6),maxshape=(None,6),dtype="float64")
            self.hf.flush()
    def write_data(self,symbol,data):
        min_ts,max_ts = self.get_first_last_timestamp(symbol)
        if min_ts is None:
            min_ts = float("inf")
            max_ts = 0
        filtered_data=[]

        for d in data:
            if d[0]<min_ts:
                filtered_data.append(d)
            elif d[0]>max_ts:
                filtered_data.append(d)

        if len(filtered_data) == 0:
            logger.warning("%s No data to inserr",symbol)


        data_array = np.array(data)

        self.hf[symbol].resize(self.hf[symbol].shape[0]+data_array.shape[0],axis=0)
        self.hf[symbol][-data_array.shape[0]:] = data_array
        self.hf.flush()

    def get_data(self,symbol,from_time,to_time):
        start_query = time.time()
        existing_data = self.hf[symbol][:]
        if len(existing_data) == 0:
            return None
        data = sorted(existing_data,key=lambda x : x[0])
        data = np.array(data)
        df = pd.DataFrame(data,columns= ["timestamp","open","high","low","close","volume"])
        df = df[(df["timestamp"] >= from_time) & (df["timestamp"] <= to_time)]
        df["timestamp"] = pd.to_datetime(df["timestamp"].values.astype(np.int64),unit = 'ms')
        df.set_index("timestamp",drop=True,inplace=True)
        query_time = round(time.time()-start_query,2)
        logger.info("Retrieved data %s %s from database in %s seconds",len(df.index),symbol,query_time)
        return df

    def get_first_last_timestamp(self,symbol):
        existing_data = self.hf[symbol][:]
        if len(existing_data) == 0:
            return None,None
        first_ts = min(existing_data,key = lambda x: x[0])[0]
        last_ts = max(existing_data, key=lambda x: x[0])[0]

        return first_ts,last_ts