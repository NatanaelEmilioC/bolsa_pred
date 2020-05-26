import json
from datetime import datetime
import pandas as pd

def acao_taxa():

    taxa = pd.read_csv("C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\python-samples-master\\python-samples-master\\sheets\\quickstart\\Selic.csv", engine='python')  
    #rename taxa close
    taxa = taxa.replace(r'[<*%]', '', regex=True)
    taxa.rename(columns = {'*2013*':'2013', '*2014*':'2014', '*2015*':'2015', '*2016*':'2016', '*2017*':'2017',
                           '*2018*':'2018', '*2019*':'2019', '*2020*':'2020'}, inplace = True)
    
    taxa = taxa.drop(columns=['*Mês/Ano*'])
    
    bolsa = pd.read_csv("C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\python-samples-master\\python-samples-master\\sheets\\quickstart\\PETR4_8.csv") 
    datas = (bolsa[['Date']])
    datas = datas.values.tolist()

    datas_bolsa = [datetime.strptime(((x[0].split())[-2]).split(">")[-1] ,'%m/%d/%Y').date() for x in datas]

    bolsa.insert(6,'selic',-1)

    for data in datas_bolsa:
        data_formatada = data.strftime("%#m/%#d/%Y")
        
        taxa_selic = taxa.at[data.month-1, str(data.year)]
        
        if taxa_selic is None:
            taxa_selic = taxa.at[data.month-2, str(data.year)]
         
        bolsa['selic'][bolsa['Date'].str.contains(data_formatada)] = float((str(taxa_selic)).replace(',', '.'))
            
    bolsa.to_csv (r'C:\Users\natan\Desktop\PETR4_8_Selic.csv', index = False, header=True)
    #print(bolsa)


def acao_dolar():

    dolar = pd.read_csv("C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\python-samples-master\\python-samples-master\\sheets\\quickstart\\Dolar_8.csv")  
    bolsa = pd.read_csv("C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\python-samples-master\\python-samples-master\\sheets\\quickstart\\PETR4_8.csv") 
    #rename dolar close
    dolar_aux = dolar.set_axis(['Date', 'Dolar_Close'], axis=1, inplace=False)
    #slip date for comparing
    bolsa[['Date','Horas']]=bolsa['Date'].str.split(' ', expand=True,n=2)
    dolar_aux[['Date','Horas']]=dolar_aux['Date'].str.split(' ', expand=True,n=2)
    #join by date
    resultado = bolsa.join(dolar_aux.set_index('Date'), on='Date', lsuffix='_caller', rsuffix='_other')
    #drop duplicate columns
    resultado = resultado.drop(columns=['Horas_caller', 'Horas_other'])
    
    resultado.to_csv (r'C:\Users\natan\Desktop\PETR4_8_Dolar.csv', index = False, header=True)


def acao_noticia(arquivo):
    conteudo = open('C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\NLP\\' + arquivo).read()
    dados = json.loads(conteudo)   

    bolsa = pd.read_csv("C:\\Users\\natan\\Documents\\MEGA\\UFOP\\UFOP\\8º periodo\\CSI498 - TRABALHO DE CONCLUSAO DE CURSO I - Turma 11\\Desenvolvimento\\Projeto_teste\\python-samples-master\\python-samples-master\\sheets\\quickstart\\PETR4_8.csv") 
    datas = (bolsa[['Date']])
    datas = datas.values.tolist()

    datas_bolsa = [datetime.strptime(((x[0].split())[-2]).split(">")[-1] ,'%m/%d/%Y').date() for x in datas]
    # datas_bolsa[0].strftime('%Y-%m-%d')

    bolsa.insert(6,'sent_value',-1)

    for data in datas_bolsa:
        
        data_formatada = data.strftime("%#m/%#d/%Y")
        data_padrao = data.strftime('%Y-%m-%d')
        
        try: 
            sentimento = [((((x["sentimento"])[0]).get("keywords")[0]).get("sentiment")['score']) for x in dados if x['data'] == data_padrao]
            bolsa['sent_value'][bolsa['Date'].str.contains(data_formatada)] = sentimento
        except:
            bolsa['sent_value'][bolsa['Date'].str.contains(data_formatada)] = 0.0
            
    if arquivo == 'NLP_response_istoedinheiro.json':
        bolsa.to_csv (r'C:\Users\natan\Desktop\PETR4_8_IstoeDinheiro.csv', index = False, header=True)
    else:
        bolsa.to_csv (r'C:\Users\natan\Desktop\PETR4_8_Istoe.csv', index = False, header=True)

    

if __name__ == "__main__":
    #acao_noticia('NLP_response_istoedinheiro.json')
    acao_dolar()
    acao_taxa()