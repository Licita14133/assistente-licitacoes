import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 7.5 - Leitor de Arquivos Divididos")
st.caption("Construção de TR com busca inteligente e padronização de itens.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    catmat_part1_name = "catmat 1.csv"
    catmat_part2_name = "catmat 2.csv"
    catser_filename = "catser.csv"
    
    try:
        # Lendo as duas partes do CATMAT
        print(f"Lendo a parte 1 do CATMAT: {catmat_part1_name}")
        df1 = pd.read_csv(catmat_part1_name, sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        
        print(f"Lendo a parte 2 do CATMAT: {catmat_part2_name}")
        df2 = pd.read_csv(catmat_part2_name, sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        
        # Juntando as duas partes em uma única tabela
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        print("As duas partes do CATMAT foram unidas com sucesso.")
        
        # Lendo o CATSER
        print(f"Lendo o CATSER: {catser_filename}")
        catser_df = pd.read_csv(catser_filename, sep=';', encoding='latin1', low_memory=False)
        
        # Limpando espaços extras nos nomes das colunas para maior robustez
        catmat_df.columns = catmat_df.columns.str.strip()
        catser_df.columns = catser_df.columns.str.strip()
        
        return catmat_df, catser_df
        
    except FileNotFoundError as e:
        st.error(f"ERRO CRÍTICO: Um dos arquivos de catálogo não foi encontrado. Verifique se os nomes no repositório são exatamente 'catmat 1.csv', 'catmat 2.csv' e 'catser.csv'. Detalhe do erro: {e}")
        return None, None
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler ou processar os arquivos: {e}")
        return None, None

catmat_df, catser_df = load_data()

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []

# --- Corpo Principal do Aplicativo ---
if catmat_df is None or catser_df is None:
    st.warning("Aguardando o carregamento completo dos arquivos de catálogo...")
else:
    st.header("Construtor Guiado do Termo de Referência")
    st.info("Utilize a busca inteligente para encontrar e adicionar itens padronizados do CATMAT/CATSER à sua tabela.")

    # --- Seção de Busca Inteligente ---
    with st.container(border=True):
        st.subheader("1. Buscar Item no Catálogo")
        
        tipo_catalogo = st.radio("Selecione o catálogo para a busca:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True)
        
        if tipo_catalogo == "CATMAT (Materiais)":
            df_selecionado = catmat_df
            col_codigo = 'Código do Item'
            col_desc = 'Descrição do Item'
            col_unid = 'Unidade de Medida'
        else: # CATSER
            df_selecionado = catser_df
            col_codigo = 'CÓDIGO'
            col_desc = 'DESCRIÇÃO'
            col_unid = 'UNIDADE DE MEDIDA'
        
        keyword = st.text_input("Digite uma palavra-chave para buscar (ex: caneta, cimento, limpeza):")
        
        if keyword:
            resultados = df_selecionado[df_selecionado[col_desc].str.contains(keyword, case=False, na=False)]
            
            if not resultados.empty:
                opcoes = [f"{row[col_codigo]} - {row[col_desc]}" for index, row in resultados.head(100).iterrows()]
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
            st.text_input("Descrição (preenchido automaticamente):", value=st.session_state.item_cat_desc, disabled=True, key="desc_auto")
            st.text_input("Código CAT (preenchido automaticamente):", value=st.session_state.item_cat_code, disabled=True, key="code_auto")
            st.text_input("Unidade (preenchido automaticamente):", value=st.session_state.item_cat_unid, disabled=True, key="unid_auto")
            
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
