import requests
import pandas as pd
import io

# Link para à API
API_URL = "http://137.184.108.252:5000/api"
# Corpo da requisição com as credenciais
body = {
            "email": "theusgesteira@gmail.com",
            "password": "6SAHvzShLSHn"
}
# 1ª Requisição
r1 = requests.post(API_URL+"/login", json=body)

if r1.status_code == 200:
    # Se a requisição for um sucesso, eu pego o token da resposta
    token = r1.json()['token']
    print(f'TOKEN: {token}')
    # 2ª requisição, dessa vez para a parte de cidades e mandando o token no cabeçalho
    r2 = requests.get(API_URL+"/cidades", headers={'x-access-token': token})
    if r2.status_code == 200:
        # Se a requisição for um sucesso, converto a resposta em um dataframe do pandas
        df = pd.read_json(io.StringIO(r2.text))
        # Renomeando a coluna nome para cidade
        df.rename(columns={"nome": 'Cidade'}, inplace=True)
        # Convertendo o df sem index para table em html
        table_html = df.to_html(index=False)

        # Passa a table para um arquivo html
        with open('table.html', mode='a', encoding='utf-8') as fp:
            fp.write(table_html)

        # Junto todos os outros arquivos html para ter um código funcional
        html = ''
        for file in ['inicio.html', 'table.html', 'fim.html']:
            with open(file, encoding='utf-8') as fp:
                html += fp.read()
                html += '\n'

        with open('index.html', mode='a', encoding='utf-8') as fp:
            fp.write(html)

