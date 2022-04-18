#  create by ourongxing
#  detail url: https://github.com/ourongxing/login4cqupt 
import requests
import argparse
import socket
import os
import sys
import subprocess

def login(ip, args):
    args.ip = ip
    args.device = 0 if args.device == 'pc' else 1
    res = requests.get('http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name='.format_map(vars(args)))
    if '"msg":""' in res.text:
        print('当前设备已登录')
        return
    elif r'\u8ba4\u8bc1\u6210\u529f' in res.text:
        print('登录成功')
        return
    elif 'bGRhcCBhdXRoIGVycm9y' in res.text:
        print("密码错误")
        return
    elif 'aW51c2UsIGxvZ2luIGFnYWluL' in res.text:
        login(ip, args)
    else:
        print("您可能欠费停机")
        return 

def get_ip():
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

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
    ip = get_ip()
    args = get_args()
    login(ip, args)
