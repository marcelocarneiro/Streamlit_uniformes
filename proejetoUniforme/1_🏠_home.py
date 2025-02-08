# from datetime import datetime

# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # Configuração inicial do Streamlit
# st.title("Análise de Dados de Uniformes")
# st.sidebar.header("Filtros e Opções")

# # Carregar dados do arquivo CSV
# df = pd.read_csv(df = pd.read_csv("/dataset/UNIFORME.csv")


# # Converter DATA_SAIDA para datetime, considerando o formato DD/MM/YYYY
# if "DATA_SAIDA" in df.columns:
#     try:
#         df["DATA_SAIDA"] = pd.to_datetime(
#             df["DATA_SAIDA"], format="%d/%m/%Y", errors="coerce")  # Especifica o formato
#     except Exception as e:
#         st.sidebar.error(f"Erro ao converter a coluna 'DATA_SAIDA': {e}")
#         df["DATA_SAIDA"] = None  # Define como nulo se houver erro
# else:
#     st.sidebar.warning(
#         "A coluna 'DATA_SAIDA' não foi encontrada no arquivo CSV.")
#     df["DATA_SAIDA"] = None  # Adiciona uma coluna fictícia para evitar erros

# # Sidebar - Filtros
# secao_filtro = st.sidebar.multiselect("Seção", df["SECAO"].unique())
# motivo_filtro = st.sidebar.multiselect("Motivo", df["MOTIVO"].unique())
# colaborador_filtro = st.sidebar.multiselect(
#     "Colaborador", df["COLABORADOR"].unique())

# # Filtro por Data de Saída
# if "DATA_SAIDA" in df.columns and not df["DATA_SAIDA"].isnull().all():
#     # Definir o intervalo mínimo e máximo de datas
#     min_date = df["DATA_SAIDA"].min().date(
#     ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()
#     max_date = df["DATA_SAIDA"].max().date(
#     ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()

#     # Widget para selecionar o intervalo de datas
#     date_range = st.sidebar.date_input(
#         "Selecione o intervalo de datas",
#         value=[min_date, max_date],  # Valor padrão: intervalo completo
#         min_value=min_date,
#         max_value=max_date,
#     )
# else:
#     st.sidebar.warning(
#         "Não há dados válidos na coluna 'DATA_SAIDA' para aplicar o filtro de data.")
#     date_range = None

# # Aplicar filtros
# filtered_df = df

# # Filtrar por Seção
# if secao_filtro:
#     filtered_df = filtered_df[filtered_df["SECAO"].isin(secao_filtro)]

# # Filtrar por Motivo
# if motivo_filtro:
#     filtered_df = filtered_df[filtered_df["MOTIVO"].isin(motivo_filtro)]

# # Filtrar por Colaborador
# if colaborador_filtro:
#     filtered_df = filtered_df[filtered_df["COLABORADOR"].isin(
#         colaborador_filtro)]

# # Filtrar por Data de Saída
# if date_range and len(date_range) == 2:
#     start_date, end_date = date_range
#     filtered_df = filtered_df[
#         (filtered_df["DATA_SAIDA"] >= pd.to_datetime(start_date)) &
#         (filtered_df["DATA_SAIDA"] <= pd.to_datetime(end_date))
#     ]

# # Exibir dados filtrados
# st.subheader("Dados Filtrados")
# st.dataframe(filtered_df)

# # Gráficos
# st.subheader("Gráficos")

# # Top 15 Colaboradores que Mais Aparecem
# st.write("Top 15 Colaboradores que Mais Aparecem")
# if "COLABORADOR" in filtered_df.columns:
#     top_colaboradores = filtered_df["COLABORADOR"].value_counts().head(15)
#     fig_top_colaboradores = px.bar(
#         top_colaboradores,
#         x=top_colaboradores.values,
#         y=top_colaboradores.index,
#         labels={"x": "Número de Ocorrências", "y": "Colaborador"},
#         title="Top 15 Colaboradores que Mais Aparecem",
#         orientation="h",
#     )
#     st.plotly_chart(fig_top_colaboradores)

