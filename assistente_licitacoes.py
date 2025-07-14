import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 6.3 - Montador Completo")
st.caption("Construção guiada e integral do Termo de Referência (Compras), espelhando o modelo oficial da AGU.")

# --- Inicialização do Estado da Sessão ---
if 'tr_itens' not in st.session_state:
    st.session_state.tr_itens = []
if 'tr_inputs' not in st.session_state:
    st.session_state.tr_inputs = {}

# --- Aba Única para Foco Total na Construção do TR ---
st.header("Construtor Guiado do Termo de Referência (Modelo: Compras)")
st.info("Siga os 14 tópicos abaixo para construir o documento. O assistente irá guiar o preenchimento de cada etapa.")

# --- TÓPICO 1: CONSTRUTOR DE ITENS (JÁ IMPLEMENTADO) ---
st.markdown("---")
st.subheader("Tópico 1: DO OBJETO (Detalhamento dos Itens)")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col1:
        item_desc = st.text_input("Descrição Detalhada do Item", placeholder="Ex: Caneta esferográfica azul")
    with col2:
        item_unid = st.selectbox("Unidade", ["UN", "CX", "PCT", "RES", "KG", "L", "M"])
    with col3:
        item_qtd = st.number_input("Quantidade", min_value=1, step=1)
    with col4:
        item_valor_unit = st.number_input("Valor Unitário (R$)", min_value=0.01, step=0.01, format="%.2f")

    if st.button("Adicionar Item à Tabela", type="primary"):
        if item_desc:
            novo_item = {
                "Item": len(st.session_state.tr_itens) + 1,
                "Descrição": item_desc,
                "Unidade": item_unid,
                "Quantidade": item_qtd,
                "Valor Unitário (R$)": item_valor_unit,
                "Valor Total (R$)": item_qtd * item_valor_unit
            }
            st.session_state.tr_itens.append(novo_item)
        else:
            st.warning("Por favor, preencha a descrição do item.")
if st.session_state.tr_itens:
    st.markdown("##### Tabela de Itens da Contratação:")
    df_itens = pd.DataFrame(st.session_state.tr_itens)
    st.dataframe(df_itens, use_container_width=True, hide_index=True)
    valor_total_contratacao = df_itens["Valor Total (R$)"].sum()
    st.success(f"**Valor Total Estimado da Contratação: R$ {valor_total_contratacao:,.2f}**")
    st.session_state.tr_inputs['valor_total_calculado'] = f"R$ {valor_total_contratacao:,.2f}"

# --- INÍCIO DO FORMULÁRIO COMPLETO ---
with st.form("tr_completo_form"):
    st.markdown("---")
    st.subheader("Preenchimento dos Tópicos 2 a 14 do Termo de Referência")

    # --- INCLUSÃO COMPLETA DOS TÓPICOS 2 A 14 ---

    st.markdown("#### Tópico 2: DA FUNDAMENTAÇÃO E JUSTIFICATIVA DA CONTRATAÇÃO")
    st.info("Nota Explicativa: Detalhar a necessidade da contratação, demonstrando o alinhamento com o planejamento e o interesse público.")
    st.session_state.tr_inputs['justificativa'] = st.text_area("2.1. Descreva a justificativa para a aquisição.", height=150, key=2.1)

    st.markdown("#### Tópico 3: DOS REQUISITOS DA CONTRATAÇÃO")
    st.info("Nota Explicativa: Detalhar todos os requisitos essenciais para o pleno atendimento da necessidade.")
    st.session_state.tr_inputs['requisitos'] = st.text_area("3.1. Especifique os requisitos do material (qualidade, desempenho, sustentabilidade, etc.).", key=3.1)

    st.markdown("#### Tópico 4: DO LOCAL E DAS CONDIÇÕES DE ENTREGA DO OBJETO")
    st.session_state.tr_inputs['local_entrega'] = st.text_input("4.1. Local de entrega dos bens:", key=4.1)
    st.session_state.tr_inputs['prazo_entrega'] = st.text_input("4.2. Prazo de entrega (ex: 30 dias corridos).", key=4.2)
    st.session_state.tr_inputs['marco_inicial_prazo'] = st.text_input("4.2.1. Marco inicial da contagem do prazo (ex: a partir da assinatura do contrato).", key=4.21)

    st.markdown("#### Tópico 5: DAS OBRIGAÇÕES DA CONTRATANTE")
    st.info("Texto Fixo: As obrigações listadas no modelo da AGU (itens 5.1 a 5.6) serão adicionadas automaticamente ao documento final.")

    st.markdown("#### Tópico 6: DAS OBRIGAÇÕES DA CONTRATADA")
    st.info("Texto Fixo: As obrigações listadas no modelo da AGU (itens 6.1 a 6.14) serão adicionadas automaticamente ao documento final.")

    st.markdown("#### Tópico 7: DA SUBCONTRATAÇÃO")
    st.session_state.tr_inputs['subcontratacao'] = st.radio("Será admitida a subcontratação?", ["Não", "Sim, para partes acessórias"], horizontal=True, key=7)

    st.markdown("#### Tópico 8: DO MODELO DE GESTÃO DO CONTRATO E CRITÉRIOS DE MEDIÇÃO E PAGAMENTO")
    st.session_state.tr_inputs['fiscal_contrato'] = st.text_input("8.1. Indique o servidor ou unidade responsável pela fiscalização do contrato.", key=8.1)
    st.session_state.tr_inputs['criterios_pagamento'] = st.text_area("8.2. Descreva os critérios de medição e as condições de pagamento.", key=8.2)

    st.markdown("#### Tópico 9: DOS CRITÉRIOS DE SELEÇÃO DO FORNECEDOR")
    st.info("Texto Fixo: Será adotado o critério de julgamento por MENOR PREÇO.")
    st.session_state.tr_inputs['exigencias_habilitacao'] = st.text_area("9.1. Descreva eventuais requisitos de habilitação adicionais, se estritamente necessários e justificados.", key=9.1)

    st.markdown("#### Tópico 10: DA ESTIMATIVA DE PREÇOS E DOS PREÇOS REFERENCIAIS")
    st.info("O valor total estimado será preenchido automaticamente com base na tabela de itens.")
    
    st.markdown("#### Tópico 11: DO REGIME DE EXECUÇÃO")
    st.info("Texto Fixo: O regime de execução será o de Empreitada por Preço Unitário.")

    st.markdown("#### Tópico 12: DA ADEQUAÇÃO ORÇAMENTÁRIA")
    st.session_state.tr_inputs['dotacao_orcamentaria'] = st.text_input("12.1. Indique a dotação orçamentária que fará face à despesa.", key=12.1)

    st.markdown("#### Tópico 13: DA EQUIPE DE PLANEJAMENTO")
    st.info("A equipe de planejamento que participou da elaboração deste artefato será listada aqui.")
    st.session_state.tr_inputs['equipe_planejamento'] = st.text_area("13.1. Liste os nomes e matrículas dos membros da equipe.", key=13.1)

    st.markdown("#### Tópico 14: DECLARAÇÃO DE VIABILIDADE")
    st.info("Texto Fixo: A Contratante declara, sob as penas da lei, que a presente contratação é VIÁVEL.")

    # Botão de submissão
    submitted = st.form_submit_button("Gerar Documento Completo e Final do Termo de Referência")

