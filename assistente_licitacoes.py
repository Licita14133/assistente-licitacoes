import streamlit as st
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 6.1 - Montador de Alta Fidelidade")
st.caption("Construção guiada do Termo de Referência (Compras), espelhando o modelo oficial da AGU.")

# --- Inicialização do Estado da Sessão ---
if 'tr' not in st.session_state:
    st.session_state.tr = {}

# --- Aba Única para Foco Total na Construção do TR ---
st.header("Construtor Guiado do Termo de Referência (Modelo: Compras)")
st.info("Siga os 14 tópicos abaixo, baseados no modelo oficial da AGU. Preencha apenas os campos editáveis.")

with st.form("tr_completo_form"):
    # --- Tópicos do Termo de Referência ---
    
    st.markdown("---")
    st.subheader("Tópico 1: DO OBJETO")
    st.info("Nota Explicativa: Descrever o objeto de forma precisa, sem especificações excessivas ou direcionamento de marca.")
    st.session_state.tr['objeto'] = st.text_area("1.1. Especifique aqui o objeto da contratação (Ex: Aquisição de material de escritório).", key=1.1)

    st.markdown("---")
    st.subheader("Tópico 2: DA FUNDAMENTAÇÃO E JUSTIFICATIVA DA CONTRATAÇÃO")
    st.info("Nota Explicativa: Detalhar a necessidade da contratação, demonstrando o alinhamento com o planejamento e o interesse público.")
    st.session_state.tr['justificativa'] = st.text_area("2.1. Descreva a justificativa para a aquisição.", height=200, key=2.1)

    st.markdown("---")
    st.subheader("Tópico 3: DOS REQUISITOS DA CONTRATAÇÃO")
    st.info("Nota Explicativa: Detalhar todos os requisitos essenciais para o pleno atendimento da necessidade.")
    st.session_state.tr['requisitos'] = st.text_area("3.1. Especifique os requisitos do material/serviço (qualidade, desempenho, etc.).", key=3.1)
    
    st.markdown("---")
    st.subheader("Tópico 4: DO LOCAL E DAS CONDIÇÕES DE ENTREGA DO OBJETO")
    st.session_state.tr['local_entrega'] = st.text_input("4.1. Local de entrega dos bens:", key=4.1)
    st.session_state.tr['prazo_entrega'] = st.text_input("4.2. Prazo de entrega (ex: 30 dias corridos).", key=4.2)
    st.session_state.tr['marco_inicial_prazo'] = st.text_input("4.2.1. Marco inicial da contagem do prazo (ex: a partir da assinatura do contrato).", key=4.21)

    st.markdown("---")
    st.subheader("Tópico 5: DAS OBRIGAÇÕES DA CONTRATANTE")
    st.info("Texto Fixo: As obrigações listadas no modelo da AGU (itens 5.1 a 5.6) serão adicionadas automaticamente ao documento final.")

    st.markdown("---")
    st.subheader("Tópico 6: DAS OBRIGAÇÕES DA CONTRATADA")
    st.info("Texto Fixo: As obrigações listadas no modelo da AGU (itens 6.1 a 6.14) serão adicionadas automaticamente ao documento final.")

    st.markdown("---")
    st.subheader("Tópico 7: DA SUBCONTRATAÇÃO")
    st.info("Nota Explicativa: A subcontratação é vedada para o objeto principal. Indique se será permitida para partes acessórias.")
    st.session_state.tr['subcontratacao'] = st.radio("Será admitida a subcontratação de partes acessórias?", ["Não", "Sim"], horizontal=True, key=7)

    st.markdown("---")
    st.subheader("Tópico 8: DO MODELO DE GESTÃO DO CONTRATO E CRITÉRIOS DE MEDIÇÃO E PAGAMENTO")
    st.session_state.tr['fiscal_contrato'] = st.text_input("8.1. Indique o servidor ou unidade responsável pela fiscalização do contrato.", key=8.1)
    st.session_state.tr['criterios_pagamento'] = st.text_area("8.2. Descreva os critérios de medição e as condições de pagamento.", key=8.2)

    st.markdown("---")
    st.subheader("Tópico 9: DOS CRITÉRIOS DE SELEÇÃO DO FORNECEDOR")
    st.info("Texto Fixo: Será adotado o critério de julgamento por MENOR PREÇO.")
    st.session_state.tr['exigencias_habilitacao'] = st.text_area("9.1. Descreva eventuais requisitos de habilitação adicionais, se estritamente necessários e justificados.", key=9.1)
    
    st.markdown("---")
    st.subheader("Tópico 10: DA ESTIMATIVA DE PREÇOS E DOS PREÇOS REFERENCIAIS")
    st.info("Nota Explicativa: O valor estimado deve ser anexado ao TR, com a devida pesquisa de preços que o fundamenta.")
    st.session_state.tr['valor_estimado'] = st.text_input("10.1. Informe o valor total estimado da contratação (Ex: R$ 15.000,00).", key=10.1)

    st.markdown("---")
    st.subheader("Tópico 11: DO REGIME DE EXECUÇÃO")
    st.info("Texto Fixo: O regime de execução será o de Empreitada por Preço Unitário.")

    st.markdown("---")
    st.subheader("Tópico 12: DA ADEQUAÇÃO ORÇAMENTÁRIA")
    st.session_state.tr['dotacao_orcamentaria'] = st.text_input("12.1. Indique a dotação orçamentária que fará face à despesa.", key=12.1)

    st.markdown("---")
    st.subheader("Tópico 13: DA EQUIPE DE PLANEJAMENTO")
    st.info("Texto Fixo: A equipe de planejamento foi composta pelos servidores listados no Despacho/Portaria [NÚMERO].")
    
    st.markdown("---")
    st.subheader("Tópico 14: DECLARAÇÃO DE VIABILIDADE")
    st.info("Texto Fixo: A Contratante declara que a contratação é VIÁVEL.")

    # Botão de submissão
    submitted = st.form_submit_button("Gerar Documento Completo do Termo de Referência")

