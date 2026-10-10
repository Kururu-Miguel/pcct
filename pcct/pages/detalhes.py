import streamlit as sl
from utils.dados import carregar_dados
import altair as alt


dados, dados_validacao = carregar_dados()[0], carregar_dados()[-1]
campus = 'MAUES'
campus_exib = 'Maués'
curso = 'Informática'
cota = 'AC'


sl.caption('Esse dashboard utiliza dados adiquiridos através de uma pesquisa, também feita por mim, para funcionar. Abaixo estão detalhes sobre a mesma, incluindo origem dos dados e o processo feito em sua análise.')



sl.title('Detalhes da Pesquisa')



sl.header('Resumo')
sl.markdown('A análise propõe um olhar para  a preditibilidade de aprovação nos processos seletivos dos cursos integrados dos campi CMA, CMZL, CMC e CMDI do IFAM entre os anos de 2016 até 2025, quando este passou a adotar o sistema de seleção por análise curricular, no lugar de um exame intelectual de múltipla escolha, utilizando como objeto de pesquisa os editais de candidatos aprovados fornecidos pelo próprio site da instituição. É possível inferir um valor de média a ser alcançada para aprovação a partir das notas de corte obtidas no próprio edital de aprovados', text_alignment = 'justify')



sl.header('Contexto')
sl.markdown('''No ano de 2016 ocorreu pela última vez o processo seletivo do IFAM via exame intelectual (IFAM, 2015) à partir de 2017 todos os processos seletivos de admissão ao IFAM foram realizados via análise curricular que consiste em avaliar o desempenho acadêmico do aluno de acordo com o histórico escolar apresentado por ele, no caso dos cursos integrados, das disciplinas de: língua portuguesa, matemática e ciências, nos anos de 7ª (sétima) e 8ª (oitava) série do ensino fundamental.

> [...] A seleção será realizada em 02 (duas) Fases:
a) Primeira Fase: o(a) candidato(a) deverá realizar sua inscrição via internet, no site www.ifam.edu.br, no banner do Processo Seletivo para o Ensino Médio Integrado 2017, no período entre 3 e 18 de novembro de 2016.
b) Segunda Fase (Classificatória): a classificação do(a)s candidato(a)s será realizada com base na Nota Final (NF) conforme fórmula no subitem 6.1, sendo resultante de cálculo a ser realizado com base nas Médias Finais (MF) das disciplinas de Língua Portuguesa, Matemática e Ciências do oitavo ano do ensino fundamental, as quais deverão ser informadas pelo(a) candidato(a) no ato da inscrição e comprovadas no ato da matrícula, por meio da apresentação do Histórico Escolar (IFAM, 2016, p. 1).''', text_alignment = 'justify')



sl.header('Metodologia')
sl.markdown('Foram lidos os editais de cada processo seletivo desde 2016 até 2025 para coleta de informações relacionadas às mudanças de método de ingresso aos campi e nomenclatura de cotas. Para cada processo seletivo também foi feita uma análise das chamadas disponíveis. Nessas chamadas eram coletadas as notas do último colocado de cada cota, curso e campi, estas eram adicionadas em uma tabela no excel. Após juntar todas essas informações e organizá-las na tabela era feito um cálculo para inferir a nota de média de corte para cada curso em determinada cota e campi.', text_alignment = 'justify')



dados_exib = dados[campus].query('curso == @curso and cota == @cota')
sl.dataframe(dados_exib.drop(columns = ['observação']), use_container_width = True, hide_index = True)
notas = dados_exib['nota de corte']
bleh = ' + '.join(notas.astype(str))
media = round(sum(notas)/len(notas), 2)
maior = round(max(notas), 2)
menor = round(min(notas), 2)
amplitude = round(maior - menor, 2)
maxima = round(media + amplitude, 2) if (media + amplitude) <= 10 else 10
minima = round(media - amplitude, 2)


sl.markdown(rf'''Tomando como exemplo a cota {cota} do curso de {curso} do Campus {campus_exib}, foram coletadas as notas e organizadas de acordo com o modelo mostrado na tabela acima, foi então feita uma média aritmética para se adquirir a nota de corte média dentre os anos, esta sendo a nota de corte provável para o processo seletivo seguinte
> $\ Média = \frac{{{bleh}}}{{{len(notas)}}} = {media}$''', text_alignment = 'justify')



