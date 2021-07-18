#  create by ourongxing
#  detail url: https://github.com/ourongxing/login4cqupt
import requests
import argparse
import socket
import time
import os
import sys
import subprocess

class Login(object):
    def __init__(self, args):
        self.args = args

    def login(self):
        res = requests.get('http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name='.format_map(vars(self.args)))
        if '"msg":""' in res.text:
            print('当前设备已登录')
            return
        elif r'\u8ba4\u8bc1\u6210\u529f' in res.text:
            #  print('登录成功')
            if(self.args.crack):
                time.sleep(3)
                self.logout_fail()
                time.sleep(1)
                self.crack()
            return
        elif 'bGRhcCBhdXRoIGVycm9y' in res.text:
            print("密码错误")
            return
        elif 'aW51c2UsIGxvZ2luIGFnYWluL' in res.text:
            self.login()
        else:
            print("您可能欠费停机")
            return

    # 注销失败后，破解
    def crack(self):
        res = requests.get('http://192.168.200.2:801/eportal/?c=Portal&a=logout&callback=dr1003&login_method=1&user_account=drcom&user_password=123&ac_logout=1&register_mode=1&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_vlan_id=1&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name='.format_map(vars(self.args)))
        if r'\u6ce8\u9500\u6210\u529f' in res.text:
            if self.is_connected():
                print('破解成功')
                return
            else:
                self.login()
        else:
            print('破解失败')
            return

    # 注销失败
    def logout_fail(self):
        requests.get('http://192.168.200.2:801/eportal/?c=portal&a=unbind_mac&callback=dr1003&user_account={account}%40telecom&wlan_user_mac=1ee20b013cc3&wlan_user_ip=10.17.100.31'.format_map(vars(self.args)))

    #  正常注销
    def logout(self):
        requests.get('http://192.168.200.2:801/eportal/?c=Portal&a=unbind_mac&callback=dr1002&user_account={account}%40cmcc&wlan_user_mac=000000000000&wlan_user_ip={ip}'.format_map(vars(self.args)))

    def is_connected(self):
        try:
            requests.get("https://baidu.com",timeout=1)
        except requests.exceptions.RequestException:
            return False
        else:
            return True

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
    parser.add_argument('-c',
                        '--crack',
                        action='store_true',
                        help='logout without offline')
    return parser.parse_args()

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    args = get_args()
    args.ip = get_ip()
    args.device = 0 if args.device == 'pc' else 1
    g = Login(args)
    g.login()
