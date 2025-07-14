import streamlit as st

# Título e descrição do nosso aplicativo
st.title("Assistente de Licitações 14.133")
st.header("Módulo 1: Análise Preliminar (Fase Preparatória)")
st.subheader("Checklist de Conformidade do Termo de Referência (TR)")

st.write("Marque os itens abaixo para verificar a conformidade do Termo de Referência.")

# --- Checklist Interativo ---

st.markdown("---")
st.markdown("#### **1. Planejamento e Objeto**")

# Item 1.1
check_objeto = st.checkbox("1.1 - A definição do objeto é precisa, suficiente e clara? (Art. 6, XXIII)")
if not check_objeto:
    st.warning("**Ação Sugerida:** Descreva o objeto da contratação sem características excessivas ou irrelevantes que possam limitar a competição.")

# Item 1.2
check_justificativa = st.checkbox("1.2 - A justificativa para a contratação está fundamentada e clara? (Art. 40, § 1º)")
if not check_justificativa:
    st.error("**Ponto Crítico:** A ausência de justificativa pode anular o processo. Descreva a necessidade da contratação, os resultados esperados e a relação com o planejamento do órgão.")

st.markdown("---")
st.markdown("#### **2. Requisitos da Contratação**")

# Item 2.1
check_requisitos = st.checkbox("2.1 - Os requisitos da contratação estão definidos? (Ex: especificações técnicas, prazos, garantia)")
if not check_requisitos:
    st.warning("**Ação Sugerida:** Detalhe todos os requisitos necessários para que a solução atenda à necessidade, incluindo critérios de qualidade e desempenho.")

# Item 2.2
check_vedacoes = st.checkbox("2.2 - O TR está livre de vedações? (Ex: marcas, especificações exclusivas, salvo exceções legais)")
if not check_vedacoes:
    st.error("**Ponto Crítico:** A indicação de marca é vedada. Se for indispensável, deve ser formalmente justificada. Verifique o Art. 41.")

st.markdown("---")
st.markdown("#### **3. Estimativa de Preço**")

# Item 3.1
check_pesquisa_preco = st.checkbox("3.1 - A estimativa de preço foi realizada com base em uma ampla pesquisa de mercado? (Art. 23)")
if not check_pesquisa_preco:
    st.warning("**Ação Sugerida:** Anexe ao processo a pesquisa de preços detalhada. A lei exige uma pesquisa ampla, usando parâmetros como contratações similares, notas fiscais, etc.")


# --- Botão de Relatório Final ---
st.markdown("---")
if st.button("Gerar Relatório de Conformidade"):
    pendencias = []
    if not check_objeto:
        pendencias.append("1.1 - Definição do objeto")
    if not check_justificativa:
        pendencias.append("1.2 - Justificativa da contratação")
    if not check_requisitos:
        pendencias.append("2.1 - Definição dos requisitos")
    if not check_vedacoes:
        pendencias.append("2.2 - Verificação de vedações")
    if not check_pesquisa_preco:
        pendencias.append("3.1 - Estimativa de preço")

    if not pendencias:
        st.success("🎉 **Análise Concluída!** O Termo de Referência parece estar em conformidade com os pontos verificados.")
    else:
        st.error(f"**Atenção! Foram encontradas {len(pendencias)} pendências:**")
        for pendencia in pendencias:
            st.write(f"- {pendencia}")
        st.info("Corrija os pontos acima para prosseguir com segurança.")