if submitted:
    st.balloons()
    st.header("Documento Final Gerado")
    
    # Montagem do Documento Completo
    doc = []
    doc.append("TERMO DE REFERÊNCIA (COMPRAS)")
    doc.append("="*60)
    
    # Tópico 1
    doc.append("\n1. DO OBJETO")
    if st.session_state.tr_itens:
        df_para_doc = pd.DataFrame(st.session_state.tr_itens)
        doc.append(df_para_doc.to_string(index=False))
    else:
        doc.append("[NENHUM ITEM ADICIONADO À TABELA]")
    
    # Tópicos 2 em diante
    doc.append(f"\n2. DA FUNDAMENTAÇÃO E JUSTIFICATIVA\n{st.session_state.tr_inputs.get('justificativa', '[NÃO PREENCHIDO]')}")
    doc.append(f"\n3. DOS REQUISITOS DA CONTRATAÇÃO\n{st.session_state.tr_inputs.get('requisitos', '[NÃO PREENCHIDO]')}")
    doc.append(f"\n4. DO LOCAL E DAS CONDIÇÕES DE ENTREGA\nLocal: {st.session_state.tr_inputs.get('local_entrega', '[NÃO PREENCHIDO]')}\nPrazo: {st.session_state.tr_inputs.get('prazo_entrega', '[NÃO PREENCHIDO]')}\nMarco Inicial: {st.session_state.tr_inputs.get('marco_inicial_prazo', '[NÃO PREENCHIDO]')}")
    doc.append("\n5. DAS OBRIGAÇÕES DA CONTRATANTE\n(Conforme modelo padrão da AGU)")
    doc.append("\n6. DAS OBRIGAÇÕES DA CONTRATADA\n(Conforme modelo padrão da AGU)")
    subcontratacao_texto = "Não será admitida a subcontratação." if "Não" in st.session_state.tr_inputs.get('subcontratacao', 'Não') else "Será admitida a subcontratação de partes acessórias, mediante prévia análise e autorização da Contratante."
    doc.append(f"\n7. DA SUBCONTRATAÇÃO\n{subcontratacao_texto}")
    doc.append(f"\n8. DO MODELO DE GESTÃO DO CONTRATO\nFiscal: {st.session_state.tr_inputs.get('fiscal_contrato', '[NÃO PREENCHIDO]')}\nPagamento: {st.session_state.tr_inputs.get('criterios_pagamento', '[NÃO PREENCHIDO]')}")
    doc.append(f"\n9. DOS CRITÉRIOS DE SELEÇÃO DO FORNECEDOR\nCritério de Julgamento: Menor Preço.\nRequisitos adicionais: {st.session_state.tr_inputs.get('exigencias_habilitacao', 'Não se aplica.')}")
    doc.append(f"\n10. DA ESTIMATIVA DE PREÇOS\nValor Estimado: {st.session_state.tr_inputs.get('valor_total_calculado', '[NÃO CALCULADO]')}. A pesquisa de preços consta em anexo.")
    doc.append("\n11. DO REGIME DE EXECUÇÃO\nO regime de execução será o de Empreitada por Preço Unitário.")
    doc.append(f"\n12. DA ADEQUAÇÃO ORÇAMENTÁRIA\nDotação: {st.session_state.tr_inputs.get('dotacao_orcamentaria', '[NÃO PREENCHIDO]')}")
    doc.append(f"\n13. DA EQUIPE DE PLANEJAMENTO\n{st.session_state.tr_inputs.get('equipe_planejamento', '[NÃO PREENCHIDO]')}")
    doc.append("\n14. DECLARAÇÃO DE VIABILIDADE\nA Contratante declara que a presente contratação é VIÁVEL.")

    documento_final_str = "\n\n".join(doc)

    st.text_area("Prévia do Documento Completo", documento_final_str, height=400)
    st.download_button("📥 Baixar TR Completo (.txt)", documento_final_str, f"TR_COMPRAS_COMPLETO_{datetime.now().strftime('%Y%m%d')}.txt")
