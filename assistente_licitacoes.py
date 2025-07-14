import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 3.0")
st.caption("Um sistema especialista para apoiar o ciclo de vida da contratação pública.")

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: PLANEJAMENTO ---
with tab1:
    st.header("Módulos da Fase de Planejamento")
    
    with st.expander("Checklist do Estudo Técnico Preliminar (ETP)"):
        st.write("Verificações essenciais baseadas nos ETPs de Limpeza, Uniformes e Material Permanente.")
        st.checkbox("A autoridade competente autorizou formalmente a abertura do processo de contratação?", key="p1")
        st.checkbox("A real necessidade da contratação foi detalhada e justificada no ETP?", key="p2")
        st.checkbox("Os requisitos da contratação atendem a critérios de qualidade, sustentabilidade e acessibilidade?", key="p3")
        st.checkbox("O levantamento de mercado analisou diferentes soluções possíveis para atender à necessidade?", key="p4")
        st.checkbox("A estimativa de quantidades e preços foi baseada em memória de cálculo e pesquisa de mercado?", key="p5")

    with st.expander("Ferramenta de Análise de Pesquisa de Preços"):
        st.info("Faça o upload do seu arquivo .csv com as cotações de preços para análise automática.")
        uploaded_file = st.file_uploader("Selecione o arquivo CSV", type="csv", key="price_uploader")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, sep=';', decimal=',')
                if 'Valor' in df.columns:
                    # Limpeza de dados mais robusta
                    df['Valor_Numerico'] = df['Valor'].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.strip()
                    df['Valor_Numerico'] = pd.to_numeric(df['Valor_Numerico'], errors='coerce')
                    df.dropna(subset=['Valor_Numerico'], inplace=True)
                    
                    st.subheader("Análise das Cotações")
                    media = df['Valor_Numerico'].mean()
                    mediana = df['Valor_Numerico'].median()
                    menor_valor = df['Valor_Numerico'].min()
                    
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
         st.checkbox("A autoridade competente autorizou formalmente a realização da licitação?")
         st.checkbox("A Comissão de Contratação (ou agente/pregoeiro) foi formalmente designada por portaria?")
    
    with st.expander("Checklist de Conformidade do Edital"):
        st.write("Verificações baseadas no Edital de Pregão Eletrônico fornecido.")
        st.checkbox("O Termo de Referência, a Minuta do Contrato e o Modelo de Proposta de Preços estão anexados ao Edital?")
        st.checkbox("Os critérios de habilitação jurídica, fiscal, social, trabalhista e econômico-financeira estão claros e de acordo com a Lei?")

    with st.expander("Assistente de Habilitação", expanded=True):
        st.info("Guia para análise dos documentos de habilitação da empresa vencedora, conforme Arts. 62 a 70 da Lei 14.133.")
        
        st.subheader("Habilitação Jurídica (Art. 66)")
        st.checkbox("Apresentou o ato constitutivo, estatuto ou contrato social da empresa?")
        
        st.subheader("Qualificação Fiscal, Social e Trabalhista (Art. 68)")
        st.checkbox("Prova de inscrição no CNPJ.")
        st.checkbox("Prova de regularidade para com a Fazenda Federal (Certidão Negativa ou Positiva com Efeitos de Negativa de Débitos Federais e Dívida Ativa da União).")
        st.checkbox("Prova de regularidade com o Fundo de Garantia do Tempo de Serviço (FGTS) - CRF.")
        st.checkbox("Prova de inexistência de débitos inadimplidos perante a Justiça do Trabalho (CNDT).")

        st.subheader("Qualificação Econômico-Financeira (Art. 69)")
        st.checkbox("Apresentou balanço patrimonial, demonstração de resultado e demais demonstrações contábeis do último exercício?")
        st.checkbox("Apresentou certidão negativa de falência ou recuperação judicial?")

        st.subheader("Declarações (Art. 68, VI)")
        st.checkbox("Apresentou declaração de que não emprega menor de dezoito anos em trabalho noturno, perigoso ou insalubre e de que não emprega menor de dezesseis anos?")

# --- FASE 3: GESTÃO DO CONTRATO ---
with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Ferramentas para apoiar o fiscal do contrato nos eventos da execução contratual.")

    with st.expander("Fiscalização de Rotina"):
        st.checkbox("O serviço/bem foi entregue conforme as especificações do contrato e do termo de referência?")
        st.checkbox("A Nota Fiscal foi recebida e atestada pelo fiscal do contrato?")
        st.checkbox("O pagamento foi realizado no prazo estipulado na cláusula de pagamento do contrato?")

    with st.expander("Assistente para Repactuação de Preços"):
        st.write("Guia para análise de pedidos de repactuação em contratos de serviço com mão de obra exclusiva.")
        st.checkbox("A empresa formalizou o pedido de repactuação por meio de ofício ou requerimento?")
        st.checkbox("O pedido foi protocolado após o intervalo mínimo de 1 ano?")
        st.checkbox("A empresa apresentou a nova Convenção Coletiva de Trabalho (CCT) que fundamenta o pedido?")
        st.checkbox("A nova planilha de custos foi apresentada, demonstrando analiticamente o impacto da nova CCT?")
        st.checkbox("A decisão final (pelo deferimento ou indeferimento) foi formalizada em um documento de Decisão Administrativa?")
    
    with st.expander("Assistente para Apostilamento"):
        st.info("Checklist refinado com base no fluxo de documentos que você forneceu.")
        st.checkbox("O fiscal do contrato solicitou a alteração por meio de despacho ou ofício, justificando a necessidade?")
        st.checkbox("A alteração proposta (ex: readequação da dotação orçamentária) não afeta a natureza do objeto do contrato?")
        st.checkbox("A Declaração de Disponibilidade Orçamentária (DDO) foi emitida para suportar a alteração?")
        st.checkbox("A autoridade competente aprovou a alteração por meio de despacho?")
        st.checkbox("A Minuta do Termo de Apostilamento foi elaborada e assinada pelas partes?")
