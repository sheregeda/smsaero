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

    @httpretty.activate
    def test_status(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/status/'),
            body='{"reason": "empty field", "result": "reject"}',
            status=200,
            content_type='text/json',
        )

        try:
            self.api.status(0)
            self.assertTrue(False)
        except SmsAeroError:
            pass

    @httpretty.activate
    def test_balance(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/balance/'),
            body='{"balance": "48.20"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.balance()
        self.assertEqual(response['balance'], u'48.20')

    @httpretty.activate
    def test_checktarif(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/checktarif/'),
            body='{"reason": {"Digital channel": "0.45", \
                "Direct channel": "1.80"}, "result": "accepted"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.checktarif()
        self.assertEqual(response['reason']['Digital channel'], u'0.45')

    @httpretty.activate
    def test_sign(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/sign/'),
            body='{"accepted": "pending"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.sign('awesome')
        self.assertEqual(response['accepted'], u'pending')

    @httpretty.activate
    def test_senders(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/senders/'),
            body='["NEWS", "awesome"]',
            status=200,
            content_type='text/json',
        )

        response = self.api.senders()
        self.assertEqual(response, [u'NEWS', u'awesome'])

    @httpretty.activate
    def test_checkgroup(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/checkgroup/'),
            body='{"reason": ["Личные контакты"], "result": "accepted "}',
            status=200,
            content_type='text/json',
        )

        response = self.api.checkgroup()
        self.assertEqual(response['reason'], [u'Личные контакты'])

    @httpretty.activate
    def test_addgroup(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/addgroup/'),
            body='{"reason": "Group created", "result": "accepted"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.addgroup('test')
        self.assertEqual(response['result'], u'accepted')
        self.assertEqual(response['reason'], u'Group created')

    @httpretty.activate
    def test_delgroup(self):
        httpretty.register_uri(
            httpretty.POST,
            urljoin(SmsAero.URL_GATE, '/delgroup/'),
            body='{"reason": "Group delete", "result": "accepted"}',
            status=200,
            content_type='text/json',
        )

        response = self.api.delgroup('test')
        self.assertEqual(response['result'], u'accepted')
        self.assertEqual(response['reason'], u'Group delete')

if __name__ == '__main__':
    unittest.main()
