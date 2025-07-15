import streamlit as st
import pandas as pd
import re
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 11.2 - Leitor Universal")
st.caption("Versão com detecção automática de separador de colunas para máxima compatibilidade.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    try:
        # A MÁGICA ESTÁ AQUI: engine='python' e sep=None permitem ao Pandas "adivinhar" o separador.
        # Isso resolve o problema de vírgula vs. ponto e vírgula.
        df1 = pd.read_csv("catmat 1.csv", engine='python', sep=None, encoding='latin1', on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", engine='python', sep=None, encoding='latin1', on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        
        catser_df = pd.read_csv("catser.csv", engine='python', sep=None, encoding='latin1', on_bad_lines='skip')
        
        # O restante do código de padronização continua o mesmo
        catmat_df.columns = catmat_df.columns.str.strip()
        catser_df.columns = catser_df.columns.str.strip()
        
        CATMAT_MAP = {'Código do Item': 'codigo', 'Descrição do Item': 'descricao', 'Unidade de Medida': 'unidade'}
        CATSER_MAP = {'CÓDIGO': 'codigo', 'DESCRIÇÃO': 'descricao', 'UNIDADE DE MEDIDA': 'unidade'}

        catmat_df.rename(columns=CATMAT_MAP, inplace=True)
        catser_df.rename(columns=CATSER_MAP, inplace=True)

        for col in ['codigo', 'descricao']:
            if col not in catmat_df.columns:
                raise ValueError(f"Coluna padrão '{col}' não encontrada no CATMAT. Colunas encontradas: {catmat_df.columns.tolist()}")
            if col not in catser_df.columns:
                raise ValueError(f"Coluna padrão '{col}' não encontrada no CATSER. Colunas encontradas: {catser_df.columns.tolist()}")

        catmat_df['descricao'] = catmat_df['descricao'].astype(str)
        catser_df['descricao'] = catser_df['descricao'].astype(str)
        
        return catmat_df, catser_df
        
    except FileNotFoundError as e:
        st.error(f"ERRO DE ARQUIVO: O arquivo '{e.filename}' não foi encontrado.")
        return None, None
    except Exception as e:
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
        
        with st.container(border=True):
            st.subheader("1. Construção da Tabela de Itens (Busca Inteligente)")
            tipo_catalogo = st.radio("Selecione o catálogo:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True, key="cat_sel")
            
            df_selecionado = catmat_df if tipo_catalogo == "CATMAT (Materiais)" else catser_df
            
            col_codigo = 'codigo'
            col_desc = 'descricao'
            
            search_query = st.text_input("Digite 3 ou mais caracteres para buscar:", key="search_query")

            if len(search_query) >= 3:
                keywords = search_query.split()
                conditions = [df_selecionado[col_desc].str.contains(re.escape(kw), case=False, na=False) for kw in keywords]
                combined_condition = pd.Series(True, index=df_selecionado.index)
                for condition in conditions:
                    combined_condition &= condition
                
                resultados = df_selecionado[combined_condition]
                
                if not resultados.empty:
                    opcoes = ["Selecione um item sugerido..."] + [f"{row[col_codigo]} - {row[col_desc]}" for _, row in resultados.head(100).iterrows()]
                    item_selecionado_str = st.selectbox("Sugestões encontradas:", options=opcoes)

                    if item_selecionado_str != "Selecione um item sugerido...":
                        # Lógica de seleção...
                        pass
        # O restante da interface continua aqui...

# ==============================================================================
# --- FASE 2 e 3 (Não precisam de alteração) ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    # ...
with tab3:
    st.header("Módulos da Fase de Gestão do Contrato")
    # ...
