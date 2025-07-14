import streamlit as st

st.set_page_config(layout="wide")
st.title("Assistente de Licitações 14.133")
st.caption("Alinhado aos Modelos da Advocacia-Geral da União (AGU) e Jurisprudência do TCU")

# ... (o dicionário de links continua o mesmo) ...
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

# ... (Os outros `if` para Compras, Serviços sem mão de obra, etc. continuam como antes) ...

if tipo_contrato == "Serviços (com dedicação exclusiva de mão de obra)":
    st.header("2. Checklist de Análise: Serviços com Mão de Obra Exclusiva")
    st.info("Módulo especialista para análise de planilha de custos e formação de preços.")

    with st.expander("✅ Verificações Gerais e Documentos Base"):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.checkbox("O Termo de Referência (TR) foi preenchido com as especificidades do serviço?", key="sc1")
        with col2:
            st.markdown(f'<a href="{links_agu["tr_servicos_unificado"]}" target="_blank">📄 TR Unificado</a>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.checkbox("A 'Lista de Verificação' específica da AGU para este modelo foi preenchida?", key="sc5")
        with col2:
            st.markdown(f'<a href="{links_agu["lista_verificacao_servicos_com_mao_obra"]}" target="_blank">📄 Lista AGU</a>', unsafe_allow_html=True)

    with st.expander("📊 Análise da Planilha de Custos e Formação de Preços"):
        st.subheader("Módulo 1: Composição da Remuneração")
        st.checkbox("Os salários base estão de acordo com a Convenção Coletiva de Trabalho (CCT) da categoria?", key="pc1")
        st.checkbox("Foram incluídos todos os adicionais aplicáveis (periculosidade, insalubridade, noturno)?", key="pc2")

        st.subheader("Módulo 2: Encargos Sociais e Trabalhistas")
        st.checkbox("O percentual do Submódulo 2.1 (INSS, FGTS, etc.) está correto e de acordo com a legislação vigente?", key="pc3")
        st.info("Dica TCU: Variações nos percentuais do 'Sistema S' ou 'RAT' devem ser justificadas.")
        st.checkbox("O Submódulo 2.2 (13º, Férias) considera corretamente as provisões para pagamentos futuros?", key="pc4")

        st.subheader("Módulo 3: Insumos (Uniformes, Equipamentos)")
        st.checkbox("Os custos com uniformes e equipamentos estão detalhados e são compatíveis com os preços de mercado?", key="pc5")
        st.checkbox("A vida útil dos materiais e a frequência de reposição foram especificadas e são razoáveis?", key="pc6")

        st.subheader("Módulo 4: Custos Indiretos, Tributos e Lucro (LDI/BDI)")
        st.checkbox("A taxa de Lucro é compatível com a média de mercado para serviços similares?", key="pc7")
        st.checkbox("Os impostos (PIS, COFINS, ISS) foram calculados sobre o faturamento e com as alíquotas corretas?", key="pc8")
        st.warning("Atenção: É vedado o repasse de IRPJ e CSLL nos custos, pois são impostos sobre o lucro. (Manual TCU)")

    st.text_area("Anotações da Unidade / Jurisprudência Local")
