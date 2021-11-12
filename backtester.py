from database import HDF5client
from utils import resample_timeframe
import strategies.obv
def run(symbol,strategy,tf,from_time,to_time):
    if strategy == "obv":
        h5_db = HDF5client()
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data,tf)

        print(strategies.obv.backtest(data, 20))
