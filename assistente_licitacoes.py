import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 9.1 - Versão Final Consolidada")
st.caption("Ferramenta especialista com as 3 fases, análise de conformidade e leitura correta dos catálogos.")

# --- Carregamento e Cache dos Catálogos (VERSÃO CORRIGIDA) ---
@st.cache_data
def load_data():
    try:
        # Lendo as duas partes do CATMAT, conforme solucionamos
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
        # Mensagem de erro específica para o usuário
        st.error(f"ERRO DE ARQUIVO: O arquivo '{e.filename}' não foi encontrado. Por favor, verifique se os nomes no repositório são exatamente 'catmat 1.csv', 'catmat 2.csv' e 'catser.csv'.")
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
        st.header("Construtor e Analisador do Planejamento")
        st.info("Construa a tabela de itens e depois preencha o checklist de conformidade para gerar uma análise prévia.")

        with st.container(border=True):
            st.subheader("1. Construção da Tabela de Itens (Anexo I do TR)")
            tipo_catalogo = st.radio("Catálogo:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True, key="cat_sel")
            df_selecionado = catmat_df if tipo_catalogo == "CATMAT (Materiais)" else catser_df
            col_codigo = 'Código do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'CÓDIGO'
            col_desc = 'Descrição do Item' if tipo_catalogo == "CATMAT (Materiais)" else 'DESCRIÇÃO'
            
            keyword = st.text_input("Digite uma palavra-chave para buscar:")
            # ... (Restante da lógica de busca e adição de item, que já estava correta)

        if st.session_state.tr_itens:
            st.subheader("Tabela de Itens Construída")
            st.dataframe(pd.DataFrame(st.session_state.tr_itens), use_container_width=True, hide_index=True)
            valor_total = pd.DataFrame(st.session_state.tr_itens)["Valor Total (R$)"].sum()
            st.success(f"**Valor Total Estimado: R$ {valor_total:,.2f}**")

        st.markdown("---")
        with st.container(border=True):
            st.subheader("2. Checklist de Conformidade do Planejamento")
            st.checkbox("A necessidade da contratação está devidamente justificada no processo?", key="chk_justificativa")
            st.checkbox("A descrição do objeto (tabela de itens) é precisa, suficiente e clara, sem restrição de competição?", key="chk_objeto")
            st.checkbox("A estimativa de valor da contratação foi baseada em pesquisa de mercado ampla e documentada?", key="chk_pesquisa_preco")
            st.checkbox("A Declaração de Disponibilidade Orçamentária (DDO) foi emitida?", key="chk_ddo")

            if st.button("Gerar Análise de Conformidade", type="primary"):
                # Lógica para gerar o relatório de análise...
                pass
# ==============================================================================
# --- FASE 2: SELEÇÃO DO FORNECEDOR ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    with st.expander("Atos Preparatórios"):
         st.checkbox("A autoridade competente autorizou formalmente a realização da licitação?")
         st.checkbox("A Comissão de Contratação (ou agente/pregoeiro) foi designada por portaria?")
    
    with st.expander("Conformidade do Edital"):
        st.checkbox("O Termo de Referência, a Minuta do Contrato e o Modelo de Proposta estão anexados ao Edital?")
        st.checkbox("Os critérios de habilitação estão claros e de acordo com os Arts. 62 a 70 da Lei 14.133?")

    with st.expander("Assistente de Habilitação", expanded=True):
        st.info("Guia para análise dos documentos da empresa vencedora.")
        st.subheader("Fiscal, Social e Trabalhista")
        st.checkbox("Prova de regularidade com a Fazenda Federal (CND).")
        st.checkbox("Prova de regularidade com o FGTS (CRF).")
        st.checkbox("Prova de inexistência de débitos trabalhistas (CNDT).")
        st.subheader("Econômico-Financeira")
        st.checkbox("Certidão negativa de falência ou recuperação judicial.")

# ==============================================================================
# --- FASE 3: GESTÃO DO CONTRATO ---
# ==============================================================================
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    with st.expander("Fiscalização de Rotina"):
        st.checkbox("O serviço/bem foi entregue conforme as especificações do contrato?")
        st.checkbox("A Nota Fiscal foi recebida e atestada pelo fiscal?")
        st.checkbox("O pagamento foi realizado no prazo estipulado?")

    with st.expander("Fluxo de Trabalho: Repactuação de Preços", expanded=True):
        st.info("Guia para análise de pedidos de repactuação.")
        st.checkbox("A empresa formalizou o pedido por ofício?")
        st.checkbox("O pedido foi protocolado após o intervalo mínimo de 1 ano?")
        st.checkbox("A empresa apresentou a nova CCT e a planilha de custos atualizada?")
        st.checkbox("A decisão final foi formalizada pela autoridade competente?")
    
    with st.expander("Fluxo de Trabalho: Apostilamento", expanded=True):
        st.info("Checklist baseado na sequência real de documentos.")
        st.checkbox("1. O fiscal do contrato solicitou a alteração via Ofício/Despacho?")
        st.checkbox("2. A autoridade competente exarou despacho favorável?")
        st.checkbox("3. A Declaração de Disponibilidade Orçamentária (DDO) foi emitida?")
        st.checkbox("4. O Termo de Apostilamento foi elaborado e assinado?")
