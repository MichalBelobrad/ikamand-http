#!/usr/bin/env python3
import sys
import time
import uuid
import requests

# converts key value pairs delimited by & to a dictionary
def convert_to_dict(text):
    dictionary = {}
    for line in text.split('&'):
        if line:
            key, value = line.split('=')
            dictionary[key] = value
    return dictionary

# translates ikamands raw state into a meaningful dictionary
# Example input: time=845&rm=0&acs=0&csid=&cm=0&ag=0&as=0&pt=26&t1=26&t2=400&t3=400&dc=0&tpt=0
def translate_ikamand_state(raw_text):
    input = convert_to_dict(raw_text)
    dictionary = {}
    dictionary['time'] = input['time']
    dictionary['rm'] = input['rm']              # TODO: what's this?
    dictionary['active'] = input['acs']
    dictionary['session_id'] = input['csid']
    dictionary['cm'] = input['cm']              # TODO: what's this?
    dictionary['ag'] = input['ag']              # TODO: what's this?
    dictionary['as'] = input['as']              # TODO: what's this?
    dictionary['pit_temp'] = input['pt']
    dictionary['probe_1_temp'] = input['t1']
    dictionary['probe_2_temp'] = input['t2']
    dictionary['probe_3_temp'] = input['t3']
    dictionary['fan_speed'] = input['dc']
    dictionary['target_temp'] = input['tpt']
    return dictionary


def get_status(ip):
    r = requests.get('http://' + ip + '/cgi-bin/data')

    if r.status_code != requests.codes.ok:
        print('Request failed')

    result = translate_ikamand_state(r.text)
    return result


def start_cook(ip):
    current_time = time.time()
    current_time_plus_one_day = current_time + 86400

    payload = {
        "acs": 1,                               # active cook session
        "csid": uuid.uuid4(),                   # cook session id
        "tpt": 50,                              # target pit temperature
        "sce": current_time_plus_one_day,       # session end time
        "p": 1,                                 # probe number
        "tft": 50,                              # target food temperature
        "as": 0,                                # TODO: what's this?
        "ct": current_time,     # current time
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('http://' + ip + '/cgi-bin/cook', data=payload, headers=headers)
    if r.status_code != requests.codes.ok:
        print('Request failed')

    print("ikamand response: " + r.text)


def stop_cook(ip):
    payload = {
        "acs": 0,                           # active cook session
        "csid": '',                         # cook session id
        "tpt": 120,                         # target pit temperature
        "sce": 0,                           # TODO: what's this?
        "p": 0,                             # probe number (1,2,3)
        "tft": 0,                           # target food temperature
        "as": 0,                            # TODO: what's this?
        "ct": int(time.time()),             # current time
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('http://' + ip + '/cgi-bin/cook', data=payload, headers=headers)
    if r.status_code != requests.codes.ok:
        print('Request failed')

    print("ikamand response: " + r.text)


def print_help():
    print('Usage: ikamand_control.py <ip_address> <mode>')
    print('Available modes: watch, start, stop')
    sys.exit(1)


if __name__ == '__main__':
    # print help if no arguments are provided
    if len(sys.argv) < 3:
        print_help()

    ikamand_ip = sys.argv[1]
    mode = sys.argv[2]

    if mode == 'watch':
        while True:
            for key, value in get_status(ikamand_ip).items():
                print(key + ' = ' + value, end=' | ')
            print()
            time.sleep(1)
    elif mode == 'start':
        start_cook(ikamand_ip)
    elif mode == 'stop':
        stop_cook(ikamand_ip)
    else:
        print_help()