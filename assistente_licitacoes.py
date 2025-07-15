import streamlit as st
import pandas as pd
import re
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 11.0 - Versão Consolidada")
st.caption("Ferramenta especialista com as 3 fases do processo de contratação, com busca inteligente e guias de conformidade.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    try:
        df1 = pd.read_csv("catmat 1.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)
        
        for df in [catmat_df, catser_df]:
            df.columns = df.columns.str.strip()
        
        catmat_df['Descrição do Item'] = catmat_df['Descrição do Item'].astype(str)
        catser_df['DESCRIÇÃO'] = catser_df['DESCRIÇÃO'].astype(str)
        return catmat_df, catser_df
    except FileNotFoundError as e:
        st.error(f"ERRO DE ARQUIVO: O arquivo '{e.filename}' não foi encontrado. Verifique se os nomes no repositório estão corretos ('catmat 1.csv', 'catmat 2.csv', 'catser.csv').")
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
            
            df, col_codigo, col_desc, col_unid = (
                (catmat_df, 'Código do Item', 'Descrição do Item', 'Unidade de Medida') 
                if tipo_catalogo == "CATMAT (Materiais)" 
                else (catser_df, 'CÓDIGO', 'DESCRIÇÃO', 'UNIDADE DE MEDIDA')
            )
            
            search_query = st.text_input("Digite 3 ou mais caracteres para buscar:", key="search_query")

            if len(search_query) >= 3:
                keywords = search_query.split()
                conditions = [df[col_desc].str.contains(re.escape(kw), case=False, na=False) for kw in keywords]
                combined_condition = pd.Series(True, index=df.index)
                for condition in conditions:
                    combined_condition &= condition
                
                resultados = df[combined_condition]
                
                if not resultados.empty:
                    opcoes = ["Selecione um item sugerido..."] + [f"{row[col_codigo]} - {row[col_desc]}" for _, row in resultados.head(20).iterrows()]
                    item_selecionado_str = st.selectbox("Sugestões encontradas:", options=opcoes)

                    if item_selecionado_str != "Selecione um item sugerido...":
                        codigo_selecionado = int(item_selecionado_str.split(' - ')[0])
                        detalhe_item = df[df[col_codigo] == codigo_selecionado].iloc[0]
                        st.session_state.item_selecionado = {"code": detalhe_item[col_codigo], "desc": detalhe_item[col_desc], "unid": detalhe_item.get(col_unid, "UN")}

        with st.container(border=True):
            st.subheader("2. Adicionar Item Selecionado à Tabela")
            if 'item_selecionado' in st.session_state:
                st.text_input("Descrição:", value=st.session_state.item_selecionado['desc'], disabled=True)
                item_qtd = st.number_input("Informe a Quantidade:", min_value=1, step=1, key="qtd")
                item_valor_unit = st.number_input("Informe o Valor Unitário Estimado (R$):", min_value=0.01, format="%.2f", key="valor")

                if st.button("Adicionar Item à Tabela", type="primary"):
                    st.session_state.tr_itens.append({
                        "Item": len(st.session_state.tr_itens) + 1, "Cód. CAT": st.session_state.item_selecionado['code'],
                        "Descrição": st.session_state.item_selecionado['desc'], "Unidade": st.session_state.item_selecionado['unid'],
                        "Quantidade": item_qtd, "Valor Unitário (R$)": item_valor_unit,
                        "Valor Total (R$)": item_qtd * item_valor_unit
                    })
                    del st.session_state.item_selecionado
                    st.rerun()
            else:
                st.info("Busque e selecione um item acima para habilitar esta seção.")

        if st.session_state.tr_itens:
            st.markdown("---")
            st.subheader("3. Tabela de Itens da Contratação")
            st.dataframe(pd.DataFrame(st.session_state.tr_itens), use_container_width=True, hide_index=True)
            valor_total = pd.DataFrame(st.session_state.tr_itens)["Valor Total (R$)"].sum()
            st.success(f"**Valor Total Estimado: R$ {valor_total:,.2f}**")

# ==============================================================================
# --- FASE 2: SELEÇÃO DO FORNECEDOR ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    with st.expander("Atos Preparatórios da Fase de Seleção"):
         st.checkbox("A autoridade competente autorizou formalmente a realização da licitação?")
         st.checkbox("A Comissão de Contratação (ou agente/pregoeiro) foi formalmente designada por portaria?")
    
    with st.expander("Conformidade do Edital"):
        st.info("Verifique se o edital está alinhado com o planejamento e a legislação.")
        st.checkbox("O Termo de Referência, a Minuta do Contrato e o Modelo de Proposta de Preços estão anexados ao Edital?")
        st.checkbox("Os critérios de habilitação estão claros e de acordo com os Arts. 62 a 70 da Lei 14.133?")

    with st.expander("Assistente de Habilitação", expanded=True):
        st.info("Guia para análise dos documentos da empresa vencedora.")
        st.subheader("Qualificação Fiscal, Social e Trabalhista")
        st.checkbox("Prova de regularidade para com a Fazenda Federal (CND).")
        st.checkbox("Prova de regularidade com o FGTS (CRF).")
        st.checkbox("Prova de inexistência de débitos inadimplidos perante a Justiça do Trabalho (CNDT).")
        st.subheader("Qualificação Econômico-Financeira")
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

    with st.expander("Fluxo de Trabalho: Repactuação de Preços"):
        st.info("Guia para análise de pedidos de repactuação.")
        st.checkbox("A empresa formalizou o pedido por ofício?")
        st.checkbox("O pedido foi protocolado após o intervalo mínimo de 1 ano?")
        st.checkbox("A empresa apresentou a nova CCT e a planilha de custos atualizada?")
        st.checkbox("A decisão final foi formalizada pela autoridade competente?")
    
    with st.expander("Fluxo de Trabalho: Apostilamento"):
        st.info("Checklist baseado na sequência real de documentos.")
        st.checkbox("1. O fiscal do contrato solicitou a alteração via Ofício/Despacho?")
        st.checkbox("2. A autoridade competente exarou despacho favorável?")
        st.checkbox("3. A Declaração de Disponibilidade Orçamentária (DDO) foi emitida?")
        st.checkbox("4. O Termo de Apostilamento foi elaborado e assinado?")
