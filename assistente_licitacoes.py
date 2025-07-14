import streamlit as st
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 6.0 - Montador de Documentos")
st.caption("Construção guiada e inteligente de artefatos de contratação, baseada nos modelos da AGU.")

# Inicializar o session_state para guardar os inputs
if 'tr_inputs' not in st.session_state:
    st.session_state.tr_inputs = {}

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Construção do Termo de Referência", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: CONSTRUÇÃO DO TERMO DE REFERÊNCIA ---
with tab1:
    st.header("Montador Guiado do Termo de Referência (Modelo: Compras)")
    st.info("Siga os passos abaixo. O assistente irá exibir o texto fixo do modelo e solicitar apenas as informações necessárias.")

    # --- Passo 1: Contextualização ---
    st.subheader("Passo 1: Contextualização da Compra")
    st.session_state.tr_inputs['exige_amostra'] = st.toggle(
        "A contratação exigirá apresentação de amostra?", 
        help="Marque esta opção se a avaliação de amostras for indispensável para verificar o atendimento das especificações."
    )

    # --- Passo 2: Construção Guiada do Documento ---
    st.subheader("Passo 2: Preenchimento das Seções do TR")

    # Usando st.form para agrupar os inputs
    with st.form("tr_builder_form"):
        # TÓPICO 1: OBJETO
        st.markdown("---")
        st.markdown("#### Tópico 1: DO OBJETO")
        st.markdown(
            "**Texto Fixo do Modelo:**\n"
            "```\n"
            "1.1. O presente Termo de Referência tem por objeto a aquisição de [NOME GENÉRICO DO BEM], conforme condições e especificações constantes neste instrumento e em seus Anexos.\n"
            "```"
        )
        st.session_state.tr_inputs['objeto_especificacoes'] = st.text_area(
            "**Campo Editável:** Detalhe as especificações, quantidades e condições do objeto.",
            height=150,
            help="Descreva de forma precisa, suficiente e clara, sem indicar marcas. Baseado no Item 2 dos modelos."
        )

        # TÓPICO 4: CONDIÇÕES DE ENTREGA
        st.markdown("---")
        st.markdown("#### Tópico 4: DO LOCAL E DAS CONDIÇÕES DE ENTREGA DO OBJETO")
        st.markdown(
            "**Texto Fixo do Modelo:**\n"
            "```\n"
            "4.1. O local de entrega dos bens é [ENDEREÇO COMPLETO].\n"
            "4.2. O prazo de entrega será de [PRAZO EM DIAS] dias, contados do(a) [DEFINIR MARCO INICIAL].\n"
            "```"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.tr_inputs['local_entrega'] = st.text_input("**Campo Editável:** Insira o endereço completo de entrega.")
        with col2:
            st.session_state.tr_inputs['prazo_entrega'] = st.number_input("**Campo Editável:** Prazo de entrega (em dias).", min_value=1, step=1)
        st.info("**Nota Explicativa:** O marco inicial para contagem do prazo (ex: assinatura do contrato, emissão da nota de empenho) deve ser definido de forma clara.")

        # SEÇÃO CONDICIONAL: AMOSTRAS
        if st.session_state.tr_inputs['exige_amostra']:
            st.markdown("---")
            st.markdown("#### Tópico 4.X: DA APRESENTAÇÃO DE AMOSTRAS (Seção Condicional)")
            st.warning("Você indicou a necessidade de amostras. Preencha as regras abaixo.")
            st.session_state.tr_inputs['prazo_amostra'] = st.text_input(
                "**Campo Editável:** Prazo e local para apresentação das amostras pelo licitante vencedor."
            )

        # Botão de submissão do formulário
        submitted = st.form_submit_button("Gerar Documento Final")

    # --- Passo 3: Geração do Documento Final ---
    if submitted:
        st.subheader("Passo 3: Documento Gerado")
        
        # Montagem do documento final
        documento_final = "TERMO DE REFERÊNCIA (Versão Gerada pelo Assistente)\n"
        documento_final += "="*60 + "\n\n"
        
        # Seção 1
        documento_final += "1. DO OBJETO\n"
        documento_final += "1.1. O presente Termo de Referência tem por objeto a aquisição de bens, conforme especificações abaixo:\n"
        documento_final += f"{st.session_state.tr_inputs.get('objeto_especificacoes', '[ESPECIFICAÇÕES NÃO PREENCHIDAS]')}\n\n"

        # Seção 4
        documento_final += "4. DO LOCAL E DAS CONDIÇÕES DE ENTREGA DO OBJETO\n"
        documento_final += f"4.1. O local de entrega dos bens é: {st.session_state.tr_inputs.get('local_entrega', '[ENDEREÇO NÃO PREENCHIDO]')}\n"
        documento_final += f"4.2. O prazo de entrega será de {st.session_state.tr_inputs.get('prazo_entrega', '[PRAZO NÃO PREENCHIDO]')} dias.\n\n"

        # Seção Condicional de Amostras
        if st.session_state.tr_inputs.get('exige_amostra'):
            documento_final += "4.X. DA APRESENTAÇÃO DE AMOSTRAS\n"
            documento_final += f"As amostras deverão ser apresentadas conforme as seguintes condições: {st.session_state.tr_inputs.get('prazo_amostra', '[CONDIÇÕES NÃO PREENCHIDAS]')}\n\n"
        
        st.info("Abaixo está a prévia do seu documento. Use o botão para fazer o download.")
        st.text_area("Prévia do Documento", documento_final, height=300)

        st.download_button(
            label="📥 Baixar Termo de Referência (.txt)",
            data=documento_final,
            file_name=f"TR_Gerado_{datetime.now().strftime('%Y%m%d')}.txt"
        )

# --- FASE 2 e 3 ---
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    st.info("Em breve: Montador Guiado do Edital.")

with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Em breve: Montador Guiado para Termos Aditivos.")
