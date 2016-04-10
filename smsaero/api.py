# coding: UTF-8
import json
import time
import requests
import hashlib
from urlparse import urljoin
from datetime import datetime


class SmsAero(object):
    URL_GATE = 'https://gate.smsaero.ru/'
    SIGNATURE = 'NEWS'

    def __init__(self, user, passwd, url_gate=None, sign=None):
        self.user = user
        self.url_gate = url_gate if url_gate else URL_GATE
        self.sign = sign if sign else SIGNATURE
        self.session = requests.session()

        m = hashlib.md5()
        m.update(passwd)
        self.passwd = m.hexdigest()

    def __request(self, selector, data):
        data.update({
            'user': self.user,
            'password': self.passwd,
            'from': self.sign,
        })
        url = urljoin(self.url_gate, selector)
        return self.session.post(url, data=data).json()

    def send(self, to, text, date=None, digital=0, type_send=2, answer='json'):
        data = {
            'digital': digital,
            'type_send': type_send,
            'to': to,
            'text': text,
            'answer': answer,
        }

        if date is not None:
            if isinstance(date, datetime):
                data.update({'date': int(time.mktime(date.timetuple()))})
            else:
                raise Exception('param `date` is not datetime object')

        return self.__request('/send/', data)

    def send_to_group(self):
        pass

    def get_status(self):
        pass

    def check_sending(self):
        pass

    def get_balance(self):
        pass

    def check_tarif(self):
        pass

    def get_senders(self):
        pass

    def get_sign(self):
        pass

    def get_sign(self):
        pass

    def check_group(self):
        pass

    def add_group(self):
        pass

    def del_group(self):
        pass

    def add_phone(self):
        pass

    def del_phone(self):
        pass

    def add_blacklist(self):
        pass
