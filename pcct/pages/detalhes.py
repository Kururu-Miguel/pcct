import streamlit as sl

sl.title("Detalhes da Pesquisa")

# Os keys aí no menu servem de id
with sl.container(key="resumo"):
    sl.header("Resumo")
    sl.write("Conteúdo...")

with sl.container(key="metodologia"):
    sl.header("Metodologia")
    sl.write("Conteúdo...")

with sl.container(key="resultados"):
    sl.header("Resultados")
    sl.write("Conteúdo...")



secao = sl.query_params.get('secao')

if secao:
    sl.components.v1.html(f"""
        <script>
            const el = window.parent.document.getElementById("{secao}");
            if (el) {{
                el.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            }}
        </script>
    """, height=0)
    
    # Limpa o parâmetro para não rolar de novo a cada rerun
    sl.query_params.clear()

