import streamlit as sl


pg = sl.navigation([
    sl.Page('pages/home.py', title = 'Página Principal', icon = ':material/home:'),
    sl.Page('pages/detalhes.py', title = 'Detalhes Da Pesquisa', icon = ':material/description:')
], position = 'top')
pg.run()