# # Gráfico 1: Valor Total por Seção (Limitado aos 10 primeiros)
# st.write("Valor Total por Seção (Top 10)")
# if "SECAO" in filtered_df.columns and "VALOR" in filtered_df.columns:
#     valor_por_secao = filtered_df.groupby(
#         "SECAO")["VALOR"].sum().sort_values(ascending=False).head(10)
#     fig1 = px.bar(
#         valor_por_secao,
#         x=valor_por_secao.values,
#         y=valor_por_secao.index,
#         labels={"x": "Valor Total", "y": "Seção"},
#         title="Valor Total por Seção (Top 10)",
#         orientation="h",
#     )
#     st.plotly_chart(fig1)

# # Gráfico 2: Distribuição de Quantidades por DESCRIÇÃO (Top 15)
# st.write("Distribuição de Quantidades por DESCRIÇÃO (Top 15)")
# if all(col in filtered_df.columns for col in ["DESCRICAO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
#     quantidades_por_descricao = (
#         filtered_df.groupby("DESCRICAO")[
#             ["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]]
#         .sum()
#         .sum(axis=1)
#     )
#     quantidades_por_descricao = quantidades_por_descricao.sort_values(
#         ascending=False).head(15)
#     fig2 = px.bar(
#         quantidades_por_descricao,
#         x=quantidades_por_descricao.values,
#         y=quantidades_por_descricao.index,
#         labels={"x": "Quantidade Total", "y": "Descrição"},
#         title="Distribuição de Quantidades por DESCRIÇÃO (Top 15)",
#         orientation="h",
#     )
#     st.plotly_chart(fig2)

# # Gráfico 3: Top 15 Seções que Mais Fazem Pedidos de Uniforme
# st.write("Top 15 Seções que Mais Fazem Pedidos de Uniforme")
# if "SECAO" in filtered_df.columns:
#     secoes_mais_pedidos = filtered_df["SECAO"].value_counts().head(15)
#     fig3 = px.bar(
#         secoes_mais_pedidos,
#         x=secoes_mais_pedidos.values,
#         y=secoes_mais_pedidos.index,
#         labels={"x": "Número de Pedidos", "y": "Seção"},
#         title="Top 15 Seções que Mais Fazem Pedidos de Uniforme",
#         orientation="h",
#     )
#     st.plotly_chart(fig3)

# # Gráfico 4: Evolução de Saídas ao Longo do Tempo
# st.write("Evolução de Saídas ao Longo do Tempo")
# if "DATA_SAIDA" in filtered_df.columns:
#     filtered_df["MES_ANO"] = filtered_df["DATA_SAIDA"].dt.to_period(
#         "M").astype(str)
#     saidas_por_mes = filtered_df.groupby("MES_ANO").size()
#     fig4 = px.line(
#         saidas_por_mes,
#         x=saidas_por_mes.index,
#         y=saidas_por_mes.values,
#         labels={"x": "Mês/Ano", "y": "Número de Saídas"},
#         title="Evolução de Saídas ao Longo do Tempo",
#     )
#     fig4.update_xaxes(tickangle=45)
#     st.plotly_chart(fig4)

# # Gráfico 5: Top 5 Maiores Motivos de Pedido de Uniforme
# st.write("Top 5 Maiores Motivos de Pedido de Uniforme")
# if "MOTIVO" in filtered_df.columns:
#     motivos_mais_comuns = filtered_df["MOTIVO"].value_counts().head(5)
#     fig5 = px.bar(
#         motivos_mais_comuns,
#         x=motivos_mais_comuns.values,
#         y=motivos_mais_comuns.index,
#         labels={"x": "Número de Pedidos", "y": "Motivo"},
#         title="Top 5 Maiores Motivos de Pedido de Uniforme",
#         orientation="h",
#     )
#     st.plotly_chart(fig5)

# # Gráfico 6: Barras Empilhadas - Distribuição de Quantidades por Seção
# st.write("Distribuição de Quantidades por Seção")
# if all(col in filtered_df.columns for col in ["SECAO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
#     quantidades_por_secao = filtered_df.groupby(
#         "SECAO")[["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum()
#     fig6 = px.bar(
#         quantidades_por_secao,
#         x=quantidades_por_secao.index,
#         y=["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"],
#         title="Distribuição de Quantidades por Seção",
#         labels={"x": "Seção", "y": "Quantidade"},
#         barmode="stack"
#     )
#     st.plotly_chart(fig6)

