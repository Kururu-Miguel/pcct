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

cursos = dados[campus]['curso'].unique()

curso = sl.selectbox('Curso', cursos)

cota = sl.selectbox('Cota/s', ('AC', 'PR', 'LB_PPI', 'LB_Q', 'LB_PCD', 'LB_EP', 'LI_PPI', 'LI_Q', 'LI_PCD', 'LI_EP'))

#cotas = sl.multiselect('Cota/s', ('AC', 'PR', 'LB_PPI', 'LB_Q', 'LB_PCD', 'LB_EP', 'LI_PPI', 'LI_Q', 'LI_PCD', 'LI_EP'))

#for c in range(len(cotas)):
#    cotas[c] = tabela_cotas[cotas[c]]
cota = tabela_cotas[cota]

#dados[campus][dados[campus]['curso'] == curso] #Não faço ideia de como essa filtragem funciona, nn sei usar indexação booleada, acabei de descobrir a existência disso

#dados_filtrados = dados[campus].query('curso == @curso and cota in @cotas') #ok, esse é fácil de entender

medias_lista = []
medias_passadas_lista = []
menores = []
maiores = []

for c in cursos:
    dados_filtrados = dados[campus].query('curso == @c and cota == @cota')
    nc = dados_filtrados['nota de corte']

    if pd.isna(nc.mean()): #verifica se o valor é um NaN
        media, media_passada, menor, maior = 6, 6, 6, 6
    else:
        media = nc.mean()
        media_passada = nc.iloc[:-1].mean()
        menor = nc.min()
        maior = nc.max()
    medias_lista.append(media)
    medias_passadas_lista.append(media_passada)
    menores.append(menor)
    maiores.append(maior)
    

valores = pd.DataFrame({
    'curso': cursos,
    'media': medias_lista,
    'media passada': medias_passadas_lista,
    'menor nota': menores,
    'maior nota': maiores
})

valores_curso = valores.query('curso == @curso')
media = valores_curso['media'][0]
media_passada = valores_curso['media passada'][0]
maior = valores_curso['maior nota'][0]
menor = valores_curso['menor nota'][0]

sl.metric(
    'Nota de corte média', 
    round(media, 2), 
    delta_description='Variação da nota em relação à média do ano passado', 
    delta=f'{round(((media - media_passada) / media_passada) * 100, 2)}'
)

sl.metric(
    'Amplitude',
    f'±{round(maior - menor, 2)}'
    )

sl.bar_chart(valores['media']) # dps eu arrumo isso aí

dados_filtrados
