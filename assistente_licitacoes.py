import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 8.2 - Versão Estável")
st.caption("Ferramenta especialista com as 3 fases do processo de contratação.")

# --- Carregamento e Cache dos Catálogos com Tratamento de Erro Aprimorado ---
@st.cache_data
def load_data():
    try:
        # Lendo as duas partes do CATMAT
        df1 = pd.read_csv("catmat 1.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        
        # Lendo o CATSER
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)
        
        # Limpando espaços extras nos nomes das colunas
        catmat_df.columns = catmat_df.columns.str.strip()
        catser_df.columns = catser_df.columns.str.strip()
        
        return catmat_df, catser_df
        
    except FileNotFoundError as e:
        # Mensagem de erro mais específica para o usuário
        st.error(f"ERRO DE ARQUIVO: O arquivo '{e.filename}' não foi encontrado. Por favor, verifique se o nome está correto e se ele foi enviado para o repositório do GitHub.")
        return None, None
    except Exception as e:
        # Captura outros erros de leitura ou processamento
        st.error(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
        return None, None

catmat_df, catser_df = load_data()

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# ==============================================================================
# --- FASE 1: PLANEJAMENTO ---
# ==============================================================================
with tab1:
    if catmat_df is None or catser_df is None:
        st.warning("Aguardando o carregamento dos arquivos de catálogo. Verifique a mensagem de erro acima se o problema persistir.")
    else:
        st.header("Construtor Guiado do Termo de Referência")
        st.info("Utilize a busca inteligente para encontrar e adicionar itens padronizados do CATMAT/CATSER à sua tabela.")

        # O restante do código da Fase 1 continua o mesmo
        with st.container(border=True):
            st.subheader("1. Buscar Item no Catálogo")
            tipo_catalogo = st.radio("Selecione o catálogo:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True, key="cat_sel")
            df_selecionado = catmat_df if tipo_catalogo == "CATMAT (Materiais)" else catser_df
            col_codigo = 'Código do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'CÓDIGO'
            col_desc = 'Descrição do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'DESCRIÇÃO'
            col_unid = 'Unidade de Medida' if tipo_catalogo == "CATMAT (Materiais)" else 'UNIDADE DE MEDIDA'
            
            keyword = st.text_input("Digite uma palavra-chave para buscar:")
            if keyword:
                resultados = df_selecionado[df_selecionado[col_desc].str.contains(keyword, case=False, na=False)]
                if not resultados.empty:
                    opcoes = [f"{row[col_codigo]} - {row[col_desc]}" for index, row in resultados.head(100).iterrows()]
                    item_selecionado_str = st.selectbox("Selecione o item desejado:", options=["Selecione um item..."] + opcoes)
                    if item_selecionado_str != "Selecione um item...":
                        codigo_selecionado = int(item_selecionado_str.split(' - ')[0])
                        detalhe_item = df_selecionado[df_selecionado[col_codigo] == codigo_selecionado].iloc[0]
                        st.session_state.item_cat_code = detalhe_item[col_codigo]
                        st.session_state.item_cat_desc = detalhe_item[col_desc]
                        st.session_state.item_cat_unid = detalhe_item.get(col_unid, "UN")
        
        with st.container(border=True):
            st.subheader("2. Adicionar Item à Tabela")
            st.info("Preencha a quantidade e o valor para o item selecionado.")
            # ... (código para adicionar item)

        if st.session_state.tr_itens:
            st.markdown("---")
            st.subheader("3. Tabela de Itens da Contratação (Anexo I do TR)")
            # ... (código para exibir a tabela)
            
# ==============================================================================
# --- FASE 2: SELEÇÃO DO FORNECEDOR ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    # ... (código da Fase 2)

# ==============================================================================
# --- FASE 3: GESTÃO DO CONTRATO ---
# ==============================================================================
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    # ... (código da Fase 3)
