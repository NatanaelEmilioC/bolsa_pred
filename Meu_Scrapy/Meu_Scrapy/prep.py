import json
import datetime
import pandas as pd
import re
from unicodedata import normalize

def removerCaracteresEspeciais (text) :
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def ordenar_noticias():
        # lemos o JSON em disco
    try:
        conteudo_novo = open('spiders/istoe.json').read()
        conteudo_antigo = open('spiders/istoe_ordenado.json').read()

        dados_novos = json.loads(conteudo_novo)
        dados_antigos = json.loads(conteudo_antigo) #print ("The list printed sorting by data: ")
        
        conteudo_novo_ordenado = (sorted(dados_novos, key = lambda i: i['data'], reverse=False))

        conteudo_ordenado = dados_antigos + conteudo_novo_ordenado # print(len(dados_antigos), len(conteudo_novo_ordenado))
    
    except:
        conteudo_novo = open('spiders/istoe.json').read()
        dados_novos = json.loads(conteudo_novo)
        conteudo_ordenado = (sorted(dados_novos, key = lambda i: i['data'], reverse=False))

    
    escrever = open('spiders/istoe_ordenado.json', 'w', encoding='utf-8')

    escrever.write("[\n")
    tamanho = len(conteudo_ordenado)

    for i in conteudo_ordenado:
        json.dump((i), escrever)
        if tamanho != 1:
            escrever.write(",\n")
            tamanho -= 1

    escrever.write("\n]\n")
    escrever.close

def filtrar_por_data():
    conteudo = open('spiders/istoe_ordenado.json', encoding='utf-8').read()

    input_dict = json.loads(conteudo)

    lista_datas = [item.get('data') for item in input_dict]
    lista_datas_filtradas = (sorted(set(lista_datas)))

    lista_titulos_concatenados = []

    for i in lista_datas_filtradas:
        # Filter python objects with list comprehensions
        output_dict = [x for x in input_dict if x['data'] == i]
        
        #remover elementos repetidos das noticias
        temp = []
        [temp.append(item) for item in output_dict if not temp.count(item) ]

        #concatenando por data

        lista_titulos= [item.get('titulo') for item in temp]
        titulos_concatenados = '. '.join(str(x) for x in lista_titulos)

        titulos_concatenados = removerCaracteresEspeciais(titulos_concatenados)

        #removendo elementos indesejados
        remover = "]["
        for i in range(0,len(remover)):
            titulos_concatenados =titulos_concatenados.replace(remover[i],"")
        
        lista_titulos_concatenados.append(titulos_concatenados)

    # print(titulos_concatenados)
    # print(lista_datas_filtradas)

    dados_processados = [{"data": t, "titulo": s} for t, s in zip(lista_datas_filtradas, lista_titulos_concatenados)]

    tamanho = len(dados_processados)

    with open('spiders/istoe_ordenado_teste.json', 'w', encoding='utf-8') as f:
        f.write("[\n")
        
        for i in dados_processados:
            json.dump((i), f)
            if tamanho != 1:
                f.write(",\n")
                tamanho -= 1

        f.write("\n]\n")

if __name__ == "__main__":
    ordenar_noticias()
    filtrar_por_data()