
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
    """
    Parametriza uma url a partir dos parâmetros e mum dicionário

    :param endpoint: A url base
    :param params: Um dicionário de parâmetros
    :return: retorna uma url parametrizada
    """
    querystring = urllib.parse.urlencode(params, doseq=True)
    return f'{endpoint}?{querystring}'


def handle_request(url):
    """
    Faz a requisição e retorna o conteúdo da resposta

    :param url: A url da requisição
    :return: O conteúdo da resposta
    """
    response = requests.get(url)
    return response.text


def parse_xml(xml):
    """
    Converte um xml em dicionário

    :param xml: Uma string que representa um xml
    :return: Um dicionário que representa o xml
    """
    try:
        data = xmltodict.parse(xml)
    except ExpatError:
        data = {}
    return data


def get_servicos_list(data):
    """
    Recebe um dicionário com a estrutura da resposta da requisição e organiza 
    as informações em uma lista de serviços.
    Caso a resposta seja de apenas um serviço, retorna um dicionário

    :param data: dicionário convertido a partir do xml da resposta da 
    requisição
    :return: Uma list de serviços (dicionário) ou apenas um dicionário.
    Se a resposta da chamada retornar um erro, exibe a Exception
    """
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

    :param servicos: lista de serviços ou um dicionário de serviço.
    Caso seja um dicionário, converte em uma lista com apenas um elemento
    :return: uma lista de serviços onde os valores contém os tipos adequados
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
    """
    Retorna os serviços de fretes com base nas informações passadas

    :param cep_origem: O cep da região que sairá o pacote - apenas dígitos
    :param cep_destino: O cep da região que será enviado o pacote - 
    apenas dígitos
    :param peso: Peso em Kg no formato string. Utilizar até duas casas 
    decimais (ex. '2.34')
    :param altura: Altura em cm no formato string. Utilizar até duas casas 
    decimais (ex. '11.54')
    :param largura: Largura em cm no formato string. Utilizar até duas casas 
    decimais (ex. '11.54')
    :param comprimento: Comprimento em cm no formato string. Utilizar até duas
    casas decimais (ex. '11.54')
    :param servicos: Lista de códigos de serviço dos correios que deverá ser 
    consultada
    :parm empresa: Código da empresa para chamadas com contrato
    :param senha: Senha para chamadas com contrato
    :param clean_types: Retorna os valores da resposta no tipo correto.
    Caso contrário todas as respostas serão em string
    """

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
