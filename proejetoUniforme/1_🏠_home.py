import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Análise de Pedidos de Uniforme",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de tema e estilo
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #9caf88;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal com ícone
st.title('👔 Dashboard de Pedidos de Uniforme')
st.markdown('Sistema de análise e visualização de dados de pedidos de uniforme')

# Carregamento dos dados


@st.cache_data
def carregar_dados():
    try:
        # "C:/Cursos/Asimov/Streamlit/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/proejetoUniforme/dataset/UNIFORME.csv")
        pathFile = os.path.join("dataset", "UNIFORME.csv")
        df = pd.read_csv(pathFile)
        df['DATA_SAIDA'] = pd.to_datetime(df['DATA_SAIDA'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {str(e)}")
        return None


df = carregar_dados()

if df is not None:
    # Sidebar com filtros
    st.sidebar.title('Filtros')

    # Filtro de período
    st.sidebar.subheader('Período')
    data_inicial = st.sidebar.date_input(
        'Data Inicial', df['DATA_SAIDA'].min())
    data_final = st.sidebar.date_input('Data Final', df['DATA_SAIDA'].max())

    # Filtros de seleção múltipla
    secoes = st.sidebar.multiselect(
        'Seções', options=sorted(df['SECAO'].unique()))
    colaboradores = st.sidebar.multiselect(
        'Colaboradores', options=sorted(df['COLABORADOR'].unique()))

    # Aplicando filtros
    mask = (df['DATA_SAIDA'].dt.date >= data_inicial) & (
        df['DATA_SAIDA'].dt.date <= data_final)
    if secoes:
        mask &= df['SECAO'].isin(secoes)
    if colaboradores:
        mask &= df['COLABORADOR'].isin(colaboradores)

    df_filtrado = df[mask]

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Pedidos", f"{len(df_filtrado):,}")
    with col2:
        valor_total = df_filtrado['VALOR'].sum()
        st.metric("Valor Total", f"R$ {valor_total:,.2f}")
    with col3:
        qtd_total = df_filtrado[['QUANTIDADE1',
                                 'QUANTIDADE2', 'QUANTIDADE3']].sum().sum()
        st.metric("Quantidade Total", f"{qtd_total:,}")
    with col4:
        media_valor = df_filtrado['VALOR'].mean()
        st.metric("Valor Médio", f"R$ {media_valor:,.2f}")

    # Abas para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(
        ["Análise por Seção", "Análise Temporal", "Detalhamento"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de barras - Top 10 seções por valor
            dados_secao = df_filtrado.groupby(
                'SECAO')['VALOR'].sum().nlargest(10)
            fig_secao = px.bar(
                dados_secao,
                title='Top 10 Seções por Valor Total',
                labels={'value': 'Valor Total (R$)', 'SECAO': 'Seção'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_secao.update_layout(showlegend=False)
            st.plotly_chart(fig_secao, use_container_width=True)

        with col2:
            # Gráfico de pizza - Distribuição de quantidades por seção
            dados_qtd = df_filtrado.groupby(
                'SECAO')[['QUANTIDADE1', 'QUANTIDADE2', 'QUANTIDADE3']].sum()
            dados_qtd['TOTAL'] = dados_qtd.sum(axis=1)
            dados_qtd = dados_qtd['TOTAL'].nlargest(10)
            fig_pizza = px.pie(
                values=dados_qtd.values,
                names=dados_qtd.index,
                title='Distribuição de Quantidades por Seção (Top 10)'
            )
            st.plotly_chart(fig_pizza, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de linha - Evolução temporal
            dados_tempo = df_filtrado.resample('M', on='DATA_SAIDA')[
                'VALOR'].sum().reset_index()
            fig_tempo = px.line(
                dados_tempo,
                x='DATA_SAIDA',
                y='VALOR',
                title='Evolução Mensal do Valor Total',
                labels={'VALOR': 'Valor Total (R$)', 'DATA_SAIDA': 'Data'}
            )
            st.plotly_chart(fig_tempo, use_container_width=True)

        with col2:
            # Gráfico de calor - Distribuição semanal
            df_filtrado['dia_semana'] = df_filtrado['DATA_SAIDA'].dt.day_name()
            df_filtrado['mes'] = df_filtrado['DATA_SAIDA'].dt.month_name()

            dados_heatmap = pd.crosstab(
                df_filtrado['dia_semana'],
                df_filtrado['mes'],
                values=df_filtrado['VALOR'],
                aggfunc='sum'
            )

            fig_heatmap = px.imshow(
                dados_heatmap,
                title='Mapa de Calor: Distribuição de Valores por Dia e Mês',
                labels={'color': 'Valor Total (R$)'}
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            # Top requisitantes
            dados_req = df_filtrado.groupby('REQUISITANTE')[
                'VALOR'].sum().nlargest(10)
            fig_req = px.bar(
                dados_req,
                title='Top 10 Requisitantes por Valor',
                labels={
                    'value': 'Valor Total (R$)', 'REQUISITANTE': 'Requisitante'},
                color_discrete_sequence=['#2ecc71']
            )
            st.plotly_chart(fig_req, use_container_width=True)

        with col2:
            # Análise de motivos
            dados_motivos = df_filtrado['MOTIVO'].value_counts().nlargest(10)
            fig_motivos = px.pie(
                values=dados_motivos.values,
                names=dados_motivos.index,
                title='Principais Motivos dos Pedidos'
            )
            st.plotly_chart(fig_motivos, use_container_width=True)

        # Tabela detalhada
        st.subheader('Dados Detalhados')
        st.dataframe(
            df_filtrado.style.format({
                'VALOR': 'R$ {:,.2f}',
                'QUANTIDADE1': '{:,.0f}',
                'QUANTIDADE2': '{:,.0f}',
                'QUANTIDADE3': '{:,.0f}'
            }),
            height=400
        )

        # Download dos dados filtrados
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Download dos dados filtrados",
            data=csv,
            file_name="dados_uniformes_filtrados.csv",
            mime="text/csv"
        )
else:
    st.warning(
        "Por favor, verifique se o arquivo CSV está no formato correto e contém todas as colunas necessárias.")