# # Gráfico 7: Pizza - Proporção de Motivos de Pedido
# st.write("Proporção de Motivos de Pedido de Uniforme")
# if "MOTIVO" in filtered_df.columns:
#     motivos = filtered_df["MOTIVO"].value_counts()
#     fig7 = px.pie(
#         motivos,
#         values=motivos.values,
#         names=motivos.index,
#         title="Proporção de Motivos de Pedido de Uniforme"
#     )
#     st.plotly_chart(fig7)

# # Gráfico 8: Linha - Evolução de Pedidos por Colaborador
# st.write("Evolução de Pedidos por Colaborador")
# if "DATA_SAIDA" in filtered_df.columns and "COLABORADOR" in filtered_df.columns:
#     top_colaboradores = filtered_df["COLABORADOR"].value_counts().head(5).index
#     df_top_colaboradores = filtered_df[filtered_df["COLABORADOR"].isin(
#         top_colaboradores)]
#     df_top_colaboradores["MES_ANO"] = df_top_colaboradores["DATA_SAIDA"].dt.to_period(
#         "M").astype(str)
#     pedidos_por_colaborador = df_top_colaboradores.groupby(
#         ["MES_ANO", "COLABORADOR"]).size().reset_index(name="Pedidos")
#     fig8 = px.line(
#         pedidos_por_colaborador,
#         x="MES_ANO",
#         y="Pedidos",
#         color="COLABORADOR",
#         title="Evolução de Pedidos por Colaborador"
#     )
#     fig8.update_xaxes(tickangle=45)
#     st.plotly_chart(fig8)

# # Gráfico 9: Dispersão - Relação entre Valor e Quantidade
# st.write("Relação entre Valor e Quantidade Total")
# if all(col in filtered_df.columns for col in ["VALOR", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
#     filtered_df["QUANTIDADE_TOTAL"] = filtered_df[[
#         "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum(axis=1)
#     fig9 = px.scatter(
#         filtered_df,
#         x="QUANTIDADE_TOTAL",
#         y="VALOR",
#         title="Relação entre Valor e Quantidade Total",
#         labels={"QUANTIDADE_TOTAL": "Quantidade Total", "VALOR": "Valor Total"}
#     )
#     st.plotly_chart(fig9)

# # Gráfico 10: Calor - Frequência de Pedidos por Dia da Semana
# st.write("Frequência de Pedidos por Dia da Semana")
# if "DATA_SAIDA" in filtered_df.columns:
#     filtered_df["DIA_SEMANA"] = filtered_df["DATA_SAIDA"].dt.day_name()
#     pedidos_por_dia = filtered_df["DIA_SEMANA"].value_counts().reindex([
#         "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
#     ])
#     fig10 = px.bar(
#         pedidos_por_dia,
#         x=pedidos_por_dia.index,
#         y=pedidos_por_dia.values,
#         title="Frequência de Pedidos por Dia da Semana",
#         labels={"x": "Dia da Semana", "y": "Número de Pedidos"}
#     )
#     st.plotly_chart(fig10)

# # Gráfico 11: Boxplot - Distribuição de Valores por Seção
# st.write("Distribuição de Valores por Seção")
# if "SECAO" in filtered_df.columns and "VALOR" in filtered_df.columns:
#     fig11 = px.box(
#         filtered_df,
#         x="SECAO",
#         y="VALOR",
#         title="Distribuição de Valores por Seção",
#         labels={"SECAO": "Seção", "VALOR": "Valor Total"}
#     )
#     st.plotly_chart(fig11)

# # Gráfico 12: Funil - Fluxo de Pedidos por Status
# st.write("Fluxo de Pedidos por Status")
# if "STATUS" in filtered_df.columns:
#     status_counts = filtered_df["STATUS"].value_counts().sort_index()
#     fig12 = px.funnel(
#         status_counts,
#         x=status_counts.values,
#         y=status_counts.index,
#         title="Fluxo de Pedidos por Status",
#         labels={"x": "Número de Pedidos", "y": "Status"}
#     )
#     st.plotly_chart(fig12)

