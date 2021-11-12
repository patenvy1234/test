import time
import numpy as np
import pandas as pd

from database import HDF5client
from utils import *

pd.set_option('display.max_columns',None)
pd.set_option('display.width',1000)

h5_db = HDF5client()
data = h5_db.get_data("BNBBTC",from_time=0,to_time=int(time.time()*1000))
data = resample_timeframe(data,"1h")

data["high_low_avg"] = (data["high"]+data["low"])/2
data['signal'] = np.where(data['close'] > data['high_low_avg'],1,-1)
print(data)