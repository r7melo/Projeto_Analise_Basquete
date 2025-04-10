# linha_streamlit.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

import pandas as pd

st.set_page_config(page_title='Avaliação de Desempenho de Jogadores')

url = "https://docs.google.com/spreadsheets/d/15UpYWf0Py2GISjyV3Nkx2J1W_hCONYBHTwTtaGXlbR8/export?format=csv"
dataframe = pd.read_csv(url)
dataframe = dataframe[dataframe.columns[2:]]

tamanho_setor = 14
metricas = ['Pontuação (Pontos)', 'Rebotes', 'Assistências', 'Tocos (Bloqueios)', 'Arremessos de 3 Pontos', 'Roubos de Bola']

df_mean = dataframe.mean()

setores = [_ for _ in range(0,len(df_mean)+1,tamanho_setor)]

data_final = []

for i in range(len(setores)-1):
    s0, s1 = setores[i], setores[i+1]
    data_l = dataframe.T[s0:s1].T.mean().values
    data_final.append(data_l)

df_final = pd.DataFrame(data_final, index=metricas, columns=dataframe.columns[:tamanho_setor])

df = df_final

# Transforma em formato longo
df_long = df.reset_index().melt(id_vars='index', var_name='Jogador', value_name='Nota')
df_long = df_long.rename(columns={'index': 'Critério'})

# Interface Streamlit
st.title("📊 Avaliação de Jogadores - Basquete")
jogadores = st.multiselect("Selecione os jogadores:", df.columns.tolist(), default=df.columns.tolist())

# Filtra os jogadores escolhidos
df_filtrado = df_long[df_long['Jogador'].isin(jogadores)]

# Gráfico
fig = px.line(
    df_filtrado,
    x='Critério',
    y='Nota',
    color='Jogador',
    markers=True,
    line_shape='spline'
)
fig.update_layout(title="Desempenho por Métrica", hovermode='x unified')

st.plotly_chart(fig, use_container_width=True)



import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carrega o arquivo CSV com as métricas como índice
df = df_final

# Título da página
st.title("🏀 Radar de Desempenho dos Jogadores - Basquete")

# Selecionar jogadores
jogadores = st.multiselect(
    "Selecione os jogadores:",
    df.columns.tolist(),
    default=df.columns.tolist(),
    key="selecionar_jogadores"
)

# Loop para mostrar gráfico radar individual
for jogador in jogadores:
    notas = df[jogador].values.tolist()
    criterios = df.index.tolist()

    # Fechar o gráfico circular
    notas += [notas[0]]
    criterios += [criterios[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=notas,
        theta=criterios,
        fill='toself',
        name=jogador,
        line=dict(color='royalblue'),
        marker=dict(size=6)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=False,
        title=f'🎯 Desempenho de {jogador}'
    )

    st.plotly_chart(fig, use_container_width=True)
