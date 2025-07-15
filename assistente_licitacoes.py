import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(layout="wide")
st.title("Assistente de Licitações 8.1 - Estrutura Completa")
st.caption("Ferramenta especialista com as 3 fases do processo de contratação.")

# --- Carregamento e Cache dos Catálogos ---
@st.cache_data
def load_data():
    try:
        df1 = pd.read_csv("catmat 1.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        df2 = pd.read_csv("catmat 2.csv", sep=';', encoding='latin1', low_memory=False, on_bad_lines='skip')
        catmat_df = pd.concat([df1, df2], ignore_index=True)
        catser_df = pd.read_csv("catser.csv", sep=';', encoding='latin1', low_memory=False)
        
        catmat_df.columns = catmat
