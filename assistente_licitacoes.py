import streamlit as st
import pandas as pd
import re
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 11.1 - Versão Robusta")
st.caption("Leitura de dados aprimorada para lidar com variações nos nomes das colunas.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    try:
        df1 = pd.read_csv("catmat 1.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)

        # --- NOVA LÓGICA DE PADRONIZAÇÃO DE COLUNAS ---
        # Mapeamento dos nomes padrão para os nomes possíveis nos arquivos
        CATMAT_MAP = {'Código do Item': 'codigo', 'Descrição do Item': 'descricao', 'Unidade de Medida': 'unidade'}
        CATSER_MAP = {'CÓDIGO': 'codigo', 'DESCRIÇÃO': 'descricao', 'UNIDADE DE MEDIDA': 'unidade'}

        # Limpa espaços e renomeia as colunas para um padrão interno
        catmat_df.columns = catmat_df.columns.str.strip()
        catmat_df.rename(columns=CATMAT_MAP, inplace=True)
        
        catser_df.columns = catser_df.columns.str.strip()
        catser_df.rename(columns=CATSER_MAP, inplace=True)

        # Verificação após a padronização
        for col in ['codigo', 'descricao', 'unidade']:
            if col not in catmat_df.columns:
                raise ValueError(f"Coluna padrão '{col}' não encontrada no CATMAT. Verifique o arquivo original.")
            if col not in catser_df.columns:
                raise ValueError(f"Coluna padrão '{col}' não encontrada no CATSER. Verifique o arquivo original.")

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
# --- FASE 1: PLANEJAMENTO (AJUSTADO PARA USAR NOMES PADRÃO) ---
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
            
            # Agora usamos os nomes padrão internos: 'codigo' e 'descricao'
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
                        codigo_selecionado = int(item_selecionado_str.split(' - ')[0])
                        detalhe_item = df_selecionado[df_selecionado[col_codigo] == codigo_selecionado].iloc[0]
                        st.session_state.item_selecionado = {
                            "code": detalhe_item[col_codigo],
                            "desc": detalhe_item[col_desc],
                            "unid": detalhe_item.get('unidade', "UN")
                        }
        # O restante do código da interface continua o mesmo...

# ==============================================================================
# --- FASE 2 e 3 (Não precisam de alteração) ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    # ...
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    # ...
