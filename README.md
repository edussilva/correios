# correios
API para consulta de frete dos correios

# Documentação
https://www.correios.com.br/a-a-z/pdf/calculador-remoto-de-precos-e-prazos/manual-de-implementacao-do-calculo-remoto-de-precos-e-prazos


# Exemplo

```python
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
```
