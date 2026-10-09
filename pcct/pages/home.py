from pathlib import Path
import streamlit as sl
import pandas as pd
import altair as alt


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
    dados_filtrados = dados[campus].query('curso == @c and cota == @cota').copy()
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
    'maior nota': maiores,
})


valores_curso = valores.query('curso == @curso')
media = valores_curso['media'].iloc[0]
media_passada = valores_curso['media passada'].iloc[0]
maior = valores_curso['maior nota'].iloc[0]
menor = valores_curso['menor nota'].iloc[0]
maior_universal = valores['maior nota'].max()
menor_universal = valores['menor nota'].min()


dados_tempo = dados[campus].query('cota == @cota').copy()
dados_tempo['nota de corte'] = pd.to_numeric(dados_tempo['nota de corte'], errors='coerce')
dados_tempo = dados_tempo.dropna(subset=['nota de corte', 'ano'])
dados_tempo['ano'] = dados_tempo['ano'].str.split('-').str[1]


sl.subheader('Informações sobre o curso selecionado')

col1, col2 = sl.columns(2)

with col1:
    sl.metric(
        'Nota de corte média', 
        round(media, 2), 
        help = 'Nota de corte é a nota mínima para se passar no processo seletivo. Abaixo da nota, destacada, está a variação entre a média atual e a média do ano passado.',
        delta=f'{round(((media - media_passada) / media_passada) * 100, 2)}%'
    )

with col2:
    sl.metric(
        'Amplitude',
        value=f'±{round(maior - menor, 2)}',
        help='Amplitude é a diferença entre a maior e menor nota, representa o quanto a nota de corte do ano atual pode variar tanto para cima quanto para baixo'
    )


graf_barras_vertical = alt.Chart(valores).mark_bar(clip=True).encode(
    x = alt.X(
        'curso:N',
        sort = '-y',
        axis = alt.Axis(
            labelAngle = 0,
            title = 'Curso'
        )
    ),

    y = alt.Y(
        'media:Q',
        title = 'Nota de corte média',
    )
)


graf_barras_horizontal = alt.Chart(valores).mark_bar(clip=True).encode(
    y = alt.Y(
        'curso:N',
        sort = '-x',
        axis = alt.Axis(
            labelAngle = 0,
            title = 'Curso'
        )
    ),

    x = alt.X(
        'media:Q',
        title = 'Nota de corte média',
        scale = alt.Scale(domain=[menor_universal*0.90, maior_universal*1.05])
    )
)

graf_retas = alt.Chart(dados_tempo).mark_line(point=True).encode(
    x = alt.X(
        'ano:O',
        title = 'Ano',
        axis = alt.Axis(labelAngle=0)
    ),

    y = alt.Y(
        'nota de corte:Q',
        title = 'Notas de corte',
        scale = alt.Scale(domain=[menor_universal*0.90, maior_universal*1.05])
    ),

    color=alt.Color(
        'curso:N',
        title='Curso',
        legend=alt.Legend(orient='bottom', columns=3)
    ),
)




sl.caption('Clique no container abaixo para ver dados mais detalhados sobre o estudo das notas de corte')
with sl.expander('Estatísticas para nerds'):
    dados_exibi = dados[campus].query('curso == @curso and cota == @cota')
    sl.subheader('Notas de corte por ano')
    sl.dataframe(
        dados_exibi.drop(columns=['observação']),
        use_container_width = True,
        hide_index=True
    )
    sl.subheader('Notas de corte dos diferentes cursos da cota e campus selecionado')
    sl.caption('Gráfico vertical geral das médias das notas de corte da cota e campus selecionado')
    graf_barras_vertical
    sl.caption('Gráfico horizontal feito a partir dos mesmos dados, ampliado para melhor vizualiação das diferenças')
    graf_barras_horizontal
    sl.caption('Gráfico de linhas mostrando as médias das notas de corte ao decorrer dos anos')
    graf_retas

