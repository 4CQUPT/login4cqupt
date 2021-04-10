#  create by ourongxing
#  detail url: https://github.com/ourongxing/login4cqupt

import requests
import argparse
import socket
import os
import sys
import subprocess

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def check_ssid():
    if sys.platform == 'linux':
        try: 
            str = 'nmcli -t -f NAME connection show --active'
            ssid = subprocess.check_output(str.split()).decode('utf-8')
        except:
            print("您需要安装 NetworkManger，请自行 Google 安装！")
        else:
            if 'CQUPT' in ssid:
                return True
            else:
                return False
    #  elif sys.platform == 'win32':

def login(ip, args):
    args.ip = ip
    args.device = 0 if args.device == 'pc' else 1
    for i in range(5):
        res = requests.get('http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name='.format_map(vars(args)))
        if '"msg":""' in res.text:
            print('您已经登录')
            return
        elif r'\u8ba4\u8bc1\u6210\u529f' in res.text:
            print('可以上网了')
            return

def get_args():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('account')
    parser.add_argument('password')
    parser.add_argument('-o',
                        '--operator',
                        default='cmcc',
                        choices=['cmcc', 'telecom'],
                        help='operator, cmcc or telecom')
    parser.add_argument('-d',
                        '--device',
                        default='pc',
                        choices=['pc', 'phone'],
                        help='fake device, phone or pc')
    return parser.parse_args()

if __name__ == '__main__':
    if check_ssid():
        login(get_ip(), get_args())
