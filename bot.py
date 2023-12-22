from time import sleep
import socket
import re
from datetime import datetime
import threading
import json

import requests

import cnfg
import utils


def main():
    s = socket.socket()
    s.connect((cnfg.HOST, cnfg.PORT))
    s.send('PASS {}\r\n'.format(cnfg.PASS).encode('utf-8'))
    s.send('NICK {}\r\n'.format(cnfg.NICK).encode('utf-8'))
    s.send('JOIN #{}\r\n'.format(cnfg.CHANNEL).encode('utf-8'))

    chat_message = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
    utils.mess(s, 'Bot in chat now')
    scan_thread = threading.Thread(utils.scan_chat())
    scan_thread.start()
    while True:
        resp = s.recv(1024).decode('utf-8')
        if resp == 'PING :tmi.twitch.tv\r\n':
            s.send('PONG :tmi.twitch.tv\r\n'.encode('utf-8'))
        else:
            username = re.search(r'\w+', resp).group(0)
            message = chat_message.sub('', resp)

            if message.strip() == '!time':
                r = requests.get(cnfg.TIME_URL, headers=cnfg.HEADERS)
                dict_data = json.loads(r.text)
                start = dict_data["data"][0]['started_at']
                now_dt = datetime.now()
                start_dt = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
                diff_time = now_dt - start_dt
                diff_tz = diff_time.seconds - 3 * 60 * 60
                utils.mess(s, username + ', uptime: ' + utils.convert_to_preferred_format(diff_tz))

            if message.strip() == '!some':
                utils.mess(s, 'Some message!')

            if message.strip() == '!another':
                utils.mess(s, 'another message')

            if message.strip() == '!at':
                with open('utime.json', 'r', encoding='utf-8') as utf:
                    users_time_data = json.load(utf)
                    if username in users_time_data.keys():
                        utils.mess(s, username + ', your total time watching this channel:' + utils.convert_to_preferred_format(
                                       users_time_data[username]))
                    else:
                        utils.mess(s, username + ', too few time')

        sleep(1)


if __name__ == '__main__':
    main()
