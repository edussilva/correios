import unittest
import collections
from unittest import mock
from unittest.mock import MagicMock
from io import StringIO

from correios.core import (
    get_url,
    parse_xml,
    get_servicos_list,
    handle_request,
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


class TestParseXML(unittest.TestCase):
    def setUp(self):
        self.xml = """<?xml version="1.0" encoding="ISO-8859-1" ?>
        <Servicos>
            <cServico>
                <Codigo>04510</Codigo>
                <Valor>26,20</Valor>
                <PrazoEntrega>6</PrazoEntrega>
            </cServico>
        </Servicos>"""

    def test_empty_string(self):
        xml = ''
        self.assertEqual(parse_xml(xml), {})

    def test_xml_with_empty_value(self):
        xml = '<?xml version="1.0" encoding="ISO-8859-1" ?><Servicos></Servicos>'
        expected = {
            'Servicos': None,
        }
        self.assertEqual(parse_xml(xml), expected)

    def test_parse_xml_ok(self):
        expected = {
            'Servicos': {
                'cServico': {
                    'Codigo': '04510',
                    'Valor': '26,20',
                    'PrazoEntrega': '6',
                }
            }
        }
        self.assertEqual(parse_xml(self.xml), expected)



class TestGetServicosList(unittest.TestCase):
    def test_empty_dict(self):
        data = {}
        self.assertEqual(get_servicos_list(data), [])

    def test_with_servicos_empty(self):
        data = {
            'Servicos': '',
        }
        self.assertEqual(get_servicos_list(data), [])

    def test_with_servicos_and_servico_not_dict(self):
        data = {
            'Servicos': {
                'cServico': ['foo', 'bar'],
            }
        }
        self.assertEqual(get_servicos_list(data), ['foo', 'bar'])


# RESPONSE_MOCK_OK = """<?xml version="1.0" encoding="ISO-8859-1" ?>
# <Servicos>
#     <cServico>
#         <Codigo>04510</Codigo>
#         <Valor>26,20</Valor>
#         <PrazoEntrega>6</PrazoEntrega>
#         <ValorSemAdicionais>26,20</ValorSemAdicionais>
#         <ValorMaoPropria>0,00</ValorMaoPropria>
#         <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
#         <ValorValorDeclarado>0,00</ValorValorDeclarado>
#         <EntregaDomiciliar>S</EntregaDomiciliar>
#         <EntregaSabado>N</EntregaSabado>
#         <obsFim></obsFim>
#         <Erro>0</Erro>
#         <MsgErro></MsgErro>
#     </cServico>
# </Servicos>"""


# class TestHandleRequest(unittest.TestCase):
#     def setUp(self):
#         self.url = 'http://test.com/?foo=bar&uni=duni+te&abra=cadabra'

#     @mock.patch('correios.core.urlopen', return_value=StringIO(RESPONSE_MOCK_OK)) 
#     def test_response_ok(self, mock_urlopen):
#         self.assertEqual(handle_request(self.url), RESPONSE_MOCK_OK)


if __name__ == '__main__':
    unittest.main()