# # Gráfico 13: Mapa de Calor - Pedidos por Mês e Seção
# st.write("Pedidos por Mês e Seção")
# if "DATA_SAIDA" in filtered_df.columns and "SECAO" in filtered_df.columns:
#     filtered_df["MES_ANO"] = filtered_df["DATA_SAIDA"].dt.to_period(
#         "M").astype(str)
#     heatmap_data = filtered_df.groupby(
#         ["MES_ANO", "SECAO"]).size().unstack(fill_value=0)
#     fig13 = px.imshow(
#         heatmap_data,
#         title="Pedidos por Mês e Seção",
#         labels=dict(x="Seção", y="Mês/Ano", color="Número de Pedidos"),
#         aspect="auto"
#     )
#     st.plotly_chart(fig13)

# # Gráfico 14: Barras Agrupadas - Comparação de Quantidades por Motivo
# st.write("Comparação de Quantidades por Motivo")
# if all(col in filtered_df.columns for col in ["MOTIVO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
#     filtered_df["QUANTIDADE_TOTAL"] = filtered_df[[
#         "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum(axis=1)
#     quantidades_por_motivo = filtered_df.groupby(
#         "MOTIVO")["QUANTIDADE_TOTAL"].sum().reset_index()
#     fig14 = px.bar(
#         quantidades_por_motivo,
#         x="MOTIVO",
#         y="QUANTIDADE_TOTAL",
#         title="Comparação de Quantidades por Motivo",
#         labels={"MOTIVO": "Motivo", "QUANTIDADE_TOTAL": "Quantidade Total"}
#     )
#     st.plotly_chart(fig14)

# # Rodapé
# st.sidebar.markdown("---")
# st.sidebar.markdown("Desenvolvido com ❤️ por [Seu Nome]")


# ********************************CLUADE************************************

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
        df = pd.read_csv("/dataset/UNIFORME.csv")
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


# ***************************************DEEPSEEK*********************************************************


# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
# import streamlit as st

# # Configuração da página
# st.set_page_config(page_title="Análise de Pedidos de Uniformes",
#                    page_icon="📊", layout="wide")

# # Título da aplicação
# st.title("📊 Análise de Pedidos de Uniformes")

# # Carregar o arquivo CSV
# uploaded_file = st.file_uploader("Carregue o arquivo CSV", type=["csv"])

# if uploaded_file is not None:
#     # Ler o arquivo CSV
#     df = pd.read_csv(uploaded_file)

#     # Exibir os dados brutos
#     st.sidebar.header("Dados Brutos")
#     if st.sidebar.checkbox("Mostrar dados brutos"):
#         st.write(df)

#     # Filtros
#     st.sidebar.header("Filtros")
#     descricao = st.sidebar.multiselect(
#         "Selecione a Descrição", options=df['DESCRICAO'].unique())
#     colaborador = st.sidebar.multiselect(
#         "Selecione o Colaborador", options=df['COLABORADOR'].unique())
#     requisitante = st.sidebar.multiselect(
#         "Selecione o Requisitante", options=df['REQUISITANTE'].unique())
#     secao = st.sidebar.multiselect(
#         "Selecione a Seção", options=df['SECAO'].unique())

#     # Aplicar filtros
#     if descricao:
#         df = df[df['DESCRICAO'].isin(descricao)]
#     if colaborador:
#         df = df[df['COLABORADOR'].isin(colaborador)]
#     if requisitante:
#         df = df[df['REQUISITANTE'].isin(requisitante)]
#     if secao:
#         df = df[df['SECAO'].isin(secao)]

#     # Gráfico 1: Top 10 Descrições mais solicitadas
#     st.header("Top 10 Descrições mais Solicitadas")
#     top_descricoes = df['DESCRICAO'].value_counts().nlargest(10)
#     fig1, ax1 = plt.subplots()
#     sns.barplot(x=top_descricoes.values, y=top_descricoes.index,
#                 ax=ax1, palette="viridis")
#     ax1.set_xlabel("Quantidade")
#     ax1.set_ylabel("Descrição")
#     st.pyplot(fig1)

#     # Gráfico 2: Valor total por Requisitante
#     st.header("Valor Total por Requisitante")
#     valor_por_requisitante = df.groupby(
#         'REQUISITANTE')['VALOR'].sum().nlargest(10)
#     fig2, ax2 = plt.subplots()
#     sns.barplot(x=valor_por_requisitante.values,
#                 y=valor_por_requisitante.index, ax=ax2, palette="magma")
#     ax2.set_xlabel("Valor Total")
#     ax2.set_ylabel("Requisitante")
#     st.pyplot(fig2)

