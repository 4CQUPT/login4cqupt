#  create by ourongxing
#  detail url: https://github.com/ourongxing/login4cqupt 
import argparse
import os
import time

import requests


def login(ip, args):
    args.ip = ip
    print(ip)
    args.device = 0 if args.device == 'pc' else 1
    res = requests.get(
        'http://192.168.200.2:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C{device}%2C{account}%40{operator}&user_password={password}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=192.168.200.1&wlan_ac_name=&jsVersion=3.3.3&v=3133'.format_map(
            vars(args)))

    if '"msg":""' in res.text:
        print('当前设备已登录', res.text)
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
    ip = '10.16.24.2'
    try:
        res = requests.get('http://192.168.200.2')
        begin_index = res.text.index("v4ip=") + 6
        end_index = res.text.index("'", begin_index + 1)
        ip = res.text[begin_index: end_index]
        print('v4ip:')
    except:
        # For not login
        try:
            res = requests.get('http://192.168.200.2')
            print('v46ip:')
            begin_index = res.text.index("v46ip=") + 7
            end_index = res.text.index("'", begin_index + 1)
            ip = res.text[begin_index: end_index]
        except:
            ip = '10.16.24.22'
            print('Error')
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


def is_login():
    exit_code = os.system('/sbin/ping baidu.com -c 3')
    if exit_code:
        return False
    return True


if __name__ == '__main__':
    state = is_login()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if state:
        print('在线,不需要重新登录\n')
    else:
        ip = get_ip()
        args = get_args()
        login(ip, args)
        print('\n')
