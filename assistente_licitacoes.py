import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 7.1 - Integração Simplificada")
st.caption("Construção de TR com busca inteligente e padronização de itens.")

# --- Carregamento e Cache dos Catálogos com NOMES SIMPLIFICADOS ---
@st.cache_data
def load_data():
    try:
        # O código agora procura pelos nomes simples: "catmat.csv" e "catser.csv"
        catmat_df = pd.read_csv("catmat.csv", sep=';', encoding='latin1', low_memory=False)
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)
        return catmat_df, catser_df
    except FileNotFoundError:
        return None, None

catmat_df, catser_df = load_data()

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []
if 'selected_item_key' not in st.session_state:
    st.session_state.selected_item_key = "initial"

# --- Aba de Construção do TR ---
if catmat_df is None or catser_df is None:
    # A mensagem de erro agora reflete os novos nomes de arquivo
    st.error("ERRO CRÍTICO: Os arquivos `catmat.csv` e `catser.csv` não foram encontrados. Por favor, renomeie os arquivos no seu computador e envie-os para o repositório do GitHub.")
else:
    st.header("Construtor Guiado do Termo de Referência")
    st.info("Utilize a busca inteligente para encontrar e adicionar itens padronizados do CATMAT/CATSER à sua tabela.")

    # --- Seção de Busca Inteligente ---
    with st.container(border=True):
        st.subheader("1. Buscar Item no Catálogo")
        
        tipo_catalogo = st.radio("Selecione o catálogo para a busca:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True)
        
        df_selecionado = catmat_df if tipo_catalogo == "CATMAT (Materiais)" else catser_df
        col_codigo = 'Código do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'CÓDIGO'
        col_desc = 'Descrição do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'DESCRIÇÃO'
        col_unid = 'Unidade de Medida' if tipo_catalogo == "CATMAT (Materiais)" else 'UNIDADE DE MEDIDA'
        
        keyword = st.text_input("Digite uma palavra-chave para buscar (ex: caneta, cimento, limpeza):")
        
        if keyword:
            resultados = df_selecionado[df_selecionado[col_desc].str.contains(keyword, case=False, na=False)]
            if not resultados.empty:
                opcoes = [f"{row[col_codigo]} - {row[col_desc]}" for index, row in resultados.iterrows()]
                item_selecionado_str = st.selectbox("Selecione o item desejado nos resultados da busca:", options=["Selecione um item..."] + opcoes)

                if item_selecionado_str != "Selecione um item...":
                    codigo_selecionado = int(item_selecionado_str.split(' - ')[0])
                    detalhe_item = df_selecionado[df_selecionado[col_codigo] == codigo_selecionado].iloc[0]
                    
                    st.session_state.item_cat_code = detalhe_item[col_codigo]
                    st.session_state.item_cat_desc = detalhe_item[col_desc]
                    st.session_state.item_cat_unid = detalhe_item.get(col_unid, "UN")

    # --- Seção para Adicionar o Item Selecionado ---
    with st.container(border=True):
        st.subheader("2. Adicionar Item à Tabela")
        if 'item_cat_desc' in st.session_state:
            st.text_input("Descrição (preenchido automaticamente):", value=st.session_state.item_cat_desc, disabled=True)
            st.text_input("Código CAT (preenchido automaticamente):", value=st.session_state.item_cat_code, disabled=True)
            st.text_input("Unidade (preenchido automaticamente):", value=st.session_state.item_cat_unid, disabled=True)
            
            item_qtd = st.number_input("Informe a Quantidade:", min_value=1, step=1, key="qtd")
            item_valor_unit = st.number_input("Informe o Valor Unitário Estimado (R$):", min_value=0.01, step=0.01, format="%.2f", key="valor")

            if st.button("Adicionar Item à Tabela", type="primary"):
                novo_item = {
                    "Item": len(st.session_state.tr_itens) + 1,
                    "Cód. CAT": st.session_state.item_cat_code,
                    "Descrição": st.session_state.item_cat_desc,
                    "Unidade": st.session_state.item_cat_unid,
                    "Quantidade": item_qtd,
                    "Valor Unitário (R$)": item_valor_unit,
                    "Valor Total (R$)": item_qtd * item_valor_unit
                }
                st.session_state.tr_itens.append(novo_item)
                st.success(f"Item '{st.session_state.item_cat_desc}' adicionado!")
        else:
            st.info("Busque e selecione um item no catálogo acima para poder adicioná-lo.")

    # --- Exibição da Tabela de Itens Construída ---
    if st.session_state.tr_itens:
        st.markdown("---")
        st.subheader("3. Tabela de Itens da Contratação (Anexo I do TR)")
        df_itens = pd.DataFrame(st.session_state.tr_itens)
        st.dataframe(df_itens, use_container_width=True, hide_index=True)
        valor_total_contratacao = df_itens["Valor Total (R$)"].sum()
        st.success(f"**Valor Total Estimado da Contratação: R$ {valor_total_contratacao:,.2f}**")
