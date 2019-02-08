import requests
import json
import sched
import time


with open('config.json', 'r') as f:
    config = json.load(f)

URL_PATH = 'http://127.0.0.1:5000/car/{}'.format(config['car'])
HEADERS = {'Content-Type': 'application/json'}

s = sched.scheduler(time.time, time.sleep)

DATA = {
    "status": False,
    "int_temp": 0,
    "ext_temp": 0,
    "cool_temp": 0,
    "voltage": 0
}


def update_status(sc):
    s.enter(60, 1, update_status, (sc,))                                            # Run every 60sec
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


s.enter(60, 1, update_status, (s,))
s.run()

if __name__ == '__main__':
  pass
