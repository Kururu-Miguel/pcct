import streamlit as sl
from pathlib import Path
import pandas as pd


caminho_dados = Path(__file__).parent.parent.parent.resolve() / 'dados' #Pega o caminho absoluto da pasta dos dados


@sl.cache_data
def carregar_dados():
    dados_manaus = pd.read_excel(caminho_dados / 'dados_manaus.xlsx', sheet_name=None) # o sheet_none serve pra ler todas as páginas do arquivo, sem o parâmetro ia ler só o 0, seria o primeiro campus.
    dados_maues = pd.read_excel(caminho_dados / 'dados_maues.xlsx')

    dados = dados_manaus.copy()
    dados['MAUES'] = dados_maues.copy()

    for k in dados.keys():
        dados[k].columns = dados[k].columns.str.lower()

    tabela_cotas = pd.read_excel(caminho_dados / 'tabela_cotas.xlsx').set_index('Nova')['Antiga'].to_dict()

    dados_validacao = pd.read_excel(caminho_dados / 'validacao.xlsx')

    return dados, tabela_cotas, dados_validacao
