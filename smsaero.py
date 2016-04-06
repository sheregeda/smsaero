# coding: UTF-8
import urlparse
import json
import requests
import hashlib


class SmsAero(object):
    def __init__(self, url_gate, user, passwd, sign):
        self.url_gate = url_gate
        self.user = user
        self.sign = sign
        self.session = requests.session()

        m = hashlib.md5()
        m.update(passwd)
        self.passwd = m.hexdigest()

    def __request(self, selector, data):
        data.update({
            'answer': 'json',
            'user': self.user,
            'password': self.passwd,
            'from': self.sign,
        })
        url = urlparse.urljoin(self.url_gate, selector)
        return self.session.post(url, data=data, verify=False).json()

    def send(self, to, text, digital=0, type_send=2):
        data = {
            'digital': digital,
            'type_send': type_send,
            'to': to,
            'text': text,
        }
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
