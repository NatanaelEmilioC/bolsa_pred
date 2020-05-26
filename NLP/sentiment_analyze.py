import requests
import json
import datetime
import pandas as pd
import numpy as np

def gerar_compilado_completo():
    try:
        conteudo_novo = open('NLP/NLP_response.json').read()
        conteudo_antigo = open('NLP/NLP_response_completo.json').read()

        dados_novos = json.loads(conteudo_novo)
        dados_antigos = json.loads(conteudo_antigo)
        #print ("The list printed sorting by data: ")
        # conteudo_novo_ordenado = (sorted(dados_novos, key = lambda i: i['data'], reverse=False))

        conteudo_ordenado = dados_antigos + dados_novos
    
    # print(len(dados_antigos), len(conteudo_novo_ordenado))
    except:
        conteudo_novo = open('NLP/NLP_response.json').read()
        conteudo_ordenado = json.loads(conteudo_novo)    
    
    escrever = open('NLP/NLP_response_completo.json', 'w', encoding='utf-8')

    escrever.write("[\n")
    tamanho = len(conteudo_ordenado)

    for i in conteudo_ordenado:
        json.dump((i), escrever)
        if tamanho != 1:
            escrever.write(",\n")
            tamanho -= 1

    escrever.write("\n]\n")
    escrever.close


def analize(noticia, targets):

    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('version', '2019-07-12'),
    )

    data = '{\n  "text": "'+ noticia +'",\n  "features": {\n    "sentiment": {\n      "targets": [\n        ' + targets + ' ]\n    }  }\n}'

    response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'P3xVYWx66kdOxKcCaUCGKX8gpjtcdx_6asyLxYQFcbtM'))

    print(response.text)


def get_targets(noticia):

    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('version', '2019-07-12'),  
    )

    data = '{\n  "text": "'+ noticia +'",\n  "features": {\n  "keywords": {\n    "emotion": true, "sentiment": true , "limit": 1 }\n  }\n}'

    response = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', headers=headers, params=params, data=data, auth=('apikey', 'P3xVYWx66kdOxKcCaUCGKX8gpjtcdx_6asyLxYQFcbtM'))

    return response

if __name__ == "__main__":
    
    conteudo = open('C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\Meu_Scrapy\\Meu_Scrapy\\spiders\\istoe_ordenado_teste.json', encoding='utf-8').read()

    input_dict = json.loads(conteudo)

    lista_datas = [item.get('data') for item in input_dict]
    # print(lista_datas)

    lista_resultados_concatenados = []

    for i in lista_datas:

        output_dict = [x for x in input_dict if x['data'] == i]

        resultados_sentiment = [get_targets(item.get('titulo')).json() for item in output_dict]
        
        lista_resultados_concatenados.append(resultados_sentiment)
        print(i)

    # print(titulos_concatenados)
    # print(lista_datas_filtradas)


    dados_processados = [{"data": t, "sentimento": s} for t, s in zip(lista_datas, lista_resultados_concatenados)]

    tamanho = len(dados_processados)

    with open('NLP/NLP_response_completo.json', 'w', encoding='utf-8') as f:
        f.write("[\n")
        
        for i in dados_processados:
            json.dump((i), f)
            if tamanho != 1:
                f.write(",\n")
                tamanho -= 1

        f.write("\n]\n")

    # resultado = get_targets('Saudi Aramco tem queda de 21% no lucro em 2019. Petroleira saudita Aramco tem queda de 20,6% no lucro')
    
    # a = resultado.json()["keywords"]

    # # mydata = {"name": "Apple", "quantity": 42, "date": "2014-02-27" }
    # serialized_data = json.dumps(a)
    # ## to write to a textfile named "whatever":
    # with open('NLP/NLP_response.json', 'w', encoding='utf-8') as f:
    #     f.write(serialized_data)
    #     f.close()

