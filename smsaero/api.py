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


class DateValueError(SmsAeroError):
    """ Exception raised when value date incorrectly. """
    pass


class UnexpectedMessageFormat(SmsAeroError):
    """ incorrect language in '...' use the cyrillic or roman alphabet. """
    pass


class UnexpectedResponse(SmsAeroError):
    """ Exception raised when unexpected format is received. """
    pass


class InvalidUse(SmsAeroError):
    """ Exception raised when API method is not used correctly. """
    pass


class SmsAero(object):
    URL_GATE = 'http://gate.smsaero.ru/'
    SIGNATURE = 'NEWS'

    def __init__(self, user, passwd, url_gate=URL_GATE, sign=SIGNATURE):
        self.user = user
        self.url_gate = url_gate
        self.sign = sign
        self.session = requests.session()

        m = hashlib.md5()
        m.update(passwd)
        self.passwd = m.hexdigest()

    def _request(self, selector, data):
        data.update({
            'user': self.user,
            'password': self.passwd,
            'from': self.sign,
        })
        url = urljoin(self.url_gate, selector)
        return self._check_response(self.session.post(url, data=data).content)

    def _check_response(self, content):
        try:
            response = json.loads(content)
            if response['result'] == u'reject':
                raise InvalidUse(response['reason'])
            return response
        except ValueError:
            if 'incorrect language' in content:
                raise UnexpectedMessageFormat(content)
            else:
                raise UnexpectedResponse()

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
                raise DateValueError('param `date` is not datetime object')

        return self._request('/send/', data)
