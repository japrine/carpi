import requests
import json
import sched
import time
import os               # for sensors


with open('config.json', 'r') as f:
    config = json.load(f)

URL_PATH = 'http://127.0.0.1:5000/car/{}'.format(config['car'])
HEADERS = {'Content-Type': 'application/json'}

s = sched.scheduler(time.time, time.sleep)

DATA = {
    "status": False,
    "int_temp": 0.0,
    "ext_temp": 0.0,
    "cool_temp": 0.0,
    "voltage": 0.0
}


def get_temp_sensors():
    ds18b20 = []
    try:
        for i in os.listdir('/sys/bus/w1/devices'):
            if i != 'w1_bus_master1':
                ds18b20.append(i)
    except FileNotFoundError:
        print('No Temp Sensors')
    return ds18b20


def check_sensor(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    with open(location) as f:
        text = f.read()
    second = text.split("\n")[1]
    temp_data = second.split(" ")[9]
    temperature = float(temp_data[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return farenheit


def update_status(sc):
    s.enter(60, 1, update_status, (sc,))                                            # Run every 60sec
    for idx, sensor in enumerate(sensor_list):
        value = check_sensor(sensor)
        if config['int_temp'] == idx:
            DATA['int_temp'] = value
        elif config['ext_temp'] == idx:
            DATA['ext_temp'] = value
        elif config['cool_temp'] == idx:
            DATA['cool_temp'] = value

    try:
        r = requests.post(URL_PATH, json=DATA, headers=HEADERS)
    except requests.exceptions.ConnectionError:
        r = None
        print('Cannot connect')
    # except Exception as e: print(e)
    if r:
        if r.ok:
            print("JSON: ", r.json())
        else:
            r.raise_for_status()


if __name__ == '__main__':
    sensor_list = get_temp_sensors()
    s.enter(60, 1, update_status, (s,))
    s.run()
