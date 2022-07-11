# Description
Implement some TimeSeries Analysis using the serverless engine [RedisGears](https://redisgears.io/), [Redis TimeSeries](https://redis.io/docs/stack/timeseries/)  and 
Facebook [Kats](https://github.com/facebookresearch/Kats) as toolkit to analyze time series data. 

It shows how to: 
* build a custom Redis docker image with given modules
* generate timeseries mocked data using Kats from an external python process
* define a RedisGears function to perform timeseries forecasting using [Kats](https://github.com/facebookresearch/Kats)
* load RedisGears function from an external python process
* fetch the predictions from a (java) Spring Boot client invoking the RedisGears function

Jupiter notebook provided, containing the Kats logic used in the project: [here](ipynb/kats_101.ipynb). 

## Preparing the environment

### Run Redis 
#### Build docker image
```bash
docker-compose up # --build # First Time
```
#### Manually install dependencies in RedisGears venv
:persevere: Struggled a lot trying to install KATS to be run in RedisGears **venv**. 
The only way I was able to make it work was manually installing dependencies. `:(`

```bash
$ docker ps # Get process id
$ docker exec -ti <id> /bin/bash
# activate rg venv
$ source /var/opt/redislabs/modules/rg/.venv-/bin/activate
$ ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6
$ pip3 install --upgrade pip
$ pip3 install --no-cache-dir setuptools
$ pip3 install numpy pandas convertdate Cython~=0.22 pystan~=2.18
$ pip3 install fbprophet==0.7.1
$ pip3 install kats
```

### Load Mocked Data from external Python process
Kats needs to be installed on `python < 3.9`. Create 3.8 venv and install [requirements](python/requirements.txt).

Run [Simulator](python/ts-generator.py) for generating time series data.

### Load Redis Gears functions (Serverless Engine in Redis) 
Run the [python client](python/loader-rgs.py) to load RG functions. 

Watch redis server log while RG functions and dependencies installation are being loaded and requested. 

#### RedisGears functions

| Name                                    | Description                                                                                                                                                                         |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Forecaster](python/rg-forecasting.py)  | Contains the forecasting logic using the Prophet model. Trigger: `GetPredictions`. Input args: x[1] days to be predicted. CLI Execution: `RG.TRIGGER GetValuesPerDayPredictions 10` |

## Rest Endpoint: 

Spring Boot Process offers a Rest endpoint to retrieve the predicted values for the next days.

```bash
# Get Predicted values for next 3 days
curl http://localhost:8080/3
[{"t":1640995200000,"v":6068.410402495052},{"t":1641081600000,"v":5706.191453574134},{"t":1641168000000,"v":5617.7999465757375}]
```
