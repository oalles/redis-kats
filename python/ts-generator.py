# RedisEdge initialization script - RG scripts loader
import argparse
from urllib.parse import urlparse

from kats.consts import TimeSeriesData
from kats.utils.simulator import Simulator
from redistimeseries.client import Client

key = 'tsdata'

def generate_data() -> TimeSeriesData:
    # TODO: Externalize var
    # Run Kats simulator
    sim = Simulator(n=365, start='2021-01-01', freq='D')
    tsd = sim.trend_shift_sim(intercept=1500, noise=300, seasonal_period=30, seasonal_magnitude=0.003,
                              cp_arr=[60, 120, 240], trend_arr=[10, -50, 80, -30])
    # Manually add outliers
    tsd_df = tsd.to_dataframe()
    tsd_df.loc[tsd_df.time == '2021-01-03', 'value'] *= 4
    tsd_df.loc[tsd_df.time == '2021-06-06', 'value'] *= 6
    tsd_df.loc[tsd_df.time == '2021-12-18', 'value'] *= 5
    return TimeSeriesData(tsd_df)


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Redis URL', type=str, default='redis://localhost:6379')
    args = parser.parse_args()

    # Set up Redis connection
    url = urlparse(args.url)

    rts = Client(host=url.hostname, port=url.port)
    if not rts.redis.ping():
        raise Exception('Redis unavailable')

    # Remove current timeseries data
    rts.redis.delete(key)

    # Run Kats simulator
    tsd = generate_data()

    for index, row in tsd.to_dataframe().iterrows():
        rts.add(key, round(row['time'].timestamp() * 1000), row['value'])
        # TS.ADD - timestamp-(integer) UNIX sample timestamp in milliseconds or * to set the timestamp based on the server's clock.

    print('TotalSamples: ', rts.info(key).total_samples)