#     # Gráfico 3: Quantidade total por Seção
#     st.header("Quantidade Total por Seção")
#     quantidade_por_secao = df.groupby('SECAO')[
#         ['QUANTIDADE1', 'QUANTIDADE2', 'QUANTIDADE3']].sum().sum(axis=1).nlargest(10)
#     fig3, ax3 = plt.subplots()
#     sns.barplot(x=quantidade_por_secao.values,
#                 y=quantidade_por_secao.index, ax=ax3, palette="plasma")
#     ax3.set_xlabel("Quantidade Total")
#     ax3.set_ylabel("Seção")
#     st.pyplot(fig3)

#     # Gráfico 4: Motivo dos Pedidos
#     st.header("Motivo dos Pedidos")
#     motivo_counts = df['MOTIVO'].value_counts().nlargest(10)
#     fig4, ax4 = plt.subplots()
#     sns.barplot(x=motivo_counts.values, y=motivo_counts.index,
#                 ax=ax4, palette="coolwarm")
#     ax4.set_xlabel("Quantidade")
#     ax4.set_ylabel("Motivo")
#     st.pyplot(fig4)

#     # Gráfico 5: Evolução Temporal dos Pedidos
#     st.header("Evolução Temporal dos Pedidos")
#     df['DATA_SAIDA'] = pd.to_datetime(df['DATA_SAIDA'])
#     pedidos_por_data = df.set_index('DATA_SAIDA').resample('M').size()
#     fig5, ax5 = plt.subplots()
#     sns.lineplot(x=pedidos_por_data.index,
#                  y=pedidos_por_data.values, ax=ax5, color="blue")
#     ax5.set_xlabel("Data")
#     ax5.set_ylabel("Número de Pedidos")
#     st.pyplot(fig5)

# else:
#     st.info("Por favor, carregue um arquivo CSV para começar a análise.")

# # Rodapé
# st.sidebar.markdown("---")
# st.sidebar.markdown("Desenvolvido por [Seu Nome]")


# ***********************************QWEN*****************************************


# from datetime import datetime

# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # Configuração inicial do Streamlit
# st.set_page_config(page_title="Análise de Pedidos de Uniforme",
#                    page_icon="👕", layout="wide")
# st.title("📊 Análise de Pedidos de Uniforme")
# st.sidebar.header("🔍 Filtros")

# # Carregar dados do arquivo CSV
# csv_path = "C:/Cursos/Asimov/Streamlit/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/proejetoUniforme/dataset/UNIFORME.csv"
# try:
#     df = pd.read_csv(csv_path)
# except FileNotFoundError:
#     st.error("Arquivo CSV não encontrado. Verifique o caminho fornecido.")
#     st.stop()

# # Converter DATA_SAIDA para datetime, se necessário
# if "DATA_SAIDA" in df.columns:
#     df["DATA_SAIDA"] = pd.to_datetime(
#         df["DATA_SAIDA"], format="%d/%m/%Y", errors="coerce")

# # Sidebar - Filtros
# secao_filtro = st.sidebar.multiselect("Seção", df["SECAO"].unique())
# motivo_filtro = st.sidebar.multiselect("Motivo", df["MOTIVO"].unique())
# colaborador_filtro = st.sidebar.multiselect(
#     "Colaborador", df["COLABORADOR"].unique())

# # Filtro por Data de Saída
# if "DATA_SAIDA" in df.columns and not df["DATA_SAIDA"].isnull().all():
#     min_date = df["DATA_SAIDA"].min().date(
#     ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()
#     max_date = df["DATA_SAIDA"].max().date(
#     ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()
#     date_range = st.sidebar.date_input(
#         "Selecione o intervalo de datas",
#         value=[min_date, max_date],
#         min_value=min_date,
#         max_value=max_date,
#     )
# else:
#     st.sidebar.warning(
#         "Não há dados válidos na coluna 'DATA_SAIDA' para aplicar o filtro de data.")
#     date_range = None

# # Aplicar filtros
# filtered_df = df

# # Filtrar por Seção
# if secao_filtro:
#     filtered_df = filtered_df[filtered_df["SECAO"].isin(secao_filtro)]

