import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set(style="whitegrid")
palette = sns.color_palette("Set2")

@st.cache_data
def carregar_dados(ano):
    arquivo = f"DADO_{ano}.csv" 

    df = pd.read_csv(arquivo, encoding='ISO-8859-1').drop("Unnamed: 0", axis=1)
    return df

def tratar_dados(df):
    df['SG_UF_ESC'] = df['SG_UF_ESC'].fillna('ND')
    df['TP_COR_RACA'] = df['TP_COR_RACA'].fillna(-1).replace(0, -1,)
    media_nota_mt = df['NU_NOTA_MT'].mean()
    df['NU_NOTA_MT'] = df['NU_NOTA_MT'].replace(0, media_nota_mt)
    df['NU_NOTA_MT'] = df['NU_NOTA_MT'].fillna(media_nota_mt)
    mediana_faixa_etaria = df['TP_FAIXA_ETARIA'].median()
    df['TP_FAIXA_ETARIA'] = df['TP_FAIXA_ETARIA'].replace(0, mediana_faixa_etaria)
    df['TP_FAIXA_ETARIA'] = df['TP_FAIXA_ETARIA'].fillna(mediana_faixa_etaria)
    valor_frequente_tp_ensino = df['TP_ENSINO'].mode()[0]
    df['TP_ENSINO'] = df['TP_ENSINO'].fillna(valor_frequente_tp_ensino)
    df['TP_ENSINO'] = df['TP_ENSINO'].replace(0, 3)
    df['TP_PRESENCA_MT'] = df['TP_PRESENCA_MT'].fillna(-1)
    return df

st.title("Dashboard de Médias de Matemática no ENEM (2018-2023)")
st.markdown("Análise detalhada das médias de Matemática por estado, raça, tipo de escola e média nacional")

ano_selecionado = st.sidebar.selectbox("Selecione o Ano", [2018, 2019, 2020, 2021, 2022, 2023])

df_ano = carregar_dados(ano_selecionado)
#df_ano = tratar_dados(df_ano)

analise = st.sidebar.radio("Escolha a Análise", ("Média Nacional", "Média por Estado", "Média por Raça", "Média por Tipo de Escola"))

if analise == "Média Nacional":
    media_nacional = df_ano['NU_NOTA_MT'].mean()
    st.subheader(f"Média Nacional de Matemática - {ano_selecionado}")
    st.write(f"Média Nacional: {media_nacional:.2f}")

elif analise == "Média por Estado":
    st.subheader("Média de Matemática por Estado")
    media_estado = df_ano.groupby('SG_UF_ESC')['NU_NOTA_MT'].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='NU_NOTA_MT', y='SG_UF_ESC', data=media_estado, ax=ax1, palette=palette)
    ax1.set_title(f"Média de Matemática por Estado - {ano_selecionado}")
    ax1.set_xlabel("Média")
    ax1.set_ylabel("Estado")
    ax1.legend(['Média de Matemática'])
    st.pyplot(fig1)

elif analise == "Média por Raça":
    st.subheader("Média de Matemática por Raça")
    media_raca = df_ano.groupby('TP_COR_RACA')['NU_NOTA_MT'].mean().reset_index()
    fig2, ax2 = plt.subplots()
    sns.barplot(x='TP_COR_RACA', y='NU_NOTA_MT', data=media_raca, ax=ax2, palette=palette)
    ax2.set_title(f"Média de Matemática por Raça - {ano_selecionado}")
    ax2.set_xlabel("Raça")
    ax2.set_ylabel("Média")
    ax2.legend(['Média de Matemática'])
    st.pyplot(fig2)

elif analise == "Média por Tipo de Escola":
    st.subheader("Média de Matemática por Tipo de Escola (Pública vs. Particular)")
    media_escola = df_ano.groupby('TP_ENSINO')['NU_NOTA_MT'].mean().reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(x='TP_ENSINO', y='NU_NOTA_MT', data=media_escola, ax=ax3, palette=palette)
    ax3.set_title(f"Média de Matemática por Tipo de Escola - {ano_selecionado}")
    ax3.set_xlabel("Tipo de Escola")
    ax3.set_ylabel("Média")
    ax3.legend(['Média de Matemática'])
    st.pyplot(fig3)
