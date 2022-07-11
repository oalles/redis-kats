import pandas as pd
from kats.models.prophet import ProphetModel, ProphetParams
from kats.consts import TimeSeriesData

KEY = 'valuesPerDay'

PARAMS = ProphetParams(seasonality_mode='multiplicative')

def predict(daysCount):

    r = execute('TS.RANGE',  KEY, '-', '+')
    tsd_df = pd.DataFrame.from_records(r,columns=['time','value'])
    tsd_df['value'] = tsd_df['value'].astype(float)
    # log(f"PreTime: '{tsd_df['time'][0]}'", level='warning')
    tsd_df['time'] = pd.to_datetime(tsd_df['time']*1000000, origin='unix', format='%Y-%m-%d').dt.date
    # log(f"PostTime: '{tsd_df['time'][0]}'", level='warning')

    tsd = TimeSeriesData(tsd_df)
    m = ProphetModel(tsd, PARAMS)
    m.fit()

    # # make prediction for next 10 days
    fcst = m.predict(steps=int(daysCount), freq="D")
    # log(f"Pred Length: '{len(fcst)}'", level='warning')

    response = []
    for index, row in fcst.iterrows():
        millisec = round(row['time'].timestamp()*1000)
        response.append({'t': millisec, 'v': row['fcst']});

    return response

gb = GearsBuilder('CommandReader')
# x[1] predicted days count
gb.map(lambda x: predict(x[1]))
gb.register(trigger='GetValuesPerDayPredictions')