# # Filtrar por Motivo
# if motivo_filtro:
#     filtered_df = filtered_df[filtered_df["MOTIVO"].isin(motivo_filtro)]

# # Filtrar por Colaborador
# if colaborador_filtro:
#     filtered_df = filtered_df[filtered_df["COLABORADOR"].isin(
#         colaborador_filtro)]

# # Filtrar por Data de Saída
# if date_range and len(date_range) == 2:
#     start_date, end_date = date_range
#     filtered_df = filtered_df[
#         (filtered_df["DATA_SAIDA"] >= pd.to_datetime(start_date)) &
#         (filtered_df["DATA_SAIDA"] <= pd.to_datetime(end_date))
#     ]

# # Exibir dados filtrados
# st.subheader("📋 Dados Filtrados")
# st.dataframe(filtered_df, use_container_width=True)

# # Gráficos
# st.subheader("📊 Gráficos")

# # Gráfico 1: Top 10 Colaboradores que Mais Fizeram Pedidos
# st.write("👥 Top 10 Colaboradores que Mais Fizeram Pedidos")
# if "COLABORADOR" in filtered_df.columns:
#     top_colaboradores = filtered_df["COLABORADOR"].value_counts().head(10)
#     fig_top_colaboradores = px.bar(
#         top_colaboradores,
#         x=top_colaboradores.values,
#         y=top_colaboradores.index,
#         labels={"x": "Número de Pedidos", "y": "Colaborador"},
#         title="Top 10 Colaboradores que Mais Fizeram Pedidos",
#         orientation="h",
#         color_discrete_sequence=["#636EFA"],
#     )
#     fig_top_colaboradores.update_layout(height=400)
#     st.plotly_chart(fig_top_colaboradores, use_container_width=True)

# # Gráfico 2: Valor Total por Seção (Top 10)
# st.write("🏢 Valor Total por Seção (Top 10)")
# if "SECAO" in filtered_df.columns and "VALOR" in filtered_df.columns:
#     valor_por_secao = filtered_df.groupby(
#         "SECAO")["VALOR"].sum().sort_values(ascending=False).head(10)
#     fig_valor_secao = px.bar(
#         valor_por_secao,
#         x=valor_por_secao.values,
#         y=valor_por_secao.index,
#         labels={"x": "Valor Total", "y": "Seção"},
#         title="Valor Total por Seção (Top 10)",
#         orientation="h",
#         color_discrete_sequence=["#EF553B"],
#     )
#     fig_valor_secao.update_layout(height=400)
#     st.plotly_chart(fig_valor_secao, use_container_width=True)

# # Gráfico 3: Distribuição de Quantidades por Descrição (Top 10)
# st.write("👕 Distribuição de Quantidades por Descrição (Top 10)")
# if all(col in filtered_df.columns for col in ["DESCRICAO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
#     quantidades_por_descricao = (
#         filtered_df.groupby("DESCRICAO")[
#             ["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]]
#         .sum()
#         .sum(axis=1)
#         .sort_values(ascending=False)
#         .head(10)
#     )
#     fig_quantidades_descricao = px.bar(
#         quantidades_por_descricao,
#         x=quantidades_por_descricao.values,
#         y=quantidades_por_descricao.index,
#         labels={"x": "Quantidade Total", "y": "Descrição"},
#         title="Distribuição de Quantidades por Descrição (Top 10)",
#         orientation="h",
#         color_discrete_sequence=["#00CC96"],
#     )
#     fig_quantidades_descricao.update_layout(height=400)
#     st.plotly_chart(fig_quantidades_descricao, use_container_width=True)

# # Gráfico 4: Evolução de Pedidos ao Longo do Tempo
# st.write("📅 Evolução de Pedidos ao Longo do Tempo")
# if "DATA_SAIDA" in filtered_df.columns:
#     filtered_df["MES_ANO"] = filtered_df["DATA_SAIDA"].dt.to_period(
#         "M").astype(str)
#     saidas_por_mes = filtered_df.groupby("MES_ANO").size()
#     fig_evolucao_pedidos = px.line(
#         saidas_por_mes,
#         x=saidas_por_mes.index,
#         y=saidas_por_mes.values,
#         labels={"x": "Mês/Ano", "y": "Número de Pedidos"},
#         title="Evolução de Pedidos ao Longo do Tempo",
#         markers=True,
#         color_discrete_sequence=["#AB63FA"],
#     )
#     fig_evolucao_pedidos.update_xaxes(tickangle=45)
#     fig_evolucao_pedidos.update_layout(height=400)
#     st.plotly_chart(fig_evolucao_pedidos, use_container_width=True)

