
import urllib.request
import urllib.parse

import xmltodict


errors = {
    '0': 'Processamento com sucesso',
    '-1': 'Código de serviço inválido',
    '-2': 'CEP de origem inválido',
    '-3': 'CEP de destino inválido',
    '-4': 'Peso excedido',
    '-5': 'O Valor Declarado não deve exceder R$ 10.000,00',
    '-6': 'Serviço indisponível para o trecho informado',
    '-7': 'O Valor Declarado é obrigatório para este serviço',
    '-8': 'Este serviço não aceita Mão Própria',
    '-9': 'Este serviço não aceita Aviso de Recebimento',
    '-10': 'Precificação indisponível para o trecho informado',
    '-11': 'Para definição do preço deverão ser informados, também, o comprimento, a largura e altura do objeto em centímetros (cm).',
    '-12': 'Comprimento inválido.',
    '-13': 'Largura inválida.',
    '-14': 'Altura inválida.',
    '-15': 'O comprimento não pode ser maior que 105 cm.',
    '-16': 'A largura não pode ser maior que 105 cm.',
    '-17': 'A altura não pode ser maior que 105 cm.',
    '-18': 'A altura não pode ser inferior a 2 cm.',
    '-20': 'A largura não pode ser inferior a 11 cm.',
    '-22': 'O comprimento não pode ser inferior a 16 cm.',
    '-23': 'A soma resultante do comprimento + largura + altura não deve superar a 200 cm.',
    '-24': 'Comprimento inválido.',
    '-25': 'Diâmetro inválido',
    '-26': 'Informe o comprimento.',
    '-27': 'Informe o diâmetro.',
    '-28': 'O comprimento não pode ser maior que 105 cm.',
    '-29': 'O diâmetro não pode ser maior que 91 cm.',
    '-30': 'O comprimento não pode ser inferior a 18 cm.',
    '-31': 'O diâmetro não pode ser inferior a 5 cm.',
    '-32': 'A soma resultante do comprimento + o dobro do diâmetro não deve superar a 200 cm.',
    '-33': 'Sistema temporariamente fora do ar. Favor tentar mais tarde.',
    '-34': 'Código Administrativo ou Senha inválidos.',
    '-35': 'Senha incorreta.',
    '-36': 'Cliente não possui contrato vigente com os Correios.',
    '-37': 'Cliente não possui serviço ativo em seu contrato.',
    '-38': 'Serviço indisponível para este código administrativo.',
    '-39': 'Peso excedido para o formato envelope',
    '-40': 'Para definicao do preco deverao ser informados, tambem, o comprimento e a largura e altura do objeto em centimetros (cm).',
    '-41': 'O comprimento nao pode ser maior que 60 cm.',
    '-42': 'O comprimento nao pode ser inferior a 16 cm.',
    '-43': 'A soma resultante do comprimento + largura nao deve superar a 120 cm.',
    '-44': 'A largura nao pode ser inferior a 11 cm.',
    '-45': 'A largura nao pode ser maior que 60 cm.',
    '-888': 'Erro ao calcular a tarifa',
    '006': 'Localidade de origem não abrange o serviço informado',
    '007': 'Localidade de destino não abrange o serviço informado',
    '008': 'Serviço indisponível para o trecho informado',
    '009': 'CEP inicial pertencente a Área de Risco.',
    '010': 'CEP de destino está temporariamente sem entrega domiciliar. A entrega será efetuada na agência indicada no Aviso de Chegada que será entregue no endereço do destinatário',
    '011': 'CEP de destino está sujeito a condições especiais de entrega pela ECT e será realizada com o acréscimo de até 7 (sete) dias úteis ao prazo regular.',
    '7': 'Serviço indisponível, tente mais tarde',
    '99': 'Outros erros diversos do .Net',
}


RESPONSE_TESTE = """
<?xml version="1.0" encoding="ISO-8859-1" ?>
<Servicos>
    <cServico>
        <Codigo>04510</Codigo>
        <Valor>26,20</Valor>
        <PrazoEntrega>6</PrazoEntrega>
        <ValorSemAdicionais>26,20</ValorSemAdicionais>
        <ValorMaoPropria>0,00</ValorMaoPropria>
        <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
        <ValorValorDeclarado>0,00</ValorValorDeclarado>
        <EntregaDomiciliar>S</EntregaDomiciliar>
        <EntregaSabado>N</EntregaSabado>
        <obsFim></obsFim>
        <Erro>0</Erro>
        <MsgErro></MsgErro>
    </cServico>
</Servicos>
"""

SERVICOS_SEM_CONTRATO = {
    '04014': 'SEDEX à vista',
    '04065': 'SEDEX à vista pagamento na entrega',
    '04510': 'PAC à vista',
    '04707': 'PAC à vista pagamento na entrega',
    '40169': 'SEDEX 12 ( à vista e a faturar)*',
    '40215': 'SEDEX 10 (à vista e a faturar)*',
    '40290': 'SEDEX Hoje Varejo*',
}

ENDPOINT = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?"
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
    f = urllib.request.urlopen(url)
    response = f.read().decode('utf-8')
    return response

def parse(xml):
    return xmltodict.parse(xml)

def get_servicos_list(data):
    return data['Servicos']['cServico']


def main():
    url = get_url(ENDPOINT, PARAMS_TESTE)
    data = parse(handle_request(url))
    fretes = get_servicos_list(data)
    return fretes