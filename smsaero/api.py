#!/usr/bin/env python
# coding: UTF-8
import json
import time
import requests
import hashlib
import json
from urlparse import urljoin
from datetime import datetime


class SmsAeroError(Exception):
    """ Super class of all SmsAero Errors. """
    pass


class SmsAeroHTTPError(SmsAeroError):
    """ A Connection error occurred. """
    pass


class SmsAero(object):
    URL_GATE = 'http://gate.smsaero.ru/'
    SIGNATURE = 'NEWS'

    def __init__(self, user, passwd, url_gate=URL_GATE, signature=SIGNATURE):
        self.user = user
        self.url_gate = url_gate
        self.signature = signature
        self.session = requests.session()

        m = hashlib.md5()
        m.update(passwd)
        self.passwd = m.hexdigest()

    def _request(self, selector, data):
        data.update({
            'user': self.user,
            'password': self.passwd,
            'answer': 'json',
        })
        url = urljoin(self.url_gate, selector)

        try:
            response = self.session.post(url, data=data)
        except requests.RequestException as err:
            raise SmsAeroHTTPError(err)

        if not response.status_code == 200:
            raise SmsAeroHTTPError('response status code is not 200')

        return self._check_response(response.content)

    def _check_response(self, content):
        try:
            response = json.loads(content)
            if 'result' in response and response['result'] == u'reject':
                raise SmsAeroError(response['reason'])
            elif 'result' in response and response['result'] == u'no credits':
                raise SmsAeroError(response['result'])
            return response
        except ValueError:
            if 'incorrect language' in content:
                raise SmsAeroError("incorrect language in '...' use \
                    the cyrillic or roman alphabet.")
            else:
                raise SmsAeroError('unexpected format is received')

    def send(self, to, text, date=None, digital=0, type_send=2):
        data = {
            'from': self.signature,
            'digital': digital,
            'type_send': type_send,
            'to': to,
            'text': text,
        }

        if date is not None:
            if isinstance(date, datetime):
                data['date'] = int(time.mktime(date.timetuple()))
            else:
                raise SmsAeroError('param `date` is not datetime object')

        return self._request('/send/', data)

    def sendtogroup(self, group, text, date=None, digital=0, type_send=2):
        data = {
            'from': self.signature,
            'digital': digital,
            'type_send': type_send,
            'group': group,
            'text': text,
        }

        if date is not None:
            if isinstance(date, datetime):
                data['date'] = int(time.mktime(date.timetuple()))
            else:
                raise SmsAeroError('param `date` is not datetime object')

        return self._request('/sendtogroup/', data)

    def status(self, id):
        return self._request('/status/', {'id': id})

    def checksending(self, id):
        return self._request('/checksending/', {'id': id})

    def balance(self):
        return self._request('/balance/', {})

    def checktarif(self):
        return self._request('/checktarif/', {})

    def senders(self):
        return self._request('/senders/', {})

    def sign(self, sign):
        return self._request('/sign/', {'sign': sign})

    def checkgroup(self):
        return self._request('/checkgroup/', {})

    def addgroup(self, group):
        return self._request('/addgroup/', {'group': group})

    def delgroup(self, group):
        return self._request('/delgroup/', {'group': group})

    def addphone(self, phone, group=None):
        data = {'phone': phone} if group is None \
            else {'phone': phone, 'group': group}

        return self._request('/addphone/', data)

    def delphone(self, phone, group=None):
        data = {'phone': phone} if group is None \
            else {'phone': phone, 'group': group}

        return self._request('/delphone/', data)

    def addblacklist(self, phone):
        return self._request('/addblacklist/', {'phone': phone})
