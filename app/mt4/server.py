import string
import random

from django.conf import settings
from socket import socket
from .constants import *


class AccountObject(object):
    def __init__(self):
        self.master_pwd = settings.MT4_MASTER_PWD
        self.master_balance_pwd = settings.MT4_MASTER_BALANCE_PWD
        self.user_ip = ''
        self.account_id = ''
        self.group_id = ''
        self.name = ''
        self.user_pwd = self.generate_password()
        self.inv_pwd = self.generate_password()
        self.email = ''
        self.country = ''
        self.state = ''
        self.city = ''
        self.address = ''
        self.comment = ''
        self.phone = ''
        self.phone_pwd = self.generate_password()
        self.status = ''
        self.zipcode = ''
        self.doc_number = ''
        self.leverage = ''
        self.agent = ''
        self.send_reports = ''
        self.deposit = ''

    def generate_password(self, length=8):
        """Generate a random string of letters, digits characters """
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    def from_user(self, user):
        self.deposit = '0'
        self.email = user.email
        self.country = user.country
        self.group_id = '3'
        self.send_reports = '0'
        self.phone = user.phone
        self.agent = '-'
        self.leverage = '500'
        self.zipcode = user.promo
        self.city = user.city
        self.status = '0'
        self.doc_number = '-'
        self.name = f'{user.first_name} {user.last_name}'
        self.user_ip = ''

    def to_dict(self):
        return {
            'master_pwd': self.master_pwd,
            'master_balance_pwd': self.master_balance_pwd,
            'user_ip': self.user_ip,
            'account_id': self.account_id,
            'group_id': self.group_id,
            'name': self.name,
            'user_pwd': self.user_pwd,
            'inv_pwd': self.inv_pwd,
            'email': self.email,
            'country': self.country,
            'state': self.state,
            'city': self.city,
            'address': self.address,
            'comment': self.comment,
            'phone': self.phone,
            'phone_pwd': self.phone_pwd,
            'status': self.status,
            'zipcode': self.zipcode,
            'doc_number': self.doc_number,
            'leverage': self.leverage,
            'agent': self.agent,
            'send_reports': self.send_reports,
            'deposit': self.deposit,
        }

    def get_mq_create_string(self):
        mq_string = MT4_CREATE_ACCOUNT
        acc_dict = self.to_dict()
        for k, v in acc_dict.items():
            mq_string = mq_string.replace(f'{{{k}}}', v)
        return mq_string

    def get_mq_change_balance_string(self, amount, description):
        mq_string = MT4_UPDATE_BALANCE
        acc_dict = self.to_dict()
        for k, v in acc_dict.items():
            mq_string = mq_string.replace(f'{{{k}}}', v)
        mq_string = mq_string.replace(f'{{amount}}', amount).replace(f'{{description}}', description)
        return mq_string


class Mt4Server(object):
    def __init__(self):
        self.host = settings.MT4_HOST
        self.port = settings.MT4_PORT
        self.master_pwd = settings.MT4_MASTER_PWD
        self.master_balance_pwd = settings.MT4_MASTER_BALANCE_PWD

    def _send(self, query):
        mq = socket()
        mq.connect((self.host, self.port))
        q = f'W{query}\r\nQUIT\r\n'.encode('cp1251')
        mq.sendall(q)
        receive = self._receive(mq)
        mq.close()
        if len(receive):
            r = receive.split(b'\r\n')
            if r[0] == b'OK':
                return r[1].decode('cp1251')
        return None

    @staticmethod
    def _receive(sock):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 4096:
            chunk = sock.recv(min(4096 - bytes_recd, 2048))
            if chunk == b'':
                break
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def last_account(self):
        pass

    def change_balance(self, account: AccountObject, amount, description) -> bool:
        result = self._send(account.get_mq_change_balance_string(amount, description))
        if result:
            return True
        return False

    def create_account(self, account: AccountObject):
        result = self._send(account.get_mq_create_string())
        if result:
            result = result.split('=')
            if len(result) == 2:
                return result[1]
        return None