# # Gráfico 5: Proporção de Motivos de Pedido (Pizza)
# st.write("🎯 Proporção de Motivos de Pedido")
# if "MOTIVO" in filtered_df.columns:
#     motivos = filtered_df["MOTIVO"].value_counts().head(10)
#     fig_motivos = px.pie(
#         motivos,
#         values=motivos.values,
#         names=motivos.index,
#         title="Proporção de Motivos de Pedido (Top 10)",
#         hole=0.3,
#         color_discrete_sequence=px.colors.qualitative.Pastel,
#     )
#     fig_motivos.update_layout(height=400)
#     st.plotly_chart(fig_motivos, use_container_width=True)

# # Rodapé
# st.sidebar.markdown("---")
# st.sidebar.markdown("Desenvolvido com ❤️ por [Seu Nome]")


# *********************GEMINI****************************

# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # Título e subtítulo
# st.set_page_config(page_title="Análise de Pedidos de Uniforme",
#                    page_icon=":bar_chart:", layout="wide")
# st.title('Análise de Pedidos de Uniforme')
# st.subheader('Dashboard Interativo para Tomada de Decisão')

# # Carregamento do arquivo CSV
# uploaded_file = st.file_uploader("Escolha o arquivo CSV", type="csv")

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)

#     # Tratamento de dados
#     df['DATA_SAIDA'] = pd.to_datetime(df['DATA_SAIDA'])

#     # Filtros
#     colunas = ['COLABORADOR', 'REQUISITANTE', 'MOTIVO', 'SECAO']
#     filtros = {}
#     for coluna in colunas:
#         valores = df[coluna].unique()
#         filtros[coluna] = st.multiselect(f'Filtrar por {coluna}', valores)
#         if filtros[coluna]:
#             df = df[df[coluna].isin(filtros[coluna])]

#     # Métricas e KPIs
#     total_pedidos = len(df)
#     valor_total_pedidos = df['VALOR'].sum()
#     media_pedidos = df['VALOR'].mean()

#     # Layout em colunas
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total de Pedidos", total_pedidos)
#     col2.metric("Valor Total dos Pedidos", f"R$ {valor_total_pedidos:.2f}")
#     col3.metric("Média por Pedido", f"R$ {media_pedidos:.2f}")

#     # Gráficos
#     if not df.empty:
#         # Top 10 produtos mais pedidos
#         top_10_produtos = df['DESCRICAO'].value_counts().nlargest(10)
#         fig_produtos = px.bar(top_10_produtos, x=top_10_produtos.index, y=top_10_produtos.values,
#                               title='Top 10 Produtos Mais Pedidos')
#         st.plotly_chart(fig_produtos)

#         # Distribuição de pedidos por seção
#         dist_secao = df['SECAO'].value_counts()
#         fig_secao = px.pie(dist_secao, names=dist_secao.index, values=dist_secao.values,
#                            title='Distribuição de Pedidos por Seção')
#         st.plotly_chart(fig_secao)

#         # Evolução dos pedidos ao longo do tempo
#         pedidos_tempo = df.groupby(pd.Grouper(
#             key='DATA_SAIDA', freq='M')).size()
#         fig_tempo = px.line(pedidos_tempo, x=pedidos_tempo.index, y=pedidos_tempo.values,
#                             title='Evolução dos Pedidos ao Longo do Tempo')
#         st.plotly_chart(fig_tempo)

#         # Relação entre quantidade e valor dos pedidos
#         fig_relacao = px.scatter(df, x='QUANTIDADE1', y='VALOR',
#                                  title='Relação entre Quantidade e Valor dos Pedidos')
#         st.plotly_chart(fig_relacao)

