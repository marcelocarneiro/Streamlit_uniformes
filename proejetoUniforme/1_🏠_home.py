from datetime import datetime

import pandas as pd
import streamlit as st

# Configuração inicial do Streamlit
st.title("Análise de Dados de Uniformes")
st.sidebar.header("Filtros e Opções")

# Carregar dados do arquivo CSV
df = pd.read_csv(
    "C:/Cursos/Asimov/Streamlit/Criando Aplicativos Web com Streamlit/Projeto Streamlit FIFA/proejetoUniforme/dataset/UNIFORME.csv"
)

# Converter DATA_SAIDA para datetime, considerando o formato DD/MM/YYYY
if "DATA_SAIDA" in df.columns:
    try:
        df["DATA_SAIDA"] = pd.to_datetime(
            df["DATA_SAIDA"], format="%d/%m/%Y", errors="coerce")  # Especifica o formato
    except Exception as e:
        st.sidebar.error(f"Erro ao converter a coluna 'DATA_SAIDA': {e}")
        df["DATA_SAIDA"] = None  # Define como nulo se houver erro
else:
    st.sidebar.warning(
        "A coluna 'DATA_SAIDA' não foi encontrada no arquivo CSV.")
    df["DATA_SAIDA"] = None  # Adiciona uma coluna fictícia para evitar erros

# Sidebar - Filtros
secao_filtro = st.sidebar.multiselect("Seção", df["SECAO"].unique())
motivo_filtro = st.sidebar.multiselect("Motivo", df["MOTIVO"].unique())
colaborador_filtro = st.sidebar.multiselect(
    "Colaborador", df["COLABORADOR"].unique())

# Filtro por Data de Saída
if "DATA_SAIDA" in df.columns and not df["DATA_SAIDA"].isnull().all():
    # Definir o intervalo mínimo e máximo de datas
    min_date = df["DATA_SAIDA"].min().date(
    ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()
    max_date = df["DATA_SAIDA"].max().date(
    ) if not df["DATA_SAIDA"].isnull().all() else datetime.today().date()

    # Widget para selecionar o intervalo de datas
    date_range = st.sidebar.date_input(
        "Selecione o intervalo de datas",
        value=[min_date, max_date],  # Valor padrão: intervalo completo
        min_value=min_date,
        max_value=max_date,
    )
else:
    st.sidebar.warning(
        "Não há dados válidos na coluna 'DATA_SAIDA' para aplicar o filtro de data.")
    date_range = None

# Aplicar filtros
filtered_df = df

# Filtrar por Seção
if secao_filtro:
    filtered_df = filtered_df[filtered_df["SECAO"].isin(secao_filtro)]

# Filtrar por Motivo
if motivo_filtro:
    filtered_df = filtered_df[filtered_df["MOTIVO"].isin(motivo_filtro)]

# Filtrar por Colaborador
if colaborador_filtro:
    filtered_df = filtered_df[filtered_df["COLABORADOR"].isin(
        colaborador_filtro)]

# Filtrar por Data de Saída
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["DATA_SAIDA"] >= pd.to_datetime(start_date)) &
        (filtered_df["DATA_SAIDA"] <= pd.to_datetime(end_date))
    ]

# Exibir dados filtrados
st.subheader("Dados Filtrados")
st.dataframe(filtered_df)

# Gráficos
st.subheader("Gráficos")

# Top 15 Colaboradores que Mais Aparecem
st.write("Top 15 Colaboradores que Mais Aparecem")
if "COLABORADOR" in filtered_df.columns:
    top_colaboradores = filtered_df["COLABORADOR"].value_counts().head(15)
    fig_top_colaboradores = px.bar(
        top_colaboradores,
        x=top_colaboradores.values,
        y=top_colaboradores.index,
        labels={"x": "Número de Ocorrências", "y": "Colaborador"},
        title="Top 15 Colaboradores que Mais Aparecem",
        orientation="h",
    )
    st.plotly_chart(fig_top_colaboradores)

# Gráfico 1: Valor Total por Seção (Limitado aos 10 primeiros)
st.write("Valor Total por Seção (Top 10)")
if "SECAO" in filtered_df.columns and "VALOR" in filtered_df.columns:
    valor_por_secao = filtered_df.groupby(
        "SECAO")["VALOR"].sum().sort_values(ascending=False).head(10)
    fig1 = px.bar(
        valor_por_secao,
        x=valor_por_secao.values,
        y=valor_por_secao.index,
        labels={"x": "Valor Total", "y": "Seção"},
        title="Valor Total por Seção (Top 10)",
        orientation="h",
    )
    st.plotly_chart(fig1)

