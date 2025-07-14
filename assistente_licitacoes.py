import streamlit as st

# --- Configuração da Página ---
st.set_page_config(layout="wide")

# --- Título Principal ---
st.title("Assistente de Licitações 14.133")
st.caption("Alinhado aos Modelos da Advocacia-Geral da União (AGU)")

# --- DICIONÁRIO DE LINKS (Extraídos do site da AGU) ---
# Manter os links aqui facilita a atualização futura.
links_agu = {
    "tr_compras": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-referencia-compras-lei-no-14-133-abr-25.docx",
    "contrato_compras": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-contrato-compras-lei-no-14-133-abr-25.docx",
    "lista_verificacao_compras_servicos_sem_mao_obra": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/listas-de-verificacao/modelo-de-lista-de-verificacao-compras-e-servicos-sem-mao-de-obra-exclusiva-lei-no-14-133-set-24.docx",
    "tr_servicos_unificado": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-referencia-servicos-e-obras-lei-no-14-133-abr-25.docx",
    "contrato_servicos_sem_mao_obra": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-contrato-servico-sem-mao-de-obra-exclusiva-lei-no-14-133-abr-25.docx",
    "contrato_servicos_com_mao_obra": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-contrato-servico-com-mao-de-obra-exclusiva-lei-no-14-133-abr-25.docx",
    "lista_verificacao_servicos_com_mao_obra": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/listas-de-verificacao/modelo-de-lista-de-verificacao-servicos-com-mao-de-obra-exclusiva-lei-no-14-133-set-24.docx",
    "contrato_engenharia": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/pregao-e-concorrencia/modelo-de-termo-de-contrato-obras-e-servicos-de-engenharia-lei-no-14-133-abr-25-1.docx",
    "lista_verificacao_engenharia": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/14133/listas-de-verificacao/modelo-de-lista-de-verificacao-obras-e-servicos-de-engenharia-lei-no-14-133-set-24.docx",
    "termo_justificativas_engenharia": "https://www.gov.br/agu/pt-br/composicao/cgu/cgu/modelos/licitacoesecontratos/termo-de-justificativas-tecnicas-relevantes-obras-e-servicos-engenharia-lei-14-133.docx"
}


# --- Menu de Seleção ---
st.header("1. Selecione o Modelo da Contratação")
opcoes_modelos = [
    "Selecione uma opção...", "Compras", "Serviços (sem dedicação exclusiva de mão de obra)",
    "Serviços (com dedicação exclusiva de mão de obra)", "Obras e Serviços de Engenharia",
    "Bens e Serviços de TIC (Tecnologia da Informação e Comunicação)"
]
tipo_contrato = st.selectbox("Qual o tipo de objeto da sua contratação?", options=opcoes_modelos, label_visibility="collapsed")
st.markdown("---")

# --- Lógica para Carregar o Checklist Correto ---

