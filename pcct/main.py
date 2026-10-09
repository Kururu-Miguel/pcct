import streamlit as sl


pg = sl.navigation([
    sl.Page('pages/home.py', title = 'Página Principal'),
    sl.Page('pages/informacoes.py', title = 'Informações Da Pesquisa')
])

pg.run()

