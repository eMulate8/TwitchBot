import json
from time import sleep

import requests

import cnfg


def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minimum = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, minimum, sec)


def mess(sock, message):
    sock.send('PRIVMSG #{} :{}\r\n'.format(cnfg.CHANNEL, message).encode('utf-8'))


def ban(sock, user):
    mess(sock, '.ban {}'.format(user))


def timeout(sock, user, seconds=500):
    mess(sock, '.timeout {}'.format(user, seconds))


def scan_chat():
    head = {'accept': '*/*'}
    with open('utime.json', 'r', encoding='utf-8') as utf:
        utime_dict = json.load(utf)
    while True:
        r = requests.get(cnfg.CHATTERS_URL, headers=head)
        if r.status_code != 502:
            data = json.loads(r.text)
            for user in data['chatters']['viewers']:
                utime_dict[user] += 10
                with open('utime.json', 'w', encoding='utf-8') as utf0:
                    json.dump(utime_dict, utf0)
        sleep(10)