sl.markdown(f'''Entretanto, a previsão para a nota, assim como tudo no campo atuarial, tem uma margem de erro, esta é chamada de amplitude e é igual a diferença entre o maior e o menor valor de amostra. No caso desta tabela a amplitude tem valor igual a {amplitude}, significando que a nota de corte do próximo processo seletivo provavelmente será de {media} podendo variar {amplitude} para cima ou para baixo. Isto torna o valor máximo igual a {maxima} e o mínimo igual a {minima}. Qualquer nota de corte fora desta margem caracteriza previsão errônea.
> $\ Amplitude = {maior} - {menor} = {amplitude}$''', text_alignment = 'justify')



sl.header('Validação Dos Dados Coletados')
sl.markdown('Após a compilação dos dados necessários foi efetuada a averiguação da precisão das projeções feitas. Foram utilizados neste estudo 43 estudantes matriculados no 9º ano de Ensino Fundamental de 2024 na Escola Estadual Professor Demóstenes Belduque de Araújo Travessa, localizada no Bairro Jorge Teixeira em Manaus, estes foram estudantes do orientador da pesquisa no ano de 2023. Estes estudantes forneceram suas médias de nota do 7º (sétimo) e 8º (oitavo) nas matérias de português, matemática e ciências conforme é requerido no edital. Eles forneceram também as informações necessárias para a inscrição, como dados pessoais e curso desejado. Com esse material em mãos foi verificado quais cotas os alunos eram elegíveis e se eles tinham chances de passar com suas notas, caso fosse acreditado ser inviável, eles eram orientados a se inscreverem em um curso com maior chance de ingresso.', text_alignment = 'justify')

sl.dataframe(dados_validacao.drop(columns = ['Seguiu a Previsão?']), hide_index = True)

sl.markdown('Conforme mostra a tabela acima, as projeções alcançaram uma precisão satisfatória.', text_alignment = 'justify')

contagem = dados_validacao['Previsão'].value_counts().reset_index()


total = contagem['count'].sum()

# Pega cada categoria (com fallback de 0 se não existir)
acertos = contagem.loc[contagem['Previsão'] == 'Acertou', 'count'].sum()
margem = contagem.loc[contagem['Previsão'] == 'Acertou na Margem', 'count'].sum()
erros = contagem.loc[contagem['Previsão'] == 'Errou', 'count'].sum()


sl.header('Eficácia do método')

col1, col2, col3 = sl.columns(3)

with col1:
    sl.metric(
        'Acertou',
        f'{acertos}',
        f'{acertos/total*100:.2f}%',
        delta_arrow = 'off'
    )

with col2:
    sl.metric(
        'Acertou na margem',
        f'{margem}',
        f'{margem/total*100:.2f}%',
        delta_arrow = 'off'
    )

with col3:
    sl.metric(
        'Errou',
        f'{erros}',
        f'{erros/total*100:.2f}%',
        delta_color = 'inverse',
        delta_arrow = 'off'
    )


sl.caption('Gráfico de barras horizontal')
grafico_barras = alt.Chart(contagem).mark_bar().encode(
    y=alt.Y('Previsão:N', sort='-x', title=''),
    x=alt.X('count:Q', title='Nº de alunos'),
    color=alt.Color(
        'Previsão:N',
        scale=alt.Scale(
            domain=['Acertou', 'Acertou na Margem', 'Errou'],
            range=['blue', 'orange', 'red']
        ),
        legend=None
    ),
    tooltip = [
        alt.Tooltip('Previsão:N', title = 'Resultado'),
        alt.Tooltip('count:Q', title = 'Alunos')
    ]
)

grafico_barras

pizza = alt.Chart(contagem).mark_arc(
    innerRadius=75,         
    outerRadius=150,
).encode(
    theta=alt.Theta('count:Q', title='Nº de alunos'),
    color=alt.Color(
        'Previsão:N',
        scale=alt.Scale(
            domain=['Acertou', 'Acertou na Margem', 'Errou'],
            range=['blue', 'orange', 'red']   # verde / amarelo / vermelho
        ),
        legend=alt.Legend(title='Previsão', orient='bottom')
    ),
    tooltip=[
        alt.Tooltip('Previsão:N', title='Resultado'),
        alt.Tooltip('count:Q', title='Alunos'),
    ]
).properties(
    height=500
)


total = contagem['count'].sum()
contagem['Percentual'] = (contagem['count'] / total * 100).round(2).astype(str) + '%'


texto = alt.Chart(contagem).mark_text(
    radius=110,
    fontSize=14,
    fontWeight='bold',
    color='white'
).encode(
    theta=alt.Theta('count:Q'),
    text=alt.Text('Percentual:N')
)

sl.caption('Gráfico de Donnut')
sl.altair_chart(pizza + texto, use_container_width=True)

sl.caption('''---
[![Dev](https://img.shields.io/badge/Dev-Kururu--Miguel-blue?logo=github)](https://github.com/Kururu-Miguel)'''
)
