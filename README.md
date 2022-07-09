# Description
Implementing some TimeSeries Analysis using [Redis TimeSeries](https://redis.io/docs/stack/timeseries/), [RedisGears](https://redisgears.io/) with CommandReader type, 
Facebook [Kats](https://github.com/facebookresearch/Kats) toolkit to analyze time series data.

`WIP`

## Preparing the environment

:persevere: Struggling a lot trying to install KATS to be run in RedisGears **venv**. 

#### Build image
```bash
docker-compose up # --build # First Time
docker ps # Get id
```

#### Manually install dependencies
```bash
$ docker exec -ti <id> /bin/bash
# activate rg venv
$ source /var/opt/redislabs/modules/rg/.venv-/bin/activate
$ ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6
$ pip3 install --upgrade pip
$ pip3 install --no-cache-dir setuptools
$ pip3 install numpy pandas convertdate Cython~=0.22 pystan~=2.18
$ pip3 install fbprophet==0.7.1 kats
$ pip3 install kats
```

#### Load Mocked Data
Run [Simulator](python/ts-generator.py) for generating synthetic time series data.

#### Load Redis Gears functions
Run the [python client](python/loader-rgs.py) to load RG functions. 
See the server log while loading. 

RG functions: 

* [Forecaster](python/rg-forecasting.py):  Run the forecasting using the Prophet model. 10 predicted values under `predicted` key. 

Next steps: 

* Invoke prediction from a Java Process using [CommandReader](https://oss.redis.com/redisgears/readers.html#commandreader) reader in a RG function. 