#         # Gráfico de barras com a quantidade de pedidos por colaborador
#         pedidos_colaborador = df['COLABORADOR'].value_counts()
#         fig_colaborador = px.bar(pedidos_colaborador, x=pedidos_colaborador.index, y=pedidos_colaborador.values,
#                                  title='Quantidade de Pedidos por Colaborador')
#         st.plotly_chart(fig_colaborador)

#         # Gráfico de pizza com a distribuição de pedidos por motivo
#         pedidos_motivo = df['MOTIVO'].value_counts()
#         fig_motivo = px.pie(pedidos_motivo, names=pedidos_motivo.index, values=pedidos_motivo.values,
#                             title='Distribuição de Pedidos por Motivo')
#         st.plotly_chart(fig_motivo)

#     else:
#         st.write("Nenhum pedido encontrado com os filtros selecionados.")

# else:
#     st.write("Por favor, envie o arquivo CSV para iniciar a análise.")


# **************************GPT****************************

# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # Configurações iniciais do Streamlit
# st.set_page_config(
#     page_title='Dashboard de Pedidos de Uniforme', layout='wide')

# # Título
# st.title('Dashboard de Pedidos de Uniforme')

# # Upload do arquivo CSV
# dados = st.file_uploader('Carregue o arquivo .csv com os dados', type=['csv'])

# if dados is not None:
#     # Leitura do arquivo CSV
#     df = pd.read_csv(dados)

#     # Filtros interativos
#     st.sidebar.header('Filtros')
#     secao_filter = st.sidebar.multiselect(
#         'Selecione a Seção:', options=df['SECAO'].unique())
#     requisitante_filter = st.sidebar.multiselect(
#         'Selecione o Requisitante:', options=df['REQUISITANTE'].unique())
#     motivo_filter = st.sidebar.multiselect(
#         'Selecione o Motivo:', options=df['MOTIVO'].unique())

#     # Aplicação dos filtros
#     df_filtered = df.copy()
#     if secao_filter:
#         df_filtered = df_filtered[df_filtered['SECAO'].isin(secao_filter)]
#     if requisitante_filter:
#         df_filtered = df_filtered[df_filtered['REQUISITANTE'].isin(
#             requisitante_filter)]
#     if motivo_filter:
#         df_filtered = df_filtered[df_filtered['MOTIVO'].isin(motivo_filter)]

#     # Gráfico de Barras - Top 10 Produtos
#     st.header('Top 10 Produtos por Quantidade')
#     top10_produtos = df_filtered.groupby('DESCRICAO').sum(numeric_only=True)[
#         'QUANTIDADE1'].nlargest(10).reset_index()
#     fig_bar = px.bar(top10_produtos, x='DESCRICAO',
#                      y='QUANTIDADE1', title='Top 10 Produtos por Quantidade')
#     st.plotly_chart(fig_bar)

#     # Gráfico de Pizza - Distribuição por Seção
#     st.header('Distribuição por Seção')
#     fig_pie = px.pie(df_filtered, names='SECAO',
#                      title='Distribuição por Seção')
#     st.plotly_chart(fig_pie)

#     # Gráfico de Linha - Evolução dos Pedidos por Data
#     st.header('Evolução dos Pedidos por Data')
#     df_filtered['DATA_SAIDA'] = pd.to_datetime(
#         df_filtered['DATA_SAIDA'], errors='coerce')
#     df_evolucao = df_filtered.groupby('DATA_SAIDA').sum(
#         numeric_only=True).reset_index()
#     fig_line = px.line(df_evolucao, x='DATA_SAIDA',
#                        y='QUANTIDADE1', title='Evolução dos Pedidos por Data')
#     st.plotly_chart(fig_line)

#     # Gráfico de Barras - Valor Total por Requisitante
#     st.header('Valor Total por Requisitante (Top 10)')
#     top10_requisitantes = df_filtered.groupby('REQUISITANTE').sum(
#         numeric_only=True)['VALOR'].nlargest(10).reset_index()
#     fig_bar_valor = px.bar(top10_requisitantes, x='REQUISITANTE',
#                            y='VALOR', title='Valor Total por Requisitante')
#     st.plotly_chart(fig_bar_valor)

#     # Exibição da Tabela Filtrada
#     st.header('Dados Filtrados')
#     st.dataframe(df_filtered)
# else:
#     st.warning('Por favor, carregue um arquivo CSV para visualizar os dados.')
