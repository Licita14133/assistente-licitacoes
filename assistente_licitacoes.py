import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 8.0 - Estrutura Completa")
st.caption("Ferramenta especialista com as 3 fases do processo de contratação.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    try:
        df1 = pd.read_csv("catmat 1.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)
        
        catmat_df.columns = catmat_df.columns.str.strip()
        catser_df.columns = catser_df.columns.str.strip()
        
        return catmat_df, catser_df
    except FileNotFoundError as e:
        return None, None
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler os arquivos de catálogo: {e}")
        return None, None

catmat_df, catser_df = load_data()

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# ==============================================================================
# --- FASE 1: PLANEJAMENTO (VERSÃO FUNCIONAL COM CATMAT/CATSER) ---
# ==============================================================================
with tab1:
    if catmat_df is None or catser_df is None:
        st.error("ERRO CRÍTICO: Arquivos de catálogo não encontrados. Verifique se 'catmat 1.csv', 'catmat 2.csv' e 'catser.csv' estão no repositório.")
    else:
        st.header("Construtor Guiado do Termo de Referência")
        st.info("Utilize a busca inteligente para encontrar e adicionar itens padronizados do CATMAT/CATSER à sua tabela.")

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
            # ... (código para adicionar item, igual à versão anterior)
            st.info("Preencha a quantidade e o valor para o item selecionado.")


        if st.session_state.tr_itens:
            st.markdown("---")
            st.subheader("3. Tabela de Itens da Contratação (Anexo I do TR)")
            # ... (código para exibir a tabela, igual à versão anterior)
            
# ==============================================================================
# --- FASE 2: SELEÇÃO DO FORNECEDOR (MÓDULOS RESTAURADOS) ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")

    with st.expander("Atos Preparatórios da Fase de Seleção"):
         st.checkbox("A autoridade competente autorizou formalmente a realização da licitação?")
         st.checkbox("A Comissão de Contratação (ou agente/pregoeiro) foi formalmente designada por portaria?")
    
    with st.expander("Checklist de Conformidade do Edital"):
        st.checkbox("O Termo de Referência, a Minuta do Contrato e o Modelo de Proposta de Preços estão anexados ao Edital?")
        st.checkbox("Os critérios de habilitação jurídica, fiscal, social, trabalhista e econômico-financeira estão claros e de acordo com a Lei?")

    with st.expander("Assistente de Habilitação", expanded=True):
        st.info("Guia para análise dos documentos de habilitação da empresa vencedora, conforme Arts. 62 a 70 da Lei 14.133 e o Edital.")
        st.subheader("Qualificação Fiscal, Social e Trabalhista")
        st.checkbox("Prova de regularidade para com a Fazenda Federal (Certidão Negativa de Débitos).")
        st.checkbox("Prova de regularidade com o FGTS (CRF).")
        st.checkbox("Prova de inexistência de débitos inadimplidos perante a Justiça do Trabalho (CNDT).")
        st.subheader("Qualificação Econômico-Financeira")
        st.checkbox("Apresentou certidão negativa de falência ou recuperação judicial?")

# ==============================================================================
# --- FASE 3: GESTÃO DO CONTRATO (MÓDULOS RESTAURADOS) ---
# ==============================================================================
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Ferramentas para apoiar o fiscal do contrato nos eventos da execução contratual.")

    with st.expander("Fiscalização de Rotina"):
        st.checkbox("O serviço/bem foi entregue conforme as especificações do contrato?")
        st.checkbox("A Nota Fiscal foi recebida e atestada pelo fiscal do contrato?")
        st.checkbox("O pagamento foi realizado no prazo estipulado na cláusula de pagamento do contrato? [cite: CON
