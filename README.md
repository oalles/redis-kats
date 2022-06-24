## Preparing the environment

:persevere: Struggled a lot trying to install KATS to be run in RedisGears **venv**. 

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

#### Load RG functions
Run the [python client](python/loader-rgs.py) to load RG functions. 

RG functions. 

* [Forecaster](python/rg-forecasting.py): 
