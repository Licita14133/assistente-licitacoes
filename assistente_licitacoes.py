import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 6.2 - Construtor Fiel ao Modelo")
st.caption("Construção guiada e detalhada do Termo de Referência, incluindo a tabela de itens.")

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []
if 'tr_inputs' not in st.session_state:
    st.session_state.tr_inputs = {}

# --- Aba Única para Foco Total na Construção do TR ---
st.header("Construtor Guiado do Termo de Referência (Modelo: Compras)")
st.info("Siga os tópicos abaixo. A seção do Objeto agora permite a construção detalhada da tabela de itens.")

# --- Tópico 1: Construtor da Tabela de Itens ---
st.markdown("---")
st.subheader("Tópico 1: DO OBJETO (Detalhamento dos Itens)")
st.info("Use os campos abaixo para adicionar cada item da sua compra na tabela. A tabela será atualizada a cada adição.")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col1:
        item_desc = st.text_input("Descrição Detalhada do Item", placeholder="Ex: Caneta esferográfica, ponta média, cor azul")
    with col2:
        item_unid = st.selectbox("Unidade", ["UN", "CX", "PCT", "RES", "KG", "L", "M"])
    with col3:
        item_qtd = st.number_input("Quantidade", min_value=1, step=1)
    with col4:
        item_valor_unit = st.number_input("Valor Unitário (R$)", min_value=0.01, step=0.01, format="%.2f")

    if st.button("Adicionar Item à Tabela", type="primary"):
        if item_desc: # Adiciona apenas se a descrição não estiver vazia
            novo_item = {
                "Item": len(st.session_state.tr_itens) + 1,
                "Descrição": item_desc,
                "Unidade": item_unid,
                "Quantidade": item_qtd,
                "Valor Unitário (R$)": item_valor_unit,
                "Valor Total (R$)": item_qtd * item_valor_unit
            }
            st.session_state.tr_itens.append(novo_item)
        else:
            st.warning("Por favor, preencha a descrição do item.")

# --- Exibição da Tabela de Itens Construída ---
if st.session_state.tr_itens:
    st.markdown("##### Tabela de Itens da Contratação:")
    df_itens = pd.DataFrame(st.session_state.tr_itens)
    st.dataframe(df_itens, use_container_width=True, hide_index=True)
    
    # AQUI ESTÁ A CORREÇÃO: Removido o "_" extra no final da string.
    valor_total_contratacao = df_itens["Valor Total (R$)"].sum()
    
    st.success(f"**Valor Total Estimado da Contratação: R$ {valor_total_contratacao:,.2f}**")
    st.session_state.tr_inputs['valor_total_calculado'] = f"R$ {valor_total_contratacao:,.2f}"

# --- Demais Tópicos do Termo de Referência ---
with st.form("tr_demais_topicos_form"):
    st.markdown("---")
    st.subheader("Demais Tópicos do Termo de Referência")

    st.markdown("#### Tópico 2: DA FUNDAMENTAÇÃO E JUSTIFICATIVA DA CONTRATAÇÃO")
    st.session_state.tr_inputs['justificativa'] = st.text_area("2.1. Descreva a justificativa para a aquisição.", height=150, key=2.1)
    
    # Aqui entrariam os outros tópicos do 3 ao 14, conforme implementarmos...

    submitted = st.form_submit_button("Gerar Documento Completo do Termo de Referência")

if submitted:
    st.balloons()
    st.header("Documento Final Gerado")
    
    doc = []
    doc.append("TERMO DE REFERÊNCIA (COMPRAS)")
    doc.append("="*60)
    
    doc.append("\n1. DO OBJETO")
    doc.append("1.1. O presente Termo de Referência tem por objeto a aquisição dos bens detalhados na tabela abaixo:")
    if st.session_state.tr_itens:
        df_para_doc = pd.DataFrame(st.session_state.tr_itens)
        doc.append(df_para_doc.to_string(index=False))
        doc.append(f"\nVALOR TOTAL ESTIMADO: {st.session_state.tr_inputs.get('valor_total_calculado', 'R$ 0,00')}")
    else:
        doc.append("[NENHUM ITEM ADICIONADO À TABELA]")

    doc.append("\n\n2. DA FUNDAMENTAÇÃO E JUSTIFICATIVA")
    doc.append(f"2.1. {st.session_state.tr_inputs.get('justificativa', '[NÃO PREENCHIDO]')}")
    
    documento_final_str = "\n".join(doc)

    st.text_area("Prévia do Documento Completo", documento_final_str, height=400)
    st.download_button("📥 Baixar TR Completo (.txt)", documento_final_str, f"TR_COMPRAS_{datetime.now().strftime('%Y%m%d')}.txt")