if submitted:
    st.balloons()
    st.header("Documento Final Gerado")
    
    # Montagem do Documento Completo
    doc = []
    doc.append("TERMO DE REFERÊNCIA (COMPRAS)")
    doc.append("="*40)
    
    # Adicionando cada seção ao documento final
    doc.append(f"1. DO OBJETO\n1.1. {st.session_state.tr.get('objeto', '[NÃO PREENCHIDO]')}")
    doc.append(f"2. DA FUNDAMENTAÇÃO E JUSTIFICATIVA\n2.1. {st.session_state.tr.get('justificativa', '[NÃO PREENCHIDO]')}")
    doc.append(f"3. DOS REQUISITOS DA CONTRATAÇÃO\n3.1. {st.session_state.tr.get('requisitos', '[NÃO PREENCHIDO]')}")
    doc.append(f"4. DO LOCAL E DAS CONDIÇÕES DE ENTREGA\n4.1. Local: {st.session_state.tr.get('local_entrega', '[NÃO PREENCHIDO]')}\n4.2. Prazo: {st.session_state.tr.get('prazo_entrega', '[NÃO PREENCHIDO]')}\n4.2.1. Marco Inicial: {st.session_state.tr.get('marco_inicial_prazo', '[NÃO PREENCHIDO]')}")
    
    # Seções com texto fixo
    doc.append("5. DAS OBRIGAÇÕES DA CONTRATANTE\n(Conforme modelo padrão da AGU)")
    doc.append("6. DAS OBRIGAÇÕES DA CONTRATADA\n(Conforme modelo padrão da AGU)")
    
    # Seção condicional
    subcontratacao_texto = "Não será admitida a subcontratação." if st.session_state.tr.get('subcontratacao') == "Não" else "Será admitida a subcontratação de partes acessórias, mediante aprovação da Contratante."
    doc.append(f"7. DA SUBCONTRATAÇÃO\n7.1. {subcontratacao_texto}")
    
    doc.append(f"8. DO MODELO DE GESTÃO DO CONTRATO\n8.1. Fiscal: {st.session_state.tr.get('fiscal_contrato', '[NÃO PREENCHIDO]')}\n8.2. Pagamento: {st.session_state.tr.get('criterios_pagamento', '[NÃO PREENCHIDO]')}")
    doc.append(f"9. DOS CRITÉRIOS DE SELEÇÃO DO FORNECEDOR\n9.1. Critério de Julgamento: Menor Preço.\n9.2. Requisitos adicionais de habilitação: {st.session_state.tr.get('exigencias_habilitacao', 'Não se aplica.')}")
    doc.append(f"10. DA ESTIMATIVA DE PREÇOS\n10.1. Valor Estimado: {st.session_state.tr.get('valor_estimado', '[NÃO PREENCHIDO]')}. A pesquisa de preços consta em anexo.")
    doc.append("11. DO REGIME DE EXECUÇÃO\n11.1. O regime de execução será o de Empreitada por Preço Unitário.")
    doc.append(f"12. DA ADEQUAÇÃO ORÇAMENTÁRIA\n12.1. Dotação: {st.session_state.tr.get('dotacao_orcamentaria', '[NÃO PREENCHIDO]')}")
    doc.append("13. DA EQUIPE DE PLANEJAMENTO\n(Conforme ato de designação)")
    doc.append("14. DECLARAÇÃO DE VIABILIDADE\n14.1. A Contratante declara que a contratação é VIÁVEL.")

    documento_final_str = "\n\n".join(doc)

    st.text_area("Prévia do Documento Completo", documento_final_str, height=400)
    st.download_button("📥 Baixar TR Completo (.txt)", documento_final_str, f"TR_COMPRAS_{datetime.now().strftime('%Y%m%d')}.txt")
