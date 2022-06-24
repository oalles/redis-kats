import pandas as pd
from kats.models.prophet import ProphetModel, ProphetParams
from kats.consts import TimeSeriesData

KEY = 'tsdata'
PARAMS = ProphetParams(seasonality_mode='multiplicative')
DAYS_PREDICTED = 10

def predict(x):

    k = x['key']
    print(k)

    assert KEY == k

    r = execute('TS.RANGE',  KEY, '-', '+')
    tsd_df = pd.DataFrame.from_records(r,columns=['time','value'])
    tsd_df['value'] = tsd_df['value'].astype(float)
    log(f"PreTime: '{tsd_df['time'][0]}'", level='warning')
    tsd_df['time'] = pd.to_datetime(tsd_df['time']*1000000, origin='unix', format='%Y-%m-%d').dt.date
    log(f"PostTime: '{tsd_df['time'][0]}'", level='warning')

    tsd = TimeSeriesData(tsd_df)
    m = ProphetModel(tsd, PARAMS)
    m.fit()

    # # make prediction for next 10 days
    fcst = m.predict(steps=DAYS_PREDICTED, freq="D")
    log(f"Pred Length: '{len(fcst)}'", level='warning')

    # for index, row in fcst[len(tsd_df):].iterrows():
    for index, row in fcst.iterrows():
        millisec = round(row['time'].timestamp()*1000)
        execute('TS.ADD', 'newk', millisec, row['fcst'])

gb = GearsBuilder()
gb.foreach(predict)
gb.run(KEY)
