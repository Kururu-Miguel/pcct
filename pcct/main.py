import streamlit as sl


# css que faz os links de âncora parecerem page_links
sl.markdown("""
<style>
    /* Container dos sublinks */
    .anchor-nav {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    /* links de âncora */
    .anchor-nav a {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px 8px 46px;
        border-radius: 8px;
        font-size: 14px;
        color: inherit;
        text-decoration: none;
        transition: background-color 0.15s;
        opacity: 0.85;
    }

    /* é pra quando clicar na âncora */
    .anchor-nav a:hover {
        background-color: rgba(128, 128, 128, 0.15);
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)


paginas = {
    '': [
        sl.Page('pages/home.py', url_path = 'home')
    ],
    'Detalhes Da Pesquisa': [
        sl.Page('pages/detalhes.py', url_path = 'detalhes')
    ]
}


# é importante colocaar isso aqui como hidden, pq eu quero usar a navegação do método, não as parada de estilização
pg = sl.navigation(paginas, position = 'hidden')


with sl.sidebar:
    sl.page_link('pages/home.py', label = 'Página Principal', icon = ':material/home:')
    sl.page_link('pages/detalhes.py', label = 'Detalhes Da Pesquisa', icon = ':material/description:')
    sl.page_link('pages/detalhes.py', label = 'Resumo', query_params = {'secao': 'resumo'})




pg.run()
