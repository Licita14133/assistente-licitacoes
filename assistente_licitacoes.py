import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 5.1 - Intérprete da AGU")
st.caption("Uma ferramenta especialista para a construção e análise de artefatos de contratação.")

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento (ETP/TR)", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: PLANEJAMENTO (Refinamento profundo) ---
with tab1:
    st.header("Construtor Guiado do Termo de Referência")
    st.info("Responda às perguntas e preencha os campos. O assistente usará a lógica das notas explicativas da AGU para guiar você.")

    # --- Perguntas de Contexto ---
    st.subheader("1. Definição do Escopo da Contratação")
    tipo_objeto = st.selectbox("Qual é a natureza do objeto?", ["Selecione...", "Compras", "Serviços"])
    
    if tipo_objeto == "Serviços":
        dedicacao_mo = st.radio("O serviço envolve dedicação exclusiva de mão de obra?", ("Sim", "Não"), horizontal=True, key="mo")

    # --- Formulário para Construção do Documento ---
    if tipo_objeto != "Selecione...":
        with st.form("tr_form_refinado"):
            st.subheader("2. Preenchimento Guiado do Documento")

            # Seção de Objeto
            st.markdown("##### Seção 2: Objeto da Contratação")
            objeto_desc = st.text_area("Descreva o objeto de forma precisa, suficiente e clara.", key="obj")

            # Seção de Justificativa
            st.markdown("##### Seção 3: Justificativa e Necessidade")
            justificativa_desc = st.text_area("Detalhe a necessidade da contratação e o interesse público envolvido.", key="just")
            
            # Seção de Sustentabilidade (Com lógica da Nota Explicativa)
            st.markdown("##### Seção 4: Critérios de Sustentabilidade")
            st.info("""
            **Nota Explicativa da AGU:** "A Administração deverá estabelecer critérios de sustentabilidade, conforme o art. 45 da Lei 14.133. 
            A decisão de não os utilizar deve ser justificada nos autos."
            """)
            
            usa_sustentabilidade = st.radio(
                "Serão exigidos critérios de sustentabilidade nesta contratação?",
                ("Sim", "Não"), horizontal=True, key="sust"
            )

            sust_criterios = ""
            sust_justificativa_nao = ""

            if usa_sustentabilidade == "Sim":
                sust_criterios = st.text_area("Descreva os critérios de sustentabilidade exigidos:", key="sust_sim")
            else:
                sust_justificativa_nao = st.text_area("Apresente a justificativa formal para a não utilização de critérios de sustentabilidade:", key="sust_nao")

            # Botão de submissão
            submitted = st.form_submit_button("Analisar e Gerar Documento")

            if submitted:
                st.subheader("3. Análise de Conformidade e Geração do Documento")
                relatorio_analise = []
                documento_final = ""

                # --- Lógica de Análise Refinada ---
                if len(objeto_desc) < 50:
                    relatorio_analise.append({"nivel": "ALERTA", "item": "Objeto", "apontamento": "Descrição do objeto parece sucinta."})
                
                if len(justificativa_desc) < 150:
                    relatorio_analise.append({"nivel": "CRÍTICO", "item": "Justificativa", "apontamento": "A justificativa da necessidade deve ser robusta e detalhada."})

                # Análise da lógica de sustentabilidade
                if usa_sustentabilidade == 'Não' and len(sust_justificativa_nao) < 50:
                    relatorio_analise.append({
                        "nivel": "CRÍTICO",
                        "item": "Sustentabilidade",
                        "apontamento": "A não utilização de critérios de sustentabilidade exige justificativa formal e fundamentada, que não foi preenchida ou é insuficiente.",
                        "recomendacao": "Elabore uma justificativa detalhada para a não aplicação de critérios de sustentabilidade, conforme exigem a Lei 14.133 e a jurisprudência do TCU."
                    })
                
                # --- Exibição da Análise ---
                if not relatorio_analise:
                    st.success("✅ **Análise Concluída:** Nenhum ponto crítico foi identificado.")
                else:
                    st.error(f"🚨 **Análise Concluída:** Foram encontrados {len(relatorio_analise)} apontamentos.")
                    for apontamento in relatorio_analise:
                        st.markdown(f"**[{apontamento['nivel']}] - {apontamento['item']}:** {apontamento['apontamento']}")
                
                # --- Geração do Documento Final ---
                documento_final += f"2. OBJETO\n{objeto_desc}\n\n"
                documento_final += f"3. JUSTIFICATIVA\n{justificativa_desc}\n\n"
                documento_final += "4. CRITÉRIOS DE SUSTENTABILIDADE\n"
                if usa_sustentabilidade == "Sim":
                    documento_final += f"Serão aplicados os seguintes critérios de sustentabilidade: {sust_criterios}\n"
                else:
                    documento_final += f"Não serão aplicados critérios de sustentabilidade, conforme justificativa a seguir: {sust_justificativa_nao}\n"
                
                st.download_button("📥 Baixar Termo de Referência (.txt)", documento_final, f"TR_{datetime.now().strftime('%Y%m%d')}.txt")

# --- FASE 2 e 3 ---
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    st.info("Em breve: Construtor Guiado do Edital.")

with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Em breve: Construtor Guiado para Termos Aditivos.")
