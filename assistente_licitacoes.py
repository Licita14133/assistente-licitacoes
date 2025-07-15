import streamlit as st
import pandas as pd
import re

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 10.0 - Busca Inteligente")
st.caption("Ferramenta com busca otimizada e sugestão de termos para CATMAT/CATSER.")

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
        
        # Otimização: Garantir que a coluna de descrição seja do tipo string
        catmat_df['Descrição do Item'] = catmat_df['Descrição do Item'].astype(str)
        catser_df['DESCRIÇÃO'] = catser_df['DESCRIÇÃO'].astype(str)

        return catmat_df, catser_df
    except FileNotFoundError as e:
        return None, None

catmat_df, catser_df = load_data()

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# ==============================================================================
# --- FASE 1: PLANEJAMENTO (COM O NOVO MOTOR DE BUSCA) ---
# ==============================================================================
with tab1:
    if catmat_df is None or catser_df is None:
        st.error("ERRO CRÍTICO: Arquivos de catálogo não encontrados. Verifique o repositório.")
    else:
        st.header("Construtor de Termo de Referência com Busca Inteligente")
        
        with st.container(border=True):
            st.subheader("1. Pesquisa Inteligente de Itens")
            
            tipo_catalogo = st.radio("Selecione o catálogo:", ["CATMAT (Materiais)", "CATSER (Serviços)"], horizontal=True, key="cat_sel")
            
            df, col_codigo, col_desc, col_unid = (
                (catmat_df, 'Código do Item', 'Descrição do Item', 'Unidade de Medida') 
                if tipo_catalogo == "CATMAT (Materiais)" 
                else (catser_df, 'CÓDIGO', 'DESCRIÇÃO', 'UNIDADE DE MEDIDA')
            )
            
            search_query = st.text_input("Digite 3 ou mais caracteres para buscar (ex: cimento portland, caneta azul):", key="search_query")

            # --- LÓGICA DO AUTOCOMPLETE INTELIGENTE ---
            if len(search_query) >= 3:
                # Quebra a busca em palavras-chave
                keywords = search_query.split()
                # Cria uma condição de busca para cada palavra-chave
                conditions = [df[col_desc].str.contains(re.escape(kw), case=False, na=False) for kw in keywords]
                # Combina todas as condições (um item deve conter TODAS as palavras-chave)
                combined_condition = pd.Series(True, index=df.index)
                for condition in conditions:
                    combined_condition &= condition
                
                resultados = df[combined_condition]
                
                if not resultados.empty:
                    # Formata as opções para o selectbox
                    opcoes = ["Selecione um item sugerido..."] + [
                        f"{row[col_codigo]} - {row[col_desc]}" for _, row in resultados.head(20).iterrows() # Limita a 20 sugestões
                    ]
                    
                    item_selecionado_str = st.selectbox("Sugestões encontradas:", options=opcoes)

                    if item_selecionado_str != "Selecione um item sugerido...":
                        codigo_selecionado = int(item_selecionado_str.split(' - ')[0])
                        detalhe_item = df[df[col_codigo] == codigo_selecionado].iloc[0]
                        
                        # Armazena o item selecionado para preencher o formulário abaixo
                        st.session_state.item_selecionado = {
                            "code": detalhe_item[col_codigo],
                            "desc": detalhe_item[col_desc],
                            "unid": detalhe_item.get(col_unid, "UN")
                        }
                else:
                    st.warning("Nenhum item encontrado com todas as palavras-chave. Tente termos mais simples.")

        with st.container(border=True):
            st.subheader("2. Adicionar Item Selecionado à Tabela")
            if 'item_selecionado' in st.session_state:
                st.text_input("Descrição:", value=st.session_state.item_selecionado['desc'], disabled=True)
                st.text_input("Código CAT:", value=st.session_state.item_selecionado['code'], disabled=True)
                
                item_qtd = st.number_input("Informe a Quantidade:", min_value=1, step=1, key="qtd")
                item_valor_unit = st.number_input("Informe o Valor Unitário Estimado (R$):", min_value=0.01, format="%.2f", key="valor")

                if st.button("Adicionar Item à Tabela", type="primary"):
                    novo_item = {
                        "Item": len(st.session_state.tr_itens) + 1,
                        "Cód. CAT": st.session_state.item_selecionado['code'],
                        "Descrição": st.session_state.item_selecionado['desc'],
                        "Unidade": st.session_state.item_selecionado['unid'],
                        "Quantidade": item_qtd,
                        "Valor Unitário (R$)": item_valor_unit,
                        "Valor Total (R$)": item_qtd * item_valor_unit
                    }
                    st.session_state.tr_itens.append(novo_item)
                    st.success(f"Item '{st.session_state.item_selecionado['desc']}' adicionado!")
                    # Limpa a seleção para permitir adicionar um novo item
                    del st.session_state.item_selecionado
                    st.rerun() # Atualiza a tela
            else:
                st.info("Busque e selecione um item acima para habilitar esta seção.")

        if st.session_state.tr_itens:
            st.markdown("---")
            st.subheader("3. Tabela de Itens da Contratação")
            df_itens = pd.DataFrame(st.session_state.tr_itens)
            st.dataframe(df_itens, use_container_width=True, hide_index=True)
            valor_total = df_itens["Valor Total (R$)"].sum()
            st.success(f"**Valor Total Estimado da Contratação: R$ {valor_total:,.2f}**")

# ==============================================================================
# --- FASE 2 e 3 (Restauradas) ---
# ==============================================================================
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    # ... (Conteúdo da Fase 2)
with tab3:
    st.header("Módulos da Fase de Gestão do Contrato")
    # ... (Conteúdo da Fase 3)
