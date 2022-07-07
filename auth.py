import os
import sys
import datetime
from matplotlib.style import use
import requests
from rsa_security import encrypt_by_aes, get_rand_num, decrypt_by_aes
from typing import Tuple, Dict, Any
from loguru import logger


class QiyuanInternetAuthenticationSystem:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.session = requests.Session()


def encrypt(username: str, password: str) -> Tuple[str, str]:
    iv = get_rand_num()
    username_encrypted = encrypt_by_aes(username, iv)
    iv = get_rand_num()
    password_encrypted = encrypt_by_aes(password, iv)
    return username_encrypted, password_encrypted


def login(username_encrypted: str, password_encrypted: str) -> Dict[str, Any]:
    url = 'http://172.16.1.11:8008/portal.cgi'
    data = {
        'username': username_encrypted,
        'password': password_encrypted,
        'uplcyid': '1',
        'language': '0',
        'submit': 'submit',
    }
    res = requests.post(url, data)
    res.encoding = res.apparent_encoding
    if not res.text.startswith('0#'):
        return {
            'status': 'success',
            'msg': '登录成功',
            'data': {
                'username': decrypt_by_aes(res.text.split('&')[0]),
                'loginipaddr': res.text.split('&')[2],
                'logintime': res.text.split('&')[1],
                'secret': res.text.split('&')[3],
            }
        }
    else:
        return {
            'status': 'failure',
            'msg': '登录失败',
            'data': res.text.replace('0#', '')
        }


def logout(username: str, secret: str) -> Dict[str, str]:
    url = 'http://172.16.1.11:8008/logout.cgi'
    data = {
        'username': username,
        'secret': secret,
        'language': '0',
        'submit': 'submit',
    }
    res = requests.post(url, data)
    res.encoding = res.apparent_encoding
    if res.status_code == 200 and res.text == '1':
        return {
            'status': 'success',
            'msg': '注销成功',
            'data': {
                'logouttime': datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"),
            }
        }
    else:
        return {
            'status': 'failure',
            'msg': '注销失败',
            'data': res.text
        }


def get_logger(logfile: str = 'log.txt'):
    logger.remove()
    logger.add(sys.stdout, level='INFO', format='{message}')
    logger.add(logfile, level='INFO', format='{message}')
    return logger


def auth(logfile: str = 'log.txt'):
    logger = get_logger()
    if sys.argv[1] == 'login':
        if os.path.getsize(logfile) == 0:
            username = input('输入用户：')
            password = input('输入密码：')
            username_encrypted, password_encrypted = encrypt(
                username,
                password,
            )
            logger.info(login(username_encrypted, password_encrypted))
            with open('aes.txt', 'w') as f:
                f.write(username_encrypted+'\n'+password_encrypted)
        else:
            with open('aes.txt') as f:
                temp = f.readlines()
                username_encrypted = temp[0].strip()
                password_encrypted = temp[1].strip()
            logger.info(login(username_encrypted, password_encrypted))
    elif sys.argv[1] == 'logout':
        if os.path.getsize(logfile) == 0:
            print('请先登录')
        else:
            with open(logfile, encoding='utf-8') as f:
                data = eval(f.readlines()[-1])['data']
            if 'logouttime' in data:
                print('请先登录')
            else:
                username = data['username']
                secret = data['secret']
                logger.info(logout(username, secret))
    else:
        print('命令错误，请检查输入是否有误')


if __name__ == '__main__':
    auth()
