from pprint import pprint
from correios import calc_preco_prazo


response = calc_preco_prazo(
    cep_origem='70002900',
    cep_destino='04547000',
    peso='1',
    altura='20',
    largura='20',
    comprimento='20',
    servicos=['04510', '04014'],
    empresa='08082650',
    senha='564321',
)
pprint(response)
