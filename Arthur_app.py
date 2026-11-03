import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render():
    st.header("Taxa de Desocupação Geral (2012 x 2022)")
    st.write("Análise focada no mapeamento do desemprego por Unidade da Federação e identificação do estado com maior eficiência na redução do índice.")
    
    # os dados da PNAD 
    data = {
        'UF': ['BA', 'PE', 'CE', 'MG', 'SP', 'RJ', 'SC', 'PR', 'RS'],
        'Regiao': ['Nordeste', 'Nordeste', 'Nordeste', 'Sudeste', 'Sudeste', 'Sudeste', 'Sul', 'Sul', 'Sul'],
        'Desocupacao_2012': [15.2, 14.8, 11.2, 8.5, 9.2, 10.1, 5.2, 7.1, 6.8],
        'Desocupacao_2022': [13.1, 12.5, 9.4, 6.2, 7.5, 9.8, 3.8, 5.0, 4.5]
    }
    df = pd.DataFrame(data)
    df['Reducao'] = df['Desocupacao_2012'] - df['Desocupacao_2022']
    
    # filtro de região
    regioes = st.multiselect("Filtrar por Região (Arthur)", options=df['Regiao'].unique(), default=df['Regiao'].unique())
    df_filtrado = df[df['Regiao'].isin(regioes)]
    
    # KPIs 
    st.subheader("Indicadores de Desempenho (Média Geral)")
    col1, col2 = st.columns(2)
    col1.metric("Média Desocupação 2012", f"{df_filtrado['Desocupacao_2012'].mean():.2f}%")
    col2.metric("Média Desocupação 2022", f"{df_filtrado['Desocupacao_2022'].mean():.2f}%")
    
    # pergunta de negocio 
    st.markdown("Qual estado mais reduziu a população desocupada?")
    estado_top = df.loc[df['Reducao'].idxmax()]
    st.success(f"O estado que apresentou a maior redução de desemprego foi a **{estado_top['UF']}**, com uma queda de **{estado_top['Reducao']:.1f} pontos percentuais**.")
    
    # grafico de barras
    df_melted = df_filtrado.melt(id_vars=['UF', 'Regiao'], value_vars=['Desocupacao_2012', 'Desocupacao_2022'], 
                                  var_name='Ano', value_name='Taxa (%)')
    df_melted['Ano'] = df_melted['Ano'].str.replace('Desocupacao_', '')
    
    fig = px.bar(df_melted, x='UF', y='Taxa (%)', color='Ano', barmode='group',
                 title="Comparativo da Taxa de Desocupação por UF (2012 vs 2022)",
                 labels={'Taxa (%)': 'Taxa de Desemprego (%)', 'UF': 'Estado'})
    st.plotly_chart(fig, use_container_width=True)

