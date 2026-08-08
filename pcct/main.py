from pathlib import Path
import streamlit as sl
import pandas as pd


caminho_dados = Path(__file__).parent.parent.resolve() / 'dados' #Pega o caminho absoluto da pasta dos dados


@sl.cache_data
def carregar_dados():
    dados_manaus = pd.read_excel(caminho_dados / 'dados_manaus.xlsx', sheet_name=None) # o sheet_none serve pra ler todas as páginas do arquivo, sem o parâmetro ia ler só o 0, seria o primeiro campus.
    dados_maues = pd.read_excel(caminho_dados / 'dados_maues.xlsx')

    dados = dados_manaus.copy()
    dados['MAUES'] = dados_maues.copy()

    for k in dados.keys():
        dados[k].columns = dados[k].columns.str.lower()

    tabela_cotas = pd.read_excel(caminho_dados / 'tabela_cotas.xlsx').set_index('Nova')['Antiga'].to_dict()

    return dados, tabela_cotas


dados, tabela_cotas = carregar_dados()

sl.title('Notas de corte dos processos seletivos do IFAM')

campus = sl.selectbox('Campus', dados.keys())

curso = sl.selectbox('Curso', dados[campus]['curso'].unique())

cotas = sl.multiselect('Cota/s', ('AC', 'PR', 'LB_PPI', 'LB_Q', 'LB_PCD', 'LB_EP', 'LI_PPI', 'LI_Q', 'LI_PCD', 'LI_EP'))

for c in range(len(cotas)):
    cotas[c] = tabela_cotas[cotas[c]]

#dados[campus][dados[campus]['curso'] == curso] #Não faço ideia de como essa filtragem funciona, nn sei usar indexação booleada, acabei de descobrir a existência disso

dados_filtrados = dados[campus].query('curso == @curso and cota in @cotas') #ok, esse é fácil de entender
dados_filtrados
