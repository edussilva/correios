
from urllib.request import urlopen
import urllib.parse
from decimal import Decimal

import requests
import xmltodict
from xml.parsers.expat import ExpatError

from correios.config import ENDPOINT, ERRORS


class CorreioException(Exception):
    """
    Exibe a mensagem de erro da api
    """
    pass


def get_url(endpoint, params):
    querystring = urllib.parse.urlencode(params, doseq=True)
    return f'{endpoint}?{querystring}'


def handle_request(url):
    response = requests.get(url)
    return response.text


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

    if isinstance(d, dict) and d.get('Erro') != '0':
        msg = 'Erro {codigo} ({desc}): {mensagem}'.format(
            codigo=d.get('Erro'),
            desc=ERRORS.get(d.get('Erro')),
            mensagem=d.get('MsgErro')
        )
        raise CorreioException(msg)
    return d


def convert_types(servicos):
    """
    Converte os valores recebidos nos tipos adequados
    """
    if isinstance(servicos, dict):
        servicos = [servicos,]

    list_dicts = []
    for s in servicos:
        keys = s.keys()
        if 'Valor' in keys:
            valor = s['Valor'].replace(',', '.')
            s['Valor'] = Decimal(valor)

        if 'PrazoEntrega' in keys:
            s['PrazoEntrega'] = int(s['PrazoEntrega'])
            
        if 'ValorSemAdicionais' in keys:
            valor = s['ValorSemAdicionais'].replace(',', '.')
            s['ValorSemAdicionais'] = Decimal(valor)
            
        if 'ValorMaoPropria' in keys:
            valor = s['ValorMaoPropria'].replace(',', '.')
            s['ValorMaoPropria'] = Decimal(valor)
            
        if 'ValorAvisoRecebimento' in keys:
            valor = s['ValorAvisoRecebimento'].replace(',', '.')
            s['ValorAvisoRecebimento'] = Decimal(valor)
            
        if 'ValorValorDeclarado' in keys:
            valor = s['ValorValorDeclarado'].replace(',', '.')
            s['ValorValorDeclarado'] = Decimal(valor)
            
        list_dicts.append(s)
    return list_dicts


def calc_preco_prazo(cep_origem, cep_destino, peso, altura, largura, 
        comprimento, servicos=['04510', '04014'], empresa='', senha='', 
        clean_types=True, **kwargs):
    params = {        
        'nCdFormato': '1',
        'sCdMaoPropria': 'n',
        'nVlValorDeclarado': '0',
        'sCdAvisoRecebimento': 'n',
        'nVlDiametro': '0',
        'StrRetorno': 'xml',
        'nIndicaCalculo': '3',    
    }
    params['nCdServico'] = ','.join(servicos)
    params['sCepOrigem'] = cep_origem
    params['sCepDestino'] = cep_destino
    params['nVlPeso'] = peso
    params['nVlComprimento'] = comprimento
    params['nVlAltura'] = altura
    params['nVlLargura'] = largura
    params['nCdEmpresa'] = empresa
    params['sDsSenha'] = senha
    params.update(kwargs)
    
    url = get_url(ENDPOINT, params)
    raw = handle_request(url)
    data = parse_xml(raw)
    fretes = get_servicos_list(data)
    if clean_types:
        fretes = convert_types(fretes)
    return fretes
