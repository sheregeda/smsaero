# coding: utf-8
import unittest
import httpretty
from urlparse import urljoin
from datetime import datetime, timedelta
from smsaero.api import SmsAero
from smsaero.api import (
    DateValueError, UnexpectedMessageFormat, UnexpectedResponse, InvalidUse
)


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = SmsAero('test', 'test')

    def test__check_response(self):
        try:
            self.api._check_response(
                "incorrect language in '' use the cyrillic or roman alphabet")
            self.assertTrue(False)
        except UnexpectedMessageFormat:
            pass

        try:
            self.api._check_response('some text')
            self.assertTrue(False)
        except UnexpectedResponse:
            pass

        try:
            self.api._check_response(
                '{"reason": "empty field", "result": "reject"}')
            self.assertTrue(False)
        except InvalidUse:
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
                date='datetime.now() + timedelta(1)',
            )
            self.assertTrue(False)
        except DateValueError:
            pass

if __name__ == '__main__':
    unittest.main()
