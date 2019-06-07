
from urllib.request import urlopen
import urllib.parse

import xmltodict
from xml.parsers.expat import ExpatError

from correios.config import ENDPOINT, ERRORS


PARAMS_TESTE = {
    'nCdEmpresa': '08082650',
    'sDsSenha': '564321',
    'sCepOrigem': '70002900',
    'sCepDestino': '04547000',
    'nVlPeso': '1',
    'nCdFormato': '1',
    'nVlComprimento': '20',
    'nVlAltura': '20',
    'nVlLargura': '20',
    'sCdMaoPropria': 'n',
    'nVlValorDeclarado': '0',
    'sCdAvisoRecebimento': 'n',
    'nCdServico': '04510,04014',
    'nVlDiametro': '0',
    'StrRetorno': 'xml',
    'nIndicaCalculo': '3',
}

def get_url(endpoint, params):
    querystring = urllib.parse.urlencode(params, doseq=True)
    return f'{endpoint}?{querystring}'

def handle_request(url):
    f = urlopen(url)
    response = f.read().decode('utf-8')
    return response

def parse_xml(xml):
    try:
        data = xmltodict.parse(xml)
    except ExpatError:
        data = {}
    return data

def get_servicos_list(data):
    try:
        d = data['Servicos']['cServico']
    except (KeyError, TypeError):
        d = [] 
    return d


def fretes():
    url = get_url(ENDPOINT, PARAMS_TESTE)
    data = parse_xml(handle_request(url))
    fretes = get_servicos_list(data)
    return fretes