if tipo_contrato == "Compras":
    st.header("2. Checklist de Análise: Compras")
    st.info("Verificação baseada nos modelos da AGU para aquisição de bens.")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("O Termo de Referência para Compras foi elaborado conforme o modelo da AGU?", key="c1")
    with col2:
        st.markdown(f'<a href="{links_agu["tr_compras"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A minuta do Contrato de Compras está de acordo com o padrão disponibilizado pela AGU?", key="c2")
    with col2:
        st.markdown(f'<a href="{links_agu["contrato_compras"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A 'Lista de Verificação para Compras' da AGU foi utilizada como guia para a análise?", key="c3")
    with col2:
        st.markdown(f'<a href="{links_agu["lista_verificacao_compras_servicos_sem_mao_obra"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)


elif tipo_contrato == "Serviços (sem dedicação exclusiva de mão de obra)":
    st.header("2. Checklist de Análise: Serviços sem Mão de Obra Exclusiva")
    st.info("Verificação baseada nos modelos da AGU para serviços gerais.")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("O Termo de Referência utilizou como base o modelo unificado para serviços da AGU?", key="s1")
    with col2:
        st.markdown(f'<a href="{links_agu["tr_servicos_unificado"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A minuta do Contrato para Serviços sem Mão de Obra Exclusiva está de acordo com o padrão?", key="s2")
    with col2:
        st.markdown(f'<a href="{links_agu["contrato_servicos_sem_mao_obra"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A 'Lista de Verificação para Serviços sem Mão de Obra' da AGU foi utilizada como guia?", key="s3")
    with col2:
        st.markdown(f'<a href="{links_agu["lista_verificacao_compras_servicos_sem_mao_obra"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)


elif tipo_contrato == "Serviços (com dedicação exclusiva de mão de obra)":
    st.header("2. Checklist de Análise: Serviços com Mão de Obra Exclusiva")
    st.info("Verificação para o modelo complexo de serviços com dedicação de mão de obra (terceirização).")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("O Termo de Referência (modelo unificado) foi preenchido com as especificidades do serviço?", key="sc1")
    with col2:
        st.markdown(f'<a href="{links_agu["tr_servicos_unificado"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)
    
    st.checkbox("As planilhas de custos e formação de preços estão detalhadas e anexadas ao TR?", key="sc2")
    st.checkbox("Foi verificado se a Convenção Coletiva de Trabalho (CCT) aplicável foi considerada na planilha de custos?", key="sc3")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A minuta do Contrato para Serviços com Mão de Obra Exclusiva está de acordo com o padrão da AGU?", key="sc4")
    with col2:
        st.markdown(f'<a href="{links_agu["contrato_servicos_com_mao_obra"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A 'Lista de Verificação para Serviços com Mão de Obra Exclusiva' da AGU foi preenchida?", key="sc5")
    with col2:
        st.markdown(f'<a href="{links_agu["lista_verificacao_servicos_com_mao_obra"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)


elif tipo_contrato == "Obras e Serviços de Engenharia":
    st.header("2. Checklist de Análise: Obras e Serviços de Engenharia")
    st.info("Verificação com base nos modelos e particularidades para contratações de engenharia.")

    st.checkbox("O Projeto Básico ou Executivo foi anexado e contém os elementos do Art. 6º, XXV?", key="e1")
    st.checkbox("O orçamento detalhado se baseia no SINAPI/SICRO, conforme exigência legal?", key="e2")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A 'Lista de Verificação para Obras e Serviços de Engenharia' da AGU foi utilizada?", key="e3")
    with col2:
        st.markdown(f'<a href="{links_agu["lista_verificacao_engenharia"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("Se aplicável, o 'Termo de Justificativas Técnicas Relevantes' foi elaborado?", key="e4")
    with col2:
        st.markdown(f'<a href="{links_agu["termo_justificativas_engenharia"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.checkbox("A minuta de Contrato de Engenharia está de acordo com o padrão da AGU?", key="e5")
    with col2:
        st.markdown(f'<a href="{links_agu["contrato_engenharia"]}" target="_blank">📄 Abrir Modelo</a>', unsafe_allow_html=True)


elif tipo_contrato == "Bens e Serviços de TIC":
    st.header("2. Checklist de Análise: Bens e Serviços de TIC")
    st.info("Checklist para contratações de TI, que seguem rito próprio e modelos específicos (não listados na página principal).")

    st.checkbox("O Estudo Técnico Preliminar (ETP Digital) e o Mapa de Riscos foram elaborados?", key="t1")
    st.checkbox("O Termo de Referência está alinhado com o ETP e o modelo de contratação de solução de TIC?", key="t2")
    st.checkbox("Os critérios de medição e os Acordos de Nível de Serviço (ANS/SLA) estão claros e objetivos?", key="t3")
    st.checkbox("A minuta de contrato segue o modelo específico para Soluções de TIC da AGU?", key="t4")
