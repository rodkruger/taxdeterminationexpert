import json
import requests

json_string = """
{
  "login": "fh.api",
  "senha": "5zp%*96l"
}
"""

json_data = json.loads(json_string)
response = requests.post("https://apigestorfiscal.iob.com.br/api/rest/token", json=json_data)
print(response)

json_string = """
{
    "token": "string",
    "id_contrato": 0,
    "id_empresa": 0,
    "sku": "001",
    "descricaoSku": "Produto Teste",
    "departamento_categoria": "Categoria",
    "ean_gtin": "0123456789012",
    "descricaoEan": "EAN",
    "segmento": "PNEUS",
    "ncm": "001",
    "nacionalImportado": "Importado",
    "tributado4": "sim",
    "operacao": "sim",
    "ufOrigem": "SP",
    "ufDestino": "PR",
    "estabelecimentoOrigem": "Jean Soares",
    "tribEstabelecimentoOrigem": "Simples",
    "estabelecimentoDestino": "Rodrigo Krüger",
    "tribEstabelecimentoDestino": "Simples",
    "cnae": "0123",
    "destinacaoMercadoria": "CONSUMO",
    "cest": "1234"
}
"""

data = json.loads(json_string)
response = requests.post("https://apigestorfiscal.iob.com.br/api/rest/incluir-produto", data)
print(response)