# Gráfico 2: Distribuição de Quantidades por DESCRIÇÃO (Top 15)
st.write("Distribuição de Quantidades por DESCRIÇÃO (Top 15)")
if all(col in filtered_df.columns for col in ["DESCRICAO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
    quantidades_por_descricao = (
        filtered_df.groupby("DESCRICAO")[
            ["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]]
        .sum()
        .sum(axis=1)
    )
    quantidades_por_descricao = quantidades_por_descricao.sort_values(
        ascending=False).head(15)
    fig2 = px.bar(
        quantidades_por_descricao,
        x=quantidades_por_descricao.values,
        y=quantidades_por_descricao.index,
        labels={"x": "Quantidade Total", "y": "Descrição"},
        title="Distribuição de Quantidades por DESCRIÇÃO (Top 15)",
        orientation="h",
    )
    st.plotly_chart(fig2)

# Gráfico 3: Top 15 Seções que Mais Fazem Pedidos de Uniforme
st.write("Top 15 Seções que Mais Fazem Pedidos de Uniforme")
if "SECAO" in filtered_df.columns:
    secoes_mais_pedidos = filtered_df["SECAO"].value_counts().head(15)
    fig3 = px.bar(
        secoes_mais_pedidos,
        x=secoes_mais_pedidos.values,
        y=secoes_mais_pedidos.index,
        labels={"x": "Número de Pedidos", "y": "Seção"},
        title="Top 15 Seções que Mais Fazem Pedidos de Uniforme",
        orientation="h",
    )
    st.plotly_chart(fig3)

# Gráfico 4: Evolução de Saídas ao Longo do Tempo
st.write("Evolução de Saídas ao Longo do Tempo")
if "DATA_SAIDA" in filtered_df.columns:
    filtered_df["MES_ANO"] = filtered_df["DATA_SAIDA"].dt.to_period(
        "M").astype(str)
    saidas_por_mes = filtered_df.groupby("MES_ANO").size()
    fig4 = px.line(
        saidas_por_mes,
        x=saidas_por_mes.index,
        y=saidas_por_mes.values,
        labels={"x": "Mês/Ano", "y": "Número de Saídas"},
        title="Evolução de Saídas ao Longo do Tempo",
    )
    fig4.update_xaxes(tickangle=45)
    st.plotly_chart(fig4)

# Gráfico 5: Top 5 Maiores Motivos de Pedido de Uniforme
st.write("Top 5 Maiores Motivos de Pedido de Uniforme")
if "MOTIVO" in filtered_df.columns:
    motivos_mais_comuns = filtered_df["MOTIVO"].value_counts().head(5)
    fig5 = px.bar(
        motivos_mais_comuns,
        x=motivos_mais_comuns.values,
        y=motivos_mais_comuns.index,
        labels={"x": "Número de Pedidos", "y": "Motivo"},
        title="Top 5 Maiores Motivos de Pedido de Uniforme",
        orientation="h",
    )
    st.plotly_chart(fig5)

# Gráfico 6: Barras Empilhadas - Distribuição de Quantidades por Seção
st.write("Distribuição de Quantidades por Seção")
if all(col in filtered_df.columns for col in ["SECAO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
    quantidades_por_secao = filtered_df.groupby(
        "SECAO")[["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum()
    fig6 = px.bar(
        quantidades_por_secao,
        x=quantidades_por_secao.index,
        y=["QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"],
        title="Distribuição de Quantidades por Seção",
        labels={"x": "Seção", "y": "Quantidade"},
        barmode="stack"
    )
    st.plotly_chart(fig6)

# Gráfico 7: Pizza - Proporção de Motivos de Pedido
st.write("Proporção de Motivos de Pedido de Uniforme")
if "MOTIVO" in filtered_df.columns:
    motivos = filtered_df["MOTIVO"].value_counts()
    fig7 = px.pie(
        motivos,
        values=motivos.values,
        names=motivos.index,
        title="Proporção de Motivos de Pedido de Uniforme"
    )
    st.plotly_chart(fig7)

# Gráfico 8: Linha - Evolução de Pedidos por Colaborador
st.write("Evolução de Pedidos por Colaborador")
if "DATA_SAIDA" in filtered_df.columns and "COLABORADOR" in filtered_df.columns:
    top_colaboradores = filtered_df["COLABORADOR"].value_counts().head(5).index
    df_top_colaboradores = filtered_df[filtered_df["COLABORADOR"].isin(
        top_colaboradores)]
    df_top_colaboradores["MES_ANO"] = df_top_colaboradores["DATA_SAIDA"].dt.to_period(
        "M").astype(str)
    pedidos_por_colaborador = df_top_colaboradores.groupby(
        ["MES_ANO", "COLABORADOR"]).size().reset_index(name="Pedidos")
    fig8 = px.line(
        pedidos_por_colaborador,
        x="MES_ANO",
        y="Pedidos",
        color="COLABORADOR",
        title="Evolução de Pedidos por Colaborador"
    )
    fig8.update_xaxes(tickangle=45)
    st.plotly_chart(fig8)

# Gráfico 9: Dispersão - Relação entre Valor e Quantidade
st.write("Relação entre Valor e Quantidade Total")
if all(col in filtered_df.columns for col in ["VALOR", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
    filtered_df["QUANTIDADE_TOTAL"] = filtered_df[[
        "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum(axis=1)
    fig9 = px.scatter(
        filtered_df,
        x="QUANTIDADE_TOTAL",
        y="VALOR",
        title="Relação entre Valor e Quantidade Total",
        labels={"QUANTIDADE_TOTAL": "Quantidade Total", "VALOR": "Valor Total"}
    )
    st.plotly_chart(fig9)

# Gráfico 10: Calor - Frequência de Pedidos por Dia da Semana
st.write("Frequência de Pedidos por Dia da Semana")
if "DATA_SAIDA" in filtered_df.columns:
    filtered_df["DIA_SEMANA"] = filtered_df["DATA_SAIDA"].dt.day_name()
    pedidos_por_dia = filtered_df["DIA_SEMANA"].value_counts().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])
    fig10 = px.bar(
        pedidos_por_dia,
        x=pedidos_por_dia.index,
        y=pedidos_por_dia.values,
        title="Frequência de Pedidos por Dia da Semana",
        labels={"x": "Dia da Semana", "y": "Número de Pedidos"}
    )
    st.plotly_chart(fig10)

# Gráfico 11: Boxplot - Distribuição de Valores por Seção
st.write("Distribuição de Valores por Seção")
if "SECAO" in filtered_df.columns and "VALOR" in filtered_df.columns:
    fig11 = px.box(
        filtered_df,
        x="SECAO",
        y="VALOR",
        title="Distribuição de Valores por Seção",
        labels={"SECAO": "Seção", "VALOR": "Valor Total"}
    )
    st.plotly_chart(fig11)

# Gráfico 12: Funil - Fluxo de Pedidos por Status
st.write("Fluxo de Pedidos por Status")
if "STATUS" in filtered_df.columns:
    status_counts = filtered_df["STATUS"].value_counts().sort_index()
    fig12 = px.funnel(
        status_counts,
        x=status_counts.values,
        y=status_counts.index,
        title="Fluxo de Pedidos por Status",
        labels={"x": "Número de Pedidos", "y": "Status"}
    )
    st.plotly_chart(fig12)

# Gráfico 13: Mapa de Calor - Pedidos por Mês e Seção
st.write("Pedidos por Mês e Seção")
if "DATA_SAIDA" in filtered_df.columns and "SECAO" in filtered_df.columns:
    filtered_df["MES_ANO"] = filtered_df["DATA_SAIDA"].dt.to_period(
        "M").astype(str)
    heatmap_data = filtered_df.groupby(
        ["MES_ANO", "SECAO"]).size().unstack(fill_value=0)
    fig13 = px.imshow(
        heatmap_data,
        title="Pedidos por Mês e Seção",
        labels=dict(x="Seção", y="Mês/Ano", color="Número de Pedidos"),
        aspect="auto"
    )
    st.plotly_chart(fig13)

# Gráfico 14: Barras Agrupadas - Comparação de Quantidades por Motivo
st.write("Comparação de Quantidades por Motivo")
if all(col in filtered_df.columns for col in ["MOTIVO", "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]):
    filtered_df["QUANTIDADE_TOTAL"] = filtered_df[[
        "QUANTIDADE1", "QUANTIDADE2", "QUANTIDADE3"]].sum(axis=1)
    quantidades_por_motivo = filtered_df.groupby(
        "MOTIVO")["QUANTIDADE_TOTAL"].sum().reset_index()
    fig14 = px.bar(
        quantidades_por_motivo,
        x="MOTIVO",
        y="QUANTIDADE_TOTAL",
        title="Comparação de Quantidades por Motivo",
        labels={"MOTIVO": "Motivo", "QUANTIDADE_TOTAL": "Quantidade Total"}
    )
    st.plotly_chart(fig14)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ por [Seu Nome]")
