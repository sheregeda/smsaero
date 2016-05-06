# coding: utf-8
import unittest
import httpretty
import requests
from urlparse import urljoin
from datetime import datetime, timedelta
from smsaero.api import SmsAero, SmsAeroError


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = SmsAero('test', 'test')

    def test__check_response(self):
        try:
            self.api._check_response("incorrect language in '' use the \
                cyrillic or roman alphabet")
            self.assertTrue(False)
        except SmsAeroError:
            pass

        try:
            self.api._check_response('some text')
            self.assertTrue(False)
        except SmsAeroError:
            pass

        try:
            self.api._check_response('{"reason": "empty field", \
                "result": "reject"}')
            self.assertTrue(False)
        except SmsAeroError:
            pass

        try:
            self.api._check_response('{"id": 33166386, "result": "accepted"}')
        except SmsAeroError:
            self.assertTrue(False)

    @httpretty.activate
    def test__request(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/send/'),
            body='{}',
            status=500,
        )

        try:
            response = self.api.send(
                '8911111111',
                'message',
            )
            self.assertTrue(False)
        except SmsAeroError:
            pass

        def exceptionCallback(request, uri, headers):
            raise requests.Timeout('Connection timed out.')

        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/send/'),
            body=exceptionCallback,
            status=200,
            content_type='text/json',
        )

        try:
            response = self.api.send('89111111111', 'message')
            self.assertTrue(False)
        except SmsAeroError:
            pass

    @httpretty.activate
    def test_send(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/send/'),
            body='{"id": 33166386, "result": "accepted"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.send('89111111111', 'message')
        self.assertEqual(response['result'], u'accepted')

        response = self.api.send(
            '89111111111',
            'message',
            date=datetime.now() + timedelta(1),
        )
        self.assertEqual(response['result'], u'accepted')

        try:
            response = self.api.send(
                '8911111111',
                'message',
                date='date value',
            )
            self.assertTrue(False)
        except SmsAeroError:
            pass

        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/send/'),
            body='{"result": "no credits"}',
            status=200,
        )

        try:
            response = self.api.send(
                '8911111111',
                'message',
            )
            self.assertTrue(False)
        except SmsAeroError:
            pass


if __name__ == '__main__':
    unittest.main()
