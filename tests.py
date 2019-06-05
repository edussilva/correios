import unittest
import collections

from correios.core import (
    get_url,
)

class TestGetUrl(unittest.TestCase):
    def setUp(self):
        self.endpoint = 'http://test.com/'

    def test_empty_params(self):
        params = {}
        expected = 'http://test.com/?'
        self.assertEqual(get_url(self.endpoint, params), expected)

    def test_one_param(self):
        params = {
            'foo': 'bar',
        }
        expected = 'http://test.com/?foo=bar'
        self.assertEqual(get_url(self.endpoint, params), expected)

    def test_n_params(self):
        params = collections.OrderedDict()
        params['foo'] = 'bar'
        params['uni'] = 'duni te'
        params['abra'] = 'cadabra'
        
        expected = 'http://test.com/?foo=bar&uni=duni+te&abra=cadabra'
        self.assertEqual(get_url(self.endpoint, params), expected)


if __name__ == '__main__':
    unittest.main()
