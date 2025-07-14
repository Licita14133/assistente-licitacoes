import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 3.1 (Refinado)")
st.caption("Um sistema especialista para apoiar o ciclo de vida da contratação pública.")

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: PLANEJAMENTO ---
with tab1:
    st.header("Módulos da Fase de Planejamento")
    
    with st.expander("Checklist do ETP e Termo de Referência (TR)", expanded=True):
        st.info("Verificações refinadas com base nos documentos de ETP, TR e Autorização fornecidos.")
        st.checkbox("O processo foi iniciado com a devida autorização da autoridade competente?")
        st.checkbox("A necessidade da contratação e a previsão no Plano de Contratações Anual estão justificadas? (Baseado no Item 3 do TR)")
        st.checkbox("A descrição do objeto é precisa, suficiente e clara, evitando especificações restritivas? (Item 2 do TR)")
        st.checkbox("O Modelo de Proposta de Preços foi definido e anexado ao TR?")
        st.checkbox("Os critérios de medição e as regras de pagamento estão claramente definidos? (Item 9 do TR)")
        st.checkbox("As responsabilidades da Contratante e da Contratada estão bem estabelecidas? (Item 10 do TR)")
        st.checkbox("A estimativa de preços foi anexada e contém pesquisa de mercado ampla? (Baseado nos arquivos de cotação)")

    with st.expander("Ferramenta de Análise de Pesquisa de Preços"):
        st.info("Faça o upload do seu arquivo .csv com as cotações de preços para análise automática.")
        # O código do uploader continua o mesmo
        uploaded_file = st.file_uploader("Selecione o arquivo CSV", type="csv", key="price_uploader")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, sep=';', decimal=',')
                if 'Valor' in df.columns:
                    df['Valor_Numerico'] = df['Valor'].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.strip()
                    df['Valor_Numerico'] = pd.to_numeric(df['Valor_Numerico'], errors='coerce')
                    df.dropna(subset=['Valor_Numerico'], inplace=True)
                    media = df['Valor_Numerico'].mean()
                    mediana = df['Valor_Numerico'].median()
                    menor_valor = df['Valor_Numerico'].min()
                    st.subheader("Análise das Cotações")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Preço Médio", f"R$ {media:,.2f}")
                    col2.metric("Mediana", f"R$ {mediana:,.2f}")
                    col3.metric("Menor Valor", f"R$ {menor_valor:,.2f}")
                    st.dataframe(df)
                else:
                    st.error("Erro: O arquivo CSV precisa ter uma coluna chamada 'Valor'.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

# --- FASE 2: SELEÇÃO DO FORNECEDOR ---
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")

    with st.expander("Atos Preparatórios da Fase de Seleção"):
         st.checkbox("A Comissão de Contratação (ou agente/pregoeiro) foi formalmente designada por portaria?")
    
    with st.expander("Checklist de Conformidade do Edital"):
        st.checkbox("O objeto no Edital está idêntico ao do Termo de Referência? (Item 1 do Edital)")
        st.checkbox("As regras e prazos para impugnação e esclarecimentos estão claras? (Item 6 do Edital)")
        st.checkbox("Os critérios de julgamento da proposta (ex: menor preço) estão definidos objetivamente? (Item 9 do Edital)")

    with st.expander("Assistente de Habilitação", expanded=True):
        st.info("Guia para análise dos documentos, conforme Edital e Lei 14.133.")
        
        st.subheader("Qualificação Fiscal, Social e Trabalhista (Item 10.3 do Edital)")
        st.checkbox("Prova de regularidade para com a Fazenda Federal (Certidão de Débitos Federais e Dívida Ativa da União).")
        st.checkbox("Prova de regularidade com o Fundo de Garantia do Tempo de Serviço (FGTS) - CRF.")
        st.checkbox("Prova de inexistência de débitos inadimplidos perante a Justiça do Trabalho (CNDT).")

        st.subheader("Qualificação Econômico-Financeira (Item 10.4 do Edital)")
        st.checkbox("Apresentou certidão negativa de falência ou recuperação judicial?")

# --- FASE 3: GESTÃO DO CONTRATO ---
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Ferramentas para apoiar o fiscal do contrato nos eventos da execução contratual.")

    with st.expander("Fiscalização de Rotina"):
        st.checkbox("O serviço/bem foi entregue conforme as especificações do contrato?")
        st.checkbox("A Nota Fiscal foi recebida e atestada?")
        st.checkbox("O pagamento foi realizado no prazo correto?")

    with st.expander("Fluxo de Trabalho: Apostilamento", expanded=True):
        st.info("Checklist baseado na sequência de documentos do processo de apostilamento.")
        st.checkbox("1. O fiscal do contrato solicitou a alteração via Ofício, justificando a necessidade?")
        st.checkbox("2. A autoridade competente exarou despacho favorável à alteração?")
        st.checkbox("3. A Declaração de Disponibilidade Orçamentária (DDO) foi emitida para a nova dotação?")
        st.checkbox("4. O Termo de Apostilamento foi elaborado, assinado e publicado?")

    with st.expander("Fluxo de Trabalho: Repactuação de Preços"):
        st.write("Guia para análise de pedidos de repactuação em contratos de serviço com mão de obra exclusiva.")
        st.checkbox("1. A empresa protocolou o pedido formal de repactuação?")
        st.checkbox("2. O pedido foi acompanhado da nova Convenção Coletiva de Trabalho (CCT)?")
        st.checkbox("3. A nova planilha de custos foi apresentada, demonstrando o impacto analítico da CCT?")
        st.checkbox("4. A análise técnica da planilha foi concluída pela equipe de planejamento?")
        st.checkbox("5. A decisão sobre o pedido foi formalizada pela autoridade competente?")
