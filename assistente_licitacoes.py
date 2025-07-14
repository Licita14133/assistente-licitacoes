import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 5.0 - Construtor Guiado")
st.caption("Uma ferramenta especialista para a construção e análise de artefatos de contratação.")

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento (ETP/TR)", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: PLANEJAMENTO (Totalmente remodelada) ---
with tab1:
    st.header("Construtor Guiado do Estudo Técnico Preliminar e Termo de Referência")
    st.info("Responda às perguntas e preencha os campos para construir seu documento. O assistente fará análises e recomendações em tempo real.")

    # --- Perguntas de Contexto para Definir o Escopo ---
    st.subheader("1. Definição do Escopo da Contratação")
    tipo_objeto = st.selectbox("Qual é a natureza do objeto?", ["Serviços", "Compras"])
    
    if tipo_objeto == "Serviços":
        dedicacao_mo = st.radio(
            "O serviço envolve dedicação exclusiva de mão de obra?",
            ("Sim", "Não"), horizontal=True
        )

    # --- Formulário para Construção do Documento ---
    with st.form("etp_tr_form"):
        st.subheader("2. Preenchimento Guiado do Documento")

        # Seção 2 do TR: Descrição do Objeto
        st.markdown("##### Item 2: Objeto da Contratação")
        objeto_desc = st.text_area("Descreva o objeto da contratação de forma precisa, suficiente e clara. Evite o uso de marcas.", height=100)

        # Seção 3 do TR: Justificativa e Necessidade
        st.markdown("##### Item 3: Justificativa e Necessidade")
        justificativa_desc = st.text_area("Detalhe a necessidade da contratação, o problema a ser resolvido e o interesse público envolvido.", height=150)
        
        # O botão de submissão do formulário
        submitted = st.form_submit_button("Analisar e Gerar Documento")

        if submitted:
            st.subheader("3. Análise de Conformidade e Geração do Documento")
            
            relatorio_analise = []
            documento_final = ""

            # --- Lógica de Análise ---
            # Análise do Objeto
            marcas_vedadas = ['dell', 'hp', 'microsoft', 'adobe', 'x-brand'] # Lista de exemplo
            if any(marca in objeto_desc.lower() for marca in marcas_vedadas):
                relatorio_analise.append({
                    "nivel": "CRÍTICO",
                    "item": "Descrição do Objeto",
                    "apontamento": "Foi identificada a menção a uma marca específica. A indicação de marca é vedada, exceto em casos excepcionais e justificados (Art. 41, I, Lei 14.133).",
                    "recomendacao": "Substitua a marca por especificações técnicas neutras e detalhadas que garantam a qualidade desejada sem restringir a competição."
                })
            elif len(objeto_desc) < 50:
                 relatorio_analise.append({
                    "nivel": "ALERTA",
                    "item": "Descrição do Objeto",
                    "apontamento": "A descrição do objeto parece muito sucinta.",
                    "recomendacao": "Considere detalhar mais as especificações para garantir que os licitantes compreendam perfeitamente o que está sendo solicitado."
                })
            
            # Análise da Justificativa
            if len(justificativa_desc) < 150:
                relatorio_analise.append({
                    "nivel": "CRÍTICO",
                    "item": "Justificativa da Necessidade",
                    "apontamento": "A justificativa é o pilar da contratação. Uma descrição com menos de 150 caracteres pode ser considerada insuficiente pelos órgãos de controle.",
                    "recomendacao": "Detalhe o problema a ser resolvido, os resultados esperados e como a contratação se alinha ao planejamento do órgão (Art. 18, § 1º, I)."
                })

            # --- Exibição da Análise na Tela ---
            if not relatorio_analise:
                st.success("✅ **Análise Concluída:** Nenhum ponto de atenção foi identificado nos campos preenchidos.")
            else:
                st.error(f"🚨 **Análise Concluída:** Foram encontrados {len(relatorio_analise)} apontamentos. Revise os itens abaixo:")
                for apontamento in relatorio_analise:
                    cor = "red" if apontamento["nivel"] == "CRÍTICO" else "orange"
                    st.markdown(f"<p style='color:{cor};'><strong>[{apontamento['nivel']}] - {apontamento['item']}</strong></p>", unsafe_allow_html=True)
                    st.markdown(f"**Apontamento:** {apontamento['apontamento']}")
                    st.markdown(f"**Recomendação:** {apontamento['recomendacao']}")
                    st.write("---")

            # --- Geração do Documento Final para Download ---
            documento_final += "TERMO DE REFERÊNCIA (Versão Preliminar)\n"
            documento_final += "="*40 + "\n\n"
            documento_final += "1. OBJETO DA CONTRATAÇÃO\n"
            documento_final += f"{objeto_desc}\n\n"
            documento_final += "2. JUSTIFICATIVA E NECESSIDADE DA CONTRATAÇÃO\n"
            documento_final += f"{justificativa_desc}\n\n"
            
            # Adiciona cláusula condicional baseada nas perguntas de contexto
            if tipo_objeto == "Serviços" and dedicacao_mo == "Sim":
                documento_final += "3. MODELO DE GESTÃO DO CONTRATO (Serviços com M.O. Exclusiva)\n"
                documento_final += "[Detalhar aqui as regras de fiscalização para serviços com dedicação de mão de obra...]\n"

            st.download_button(
                label="📥 Baixar Documento Preliminar (.txt)",
                data=documento_final,
                file_name=f"TR_Preliminar_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )


# --- FASE 2 e 3 (mantemos a estrutura para desenvolvimento futuro) ---
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    st.info("Em breve: Construtor Guiado do Edital e do Aviso de Contratação.")

with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.info("Em breve: Construtor Guiado para Termos Aditivos e de Apostilamento.")
