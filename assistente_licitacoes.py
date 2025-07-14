import streamlit as st

# --- Configuração da Página ---
st.set_page_config(layout="wide")

# --- Título Principal ---
st.title("Assistente de Licitações 14.133")
st.caption("Alinhado aos Modelos da Advocacia-Geral da União (AGU)")

# --- Menu de Seleção do Tipo de Contratação ---
st.header("1. Selecione o Modelo da Contratação")

# Lista de opções baseada nos modelos da AGU
opcoes_modelos = [
    "Selecione uma opção...",
    "Compras",
    "Serviços (sem dedicação exclusiva de mão de obra)",
    "Serviços (com dedicação exclusiva de mão de obra)",
    "Obras e Serviços de Engenharia",
    "Bens e Serviços de TIC (Tecnologia da Informação e Comunicação)"
]

tipo_contrato = st.selectbox("Qual o tipo de objeto da sua contratação?", options=opcoes_modelos)

# --- Divisória Visual ---
st.markdown("---")

# --- Lógica para Carregar o Checklist Correto ---

if tipo_contrato == "Compras":
    st.header("2. Checklist de Análise: Compras")
    st.info("Verificação baseada nos modelos da AGU para aquisição de bens.")

    check_1 = st.checkbox("O Termo de Referência para Compras foi elaborado conforme o modelo da AGU?")
    check_2 = st.checkbox("A minuta do Contrato de Compras está de acordo com o padrão disponibilizado pela AGU?")
    check_3 = st.checkbox("A 'Lista de Verificação para Compras' da AGU foi utilizada como guia para a análise jurídica?")
    if not check_3:
        st.warning("A Lista de Verificação da AGU é um instrumento chave para garantir que todos os pontos críticos foram observados antes de enviar para análise jurídica.")

elif tipo_contrato == "Serviços (sem dedicação exclusiva de mão de obra)":
    st.header("2. Checklist de Análise: Serviços sem Mão de Obra Exclusiva")
    st.info("Verificação baseada nos modelos da AGU para serviços gerais.")

    check_1 = st.checkbox("O Termo de Referência utilizou como base o modelo unificado para serviços da AGU?")
    check_2 = st.checkbox("A minuta do Contrato para Serviços sem Mão de Obra Exclusiva está de acordo com o padrão?")
    check_3 = st.checkbox("A 'Lista de Verificação para Serviços sem Mão de Obra' da AGU foi utilizada como guia?")

elif tipo_contrato == "Serviços (com dedicação exclusiva de mão de obra)":
    st.header("2. Checklist de Análise: Serviços com Mão de Obra Exclusiva")
    st.info("Verificação para o modelo complexo de serviços com dedicação de mão de obra (terceirização).")

    check_1 = st.checkbox("O Termo de Referência e seus anexos (planilhas de custos e formação de preços) estão detalhados?")
    check_2 = st.checkbox("Foi verificado se a Convenção Coletiva de Trabalho (CCT) aplicável foi considerada na planilha de custos?")
    st.warning("A análise da CCT correta é fundamental para evitar passivos trabalhistas e jogos de planilha.")
    check_3 = st.checkbox("A minuta do Contrato para Serviços com Mão de Obra Exclusiva está de acordo com o padrão da AGU?")
    check_4 = st.checkbox("A 'Lista de Verificação para Serviços com Mão de Obra Exclusiva' da AGU foi preenchida?")

elif tipo_contrato == "Obras e Serviços de Engenharia":
    st.header("2. Checklist de Análise: Obras e Serviços de Engenharia")
    st.info("Verificação com base nos modelos e particularidades para contratações de engenharia.")

    check_1 = st.checkbox("O Projeto Básico ou Executivo foi anexado e contém os elementos do Art. 6º, XXV?")
    check_2 = st.checkbox("O orçamento detalhado se baseia no SINAPI/SICRO, conforme exigência legal?")
    check_3 = st.checkbox("A 'Lista de Verificação para Obras e Serviços de Engenharia' da AGU foi utilizada?")
    check_4 = st.checkbox("Se aplicável, o 'Termo de Justificativas Técnicas Relevantes' foi elaborado?")
    check_5 = st.checkbox("Está prevista a exigência da Anotação de Responsabilidade Técnica (ART) ou RRT do projeto e da execução?")

elif tipo_contrato == "Bens e Serviços de TIC":
    st.header("2. Checklist de Análise: Bens e Serviços de TIC")
    st.info("Checklist para contratações de TI, que seguem rito próprio (IN Seges/ME nº 94/2022 e modelos AGU).")

    check_1 = st.checkbox("O Estudo Técnico Preliminar (ETP Digital) e o Mapa de Riscos foram elaborados?")
    check_2 = st.checkbox("O Termo de Referência está alinhado com o ETP e o modelo de contratação de solução de TIC?")
    st.warning("Em TIC, o ETP é a peça mais importante do planejamento. O TR deve ser um reflexo dele.")
    check_3 = st.checkbox("Os critérios de medição e os Acordos de Nível de Serviço (ANS/SLA) estão claros e objetivos?")
    check_4 = st.checkbox("A minuta de contrato segue o modelo específico para Soluções de TIC da AGU?")
