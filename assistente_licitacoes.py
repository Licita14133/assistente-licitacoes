import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 4.0 - Auditor Proativo")
st.caption("Análise de conformidade e geração de relatório para a contratação pública.")

# --- Estrutura de Abas ---
tab1, tab2, tab3 = st.tabs(["Fase 1: Planejamento", "Fase 2: Seleção do Fornecedor", "Fase 3: Gestão do Contrato"])

# --- FASE 1: PLANEJAMENTO ---
with tab1:
    st.header("Análise de Conformidade da Fase Preparatória")
    st.info("Preencha os itens abaixo. Ao final, gere um relatório de análise com apontamentos e recomendações.")

    with st.container(border=True):
        st.subheader("Documento de Formalização da Demanda (DFD) e ETP")
        
        # Usamos o session_state para guardar o estado dos checkboxes
        st.checkbox("A autoridade competente autorizou formalmente a abertura do processo?", key="p1")
        st.checkbox("A necessidade da contratação está justificada, com base no interesse público?", key="p2")
        st.checkbox("Os requisitos da contratação (quantidades, prazos, especificações) estão claros e tecnicamente fundamentados no ETP/TR?", key="p3")
        st.checkbox("O levantamento de mercado analisou e comparou diferentes soluções para atender à necessidade?", key="p4")
        st.checkbox("A estimativa de valor da contratação foi baseada em pesquisa de mercado ampla e documentada?", key="p5")
        st.checkbox("A Declaração de Disponibilidade Orçamentária (DDO) foi emitida e anexada ao processo?", key="p6")
    
    st.write("---")

    # Botão para gerar a análise
    if st.button("Gerar Análise de Conformidade da Fase de Planejamento", type="primary"):
        apontamentos = []

        # Lógica de Análise
        if not st.session_state.p1:
            apontamentos.append({
                "nivel": "CRÍTICO",
                "item": "Autorização da Autoridade Competente",
                "fundamentacao": "A ausência de autorização formal para iniciar a contratação fere o princípio da legalidade e pode invalidar todo o processo (Art. 18, Lei 14.133).",
                "recomendacao": "Providenciar o despacho de autorização da autoridade competente e juntá-lo aos autos."
            })
        if not st.session_state.p2:
            apontamentos.append({
                "nivel": "CRÍTICO",
                "item": "Justificativa da Necessidade",
                "fundamentacao": "A justificativa da necessidade é o pilar da contratação e requisito obrigatório do ETP (Art. 18, § 1º, I, Lei 14.133).",
                "recomendacao": "Detalhar no ETP/TR a motivação e o interesse público que fundamentam a contratação, sob pena de nulidade."
            })
        if not st.session_state.p3:
            apontamentos.append({
                "nivel": "CRÍTICO",
                "item": "Requisitos da Contratação",
                "fundamentacao": "A definição imprecisa dos requisitos impede a formulação de propostas adequadas e a correta execução do objeto (Art. 6º, XXIII, 'd', Lei 14.133).",
                "recomendacao": "Revisar o ETP/TR para garantir que todos os requisitos, quantidades e especificações do objeto estejam claros e bem definidos."
            })
        if not st.session_state.p5:
            apontamentos.append({
                "nivel": "ALERTA",
                "item": "Pesquisa de Mercado",
                "fundamentacao": "Uma pesquisa de preços deficiente ou mal documentada pode levar a contratações com sobrepreço e ser questionada pelos órgãos de controle (Art. 23, Lei 14.133).",
                "recomendacao": "Garantir que a pesquisa de preços foi ampla, utilizando diversas fontes (conforme IN aplicável), e que toda a documentação comprobatória está nos autos."
            })
        if not st.session_state.p6:
            apontamentos.append({
                "nivel": "CRÍTICO",
                "item": "Disponibilidade Orçamentária (DDO)",
                "fundamentacao": "Nenhuma contratação pode ser realizada sem a prévia indicação de recursos orçamentários para fazer face à despesa (Art. 16, I, LRF e Art. 18, IV, Lei 14.133).",
                "recomendacao": "Solicitar e anexar ao processo a Declaração de Disponibilidade Orçamentária (DDO) emitida pelo setor competente."
            })

        st.subheader("Resultado da Análise")

        # Exibindo o relatório na tela
        if not apontamentos:
            st.success("✅ **Análise Concluída:** Nenhum ponto crítico ou de alerta foi identificado. A fase preparatória parece estar em conformidade.")
            texto_relatorio = "Análise Concluída: Nenhum ponto crítico ou de alerta foi identificado."
        else:
            st.error(f"🚨 **Análise Concluída:** Foram encontrados {len(apontamentos)} apontamentos. É necessário revisar os itens abaixo.")
            
            texto_relatorio = f"RELATÓRIO DE ANÁLISE DE CONFORMIDADE - FASE DE PLANEJAMENTO\n"
            texto_relatorio += f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            texto_relatorio += "="*80 + "\n\n"

            for apontamento in apontamentos:
                cor = "red" if apontamento["nivel"] == "CRÍTICO" else "orange"
                st.markdown(f"<p style='color:{cor};'><strong>[{apontamento['nivel']}] - {apontamento['item']}</strong></p>", unsafe_allow_html=True)
                st.markdown(f"**Fundamentação:** {apontamento['fundamentacao']}")
                st.markdown(f"**Recomendação:** {apontamento['recomendacao']}")
                st.write("---")

                # Montando o texto para o arquivo de download
                texto_relatorio += f"[{apontamento['nivel']}] - {apontamento['item']}\n"
                texto_relatorio += f"  - Fundamentação: {apontamento['fundamentacao']}\n"
                texto_relatorio += f"  - Recomendação: {apontamento['recomendacao']}\n\n"

            # Botão para download do relatório
            st.download_button(
                label="📥 Baixar Relatório de Apontamentos (.txt)",
                data=texto_relatorio,
                file_name=f"Relatorio_Conformidade_Planejamento_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# --- FASE 2 e 3 (mantemos a estrutura, mas o foco do refinamento foi na Fase 1) ---
with tab2:
    st.header("Módulos da Fase de Seleção do Fornecedor")
    st.write("Módulos de análise do Edital e Habilitação serão refinados em breve.")

with tab3:
    st.header("Módulos da Fase de Gestão Contratual")
    st.write("Módulos de Repactuação e Apostilamento serão refinados em breve.")
