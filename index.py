import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
from datetime import datetime 
from streamlit_folium import folium_static
import pydeck as pdk


# Configuração da Página
st.set_page_config(
    page_title="House Rocket Analytics",
    layout="wide",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)

# Estilo Personalizado
st.markdown("""
<style>
    .st-emotion-cache-1v0mbdj img {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .st-bh {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

  # Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("kc_house_data_updat.csv")
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["year"] = df["date"].dt.year  # Garanta que esta linha existe
    return df

df = carregar_dados()
 
# Criar abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📌 Contexto do Negócio", "🏡 Estratégia de Compra", "📈 Melhor Momento para Compra e Venda", "🛠️ Impacto das Reformas", "🗺️ Análise Geográfica", "🎯 Insights"])

# =========================================
#        ABA 1: Contexto do Negócio
# =========================================
with tab1:
    st.title("🏠 House Rocket - Contexto do Negócio e Resultados")
    st.markdown("---")

    # 📌 Contexto do Projeto
    st.header("📌 Contexto do Negócio")
    st.markdown(
        """
        **O House Rocket** é um projeto baseado em análise de dados históricos de vendas de imóveis. O objetivo é usar essas informações para identificar as oportunidades de **compra de imóveis**, determinar o momento ideal para **vendê-los** e analisar o **impacto das reformas** no valor das propriedades.

        Os dados analisados são **de maio/2014 a maio/2015**, considerando **preços, localização, características das propriedades**
        e **sazonalidade das vendas**.
        """
    )

    # 🎯 Perguntas de Negócio
    st.subheader("🎯 Perguntas de Negócio")
    st.markdown("""
    - **Quais casas o CEO da House Rocket deveria comprar e por qual preço?**
    - **Quando é o melhor momento para vender as casas adquiridas?**
    - **A House Rocket deveria investir em reformas?** Se sim, **quais melhorias aumentam mais o valor de revenda?**
    """)
    st.markdown("---")

# =========================================
#         ABA 2: Estratégia de Compra
# =========================================
with tab2:
    st.title("🏡 Estratégia de Compra - House Rocket")
    st.markdown("---")

   

    
    # Tabela das casas recomendadas
    st.subheader("📋 Lista de Casas Recomendadas")
    casas_recomendadas = {
        "Índice": [8978, 9077, 7178, 16580, 18102, 434, 8846, 892, 19687, 1752,
                   1868, 11754, 2205, 8676, 3821, 5598, 15579, 19367, 20631, 19757],
        "Preço ($)": [169100, 182500, 190000, 190000, 194250, 196000, 204700, 205000,
                      205000, 206000, 210000, 210000, 213550, 214000, 215000, 215000,
                      215000, 215000, 215000, 216000],
        "Média da Região ($)": [267711.90] * 20,
        "Zipcode": [98001] * 20,
        "Quartos": [3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 3, 4, 3, 3, 4, 4, 3, 4, 3, 4],
        "Banheiros": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        "Condição": [4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3],
        "Construção (Grade)": [7, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        "Vista (View)": [0] * 20,
        "Frente d’água (Waterfront)": [0] * 20
    }
    df_recomendadas = pd.DataFrame(casas_recomendadas)
    st.dataframe(df_recomendadas)

 
# --------------------------------------------
# Pré-processamento (igual ao do Jupyter)
# --------------------------------------------

    # 1. Calcular média regional (log)
    df['log_price'] = np.log1p(df['price'])
    df['avg_price_region_log'] = df.groupby('zipcode')['log_price'].transform('mean')

    # 2. Filtrar imóveis
    below_avg_price = df['log_price'] < df['avg_price_region_log']
    good_houses = df[
        below_avg_price &
        (df['grade'] >= 7) &
        (df['condition'] >= 3) &
        (df['bedrooms'].isin([3, 4])) &
        (df['bathrooms'] >= 2)
    ].copy()

    # 3. Converter valores
    good_houses['price'] = np.expm1(good_houses['log_price'])
    good_houses['avg_price_region'] = np.expm1(good_houses['avg_price_region_log'])

    # 4. Ordenar e selecionar colunas
    final_selection = good_houses.sort_values(['zipcode', 'price'])[[
        'price', 'avg_price_region', 'zipcode', 'bedrooms', 
        'bathrooms', 'condition', 'grade', 'view', 'waterfront'
    ]]

    # 5. Calcular ROI
    indices_desejados = [8978, 9077, 7178, 16580, 18102, 434, 8846, 892,
                        19687, 1752, 1868, 11754, 2205, 8676, 3821, 5598,
                        15579, 19367, 20631, 19757]

    final_selection_filtered = final_selection.loc[indices_desejados].copy()
    final_selection_filtered['ROI (%)'] = ((final_selection_filtered['avg_price_region'] - 
                                          final_selection_filtered['price']) / 
                                         final_selection_filtered['price']) * 100

    # --------------------------------------------
    # Gráfico de ROI Original
    # --------------------------------------------
    st.header("Retorno sobre Investimento (ROI)")
    with st.container():
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.scatter(
            range(len(final_selection_filtered.index)),
            final_selection_filtered['ROI (%)'],
            color='#2ecc71',
            s=150,
            alpha=0.7,
            edgecolor='black'
        )
        
        for i, roi in enumerate(final_selection_filtered['ROI (%)']):
            ax.text(
                x=i,
                y=roi + 1.5,
                s=f"{roi:.1f}%",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )
        
        ax.set_ylim(0, final_selection_filtered['ROI (%)'].max() + 10)
        ax.set_title("Potencial de Retorno por Propriedade", fontsize=16, pad=20)
        ax.set_xlabel("Índice da Propriedade", fontsize=12)
        ax.set_ylabel("ROI Esperado (%)", fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_facecolor('#f5f6fa')
        plt.xticks(
            range(len(final_selection_filtered.index)),
            labels=final_selection_filtered.index,
            rotation=45,
            fontsize=10
        )
        st.pyplot(fig)

    # =========================================
    #       NOVOS GRÁFICOS ADICIONADOS
    # =========================================
    
    # Gráfico 1: Comparação de Preços Médios
    st.subheader("📊 Comparação de Preços Médios por Região")
    
    # Cálculo dos preços médios
    region_prices = df.groupby('zipcode')['price'].mean().reset_index()
    region_prices_sorted = region_prices.sort_values(by='price', ascending=False)
    top_10_regions = region_prices_sorted.head(10)

    # Garantir que a região 98001 está incluída
    if 98001 not in top_10_regions['zipcode'].values:
        region_98001 = region_prices[region_prices['zipcode'] == 98001]
        top_10_regions = pd.concat([top_10_regions, region_98001])

    # Configurar cores
    colors = ['#FF6B6B' if zipcode == 98001 else '#4ECDC4' for zipcode in top_10_regions['zipcode']]

    # Plotar com Matplotlib
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(
        top_10_regions['zipcode'].astype(str), 
        top_10_regions['price'],
        color=colors,
        edgecolor='grey'
    )
    
    # Customização do gráfico
    ax1.set_title('Top 10 Regiões com Maiores Preços Médios vs Região 98001', pad=20)
    ax1.set_xlabel('CEP da Região', labelpad=10)
    ax1.set_ylabel('Preço Médio (US$)', labelpad=10)
    ax1.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)
    
    # Gráfico 2: Taxa de Valorização Histórica
    st.subheader("📈 Taxa de Valorização Anual por Região")
    
    # Cálculo da valorização
    price_by_year = df.groupby(['zipcode', 'year'])['price'].mean().reset_index()
    price_by_year['pct_change'] = price_by_year.groupby('zipcode')['price'].pct_change()
    
    # Dados para 98001
    zipcode_98001 = price_by_year[price_by_year['zipcode'] == 98001]
    avg_pct_change_98001 = zipcode_98001['pct_change'].mean()
    
    # Comparação com outras regiões
    comparison = price_by_year.groupby('zipcode')['pct_change'].mean().reset_index()
    comparison = comparison.sort_values('pct_change', ascending=False)
    
    # Criar figura
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Plotar com Seaborn
    sns.barplot(
        data=comparison.head(10),
        x='zipcode',
        y='pct_change',
        palette='Blues_d',
        ax=ax2
    )
    
    # Linha de referência
    ax2.axhline(
        avg_pct_change_98001,
        color='#FF6B6B',
        linestyle='--',
        linewidth=2,
        label=f'CEP 98001 ({avg_pct_change_98001:.1%})'
    )
    
    # Customização
    ax2.set_title('Taxa Média de Valorização Anual Comparativa', pad=15)
    ax2.set_xlabel('CEP da Região', labelpad=10)
    ax2.set_ylabel('Valorização Média Anual', labelpad=10)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig2)

    # Exibir métrica destacada
    st.metric(label="**Valorização Média Anual do CEP 98001**", 
              value=f"{avg_pct_change_98001:.1%}")

    # --------------------------------------------
    # Tabela Interativa
    # --------------------------------------------
    st.header("🔍 Detalhes das Propriedades Selecionadas")

    # Adicionar filtros
    col1, col2 = st.columns(2)
    with col1:
        min_roi = st.slider(
            "Filtrar por ROI Mínimo (%):",
            min_value=0,
            max_value=int(final_selection_filtered['ROI (%)'].max()),
            value=0
        )

    with col2:
        selected_zipcode = st.selectbox(
            "Filtrar por Região:",
            options=['Todas'] + list(final_selection_filtered['zipcode'].unique())
        )

    # Aplicar filtros
    filtered_data = final_selection_filtered
    if selected_zipcode != 'Todas':
        filtered_data = filtered_data[filtered_data['zipcode'] == selected_zipcode]
    filtered_data = filtered_data[filtered_data['ROI (%)'] >= min_roi]

    # Exibir tabela
    st.dataframe(
        filtered_data.style.format({
            'price': '${:,.2f}',
            'avg_price_region': '${:,.2f}',
            'ROI (%)': '{:.1f}%'
        }),
        height=400,
        use_container_width=True
    )

    # Estatísticas Resumidas
    st.subheader("📊 Estatísticas Chave")
    cols = st.columns(3)
    cols[0].metric("Maior ROI", f"{filtered_data['ROI (%)'].max():.1f}%")
    cols[1].metric("ROI Médio", f"{filtered_data['ROI (%)'].mean():.1f}%")
    cols[2].metric("Propriedades Filtradas", filtered_data.shape[0])

# =========================================
#          ABA 3: Melhor Momento para Venda
# =========================================
with tab3:
    st.title("📈 Análise de Sazonalidade")
    st.markdown("---")

    # Criar coluna de ano
    df['year'] = df['date'].dt.year

    anos_disponiveis = sorted(df['year'].unique())
    selected_year = st.selectbox('Selecione o ano', anos_disponiveis)

    df_filtered = df[df['year'] == selected_year].copy()

    if df_filtered.empty:
        st.error(f"Não há dados para o ano {selected_year}.")
    else:
        df_filtered['month'] = df_filtered['date'].dt.month
        monthly_avg_price = df_filtered.groupby('month', as_index=False)['price'].mean()

        if not monthly_avg_price.empty:
            best_month_sell = monthly_avg_price.loc[monthly_avg_price['price'].idxmax()]
            best_month_buy = monthly_avg_price.loc[monthly_avg_price['price'].idxmin()]

            fig = px.line(monthly_avg_price, x='month', y='price', markers=True, title=f'Análise Sazonal de Preços em {selected_year}')
            fig.add_vline(x=best_month_sell['month'], line_dash='dash', line_color='red', annotation_text=f'Melhor Mês para Vender ({int(best_month_sell["month"])})')
            fig.add_vline(x=best_month_buy['month'], line_dash='dash', line_color='green', annotation_text=f'Melhor Mês para Comprar ({int(best_month_buy["month"])})')

            st.plotly_chart(fig)


# =========================================
#         ABA 4: Impacto das Reformas
# =========================================
with tab4:
    st.title("🛠️ Análise do Impacto das Reformas")
    st.markdown("---")

    # ============================
    # 📌 **Casas com Potencial para Reforma**
    # ============================
    st.subheader("🏠 Casas com Potencial para Reforma")

    # Criar a coluna `avg_price_region_log` caso necessário
    if 'avg_price_region_log' not in df.columns:
        df['avg_price_region_log'] = df.groupby('condition')['price'].transform('mean')

    # Filtrar as casas que têm potencial para reforma
    casas_reforma = df[['price', 'avg_price_region_log', 'condition', 'grade']].sort_values('condition')

    # Exibir a tabela no Streamlit
    st.dataframe(casas_reforma)

    # ==============================
    # 📌 **Impacto da Condição e Qualidade**
    # ==============================
    st.subheader("📊 Impacto da Condição e Qualidade no Preço")

    # Calcular impacto da condição no preço
    condition_impact = df.groupby('condition')['price'].mean().reset_index()
    condition_impact.rename(columns={'price': 'avg_price_condition'}, inplace=True)
    condition_impact = condition_impact.sort_values(by='condition')  # Garantir ordem correta

    # Calcular impacto da qualidade (grade) no preço
    grade_impact = df.groupby('grade')['price'].mean().reset_index()
    grade_impact.rename(columns={'price': 'avg_price_grade'}, inplace=True)
    grade_impact = grade_impact.sort_values(by='grade')  # Garantir ordem correta

    col1, col2 = st.columns(2)

    # **Gráfico: Impacto da Condição no Preço**
    with col1:
        fig, ax = plt.subplots(figsize=(8, 6))  # Ajustar tamanho do gráfico
        ax.bar(condition_impact['condition'], condition_impact['avg_price_condition'], color='skyblue')
        ax.set_title("Impacto da Condição no Preço Médio")
        ax.set_xlabel("Condição")
        ax.set_ylabel("Preço Médio (R$)")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.ticklabel_format(style='plain', axis='y')  # Remover notação científica
        st.pyplot(fig)

    # **Gráfico: Impacto da Qualidade no Preço**
    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))  # Ajustar tamanho do gráfico
        ax.bar(grade_impact['grade'], grade_impact['avg_price_grade'], color='salmon')
        ax.set_title("Impacto da Qualidade no Preço Médio")
        ax.set_xlabel("Qualidade (Grade)")
        ax.set_ylabel("Preço Médio (R$)")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.ticklabel_format(style='plain', axis='y')  # Remover notação científica
        st.pyplot(fig)

    # ==============================
    # 📌 **Calcular Incrementos de Preço**
    # ==============================

    # **Adicionar o incremento estimado ao melhorar a condição**
    df = df.merge(condition_impact, on='condition', how='left')
    df['price_increment_condition'] = df['avg_price_condition'] - df['price']

    # **Adicionar o incremento estimado ao melhorar a qualidade**
    df = df.merge(grade_impact, on='grade', how='left')
    df['price_increment_grade'] = df['avg_price_grade'] - df['price']

    # **Gerar a tabela de sugestões de melhoria**
    improvement_suggestions = df[['condition', 'grade', 'price_increment_condition', 'price_increment_grade']].sort_values(
        by=['price_increment_condition', 'price_increment_grade'], ascending=False
    )

    # ==============================
    # 📌 **Incremento do Preço por Condição e Qualidade**
    # ==============================
    st.subheader("📈 Incremento do Preço por Melhoria de Condição e Qualidade")

    # Selecionar as 10 casas com maior impacto na reforma
    top_improvements = improvement_suggestions.head(10)

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criar o gráfico de barras comparando os incrementos
    sns.barplot(data=top_improvements, 
                x='condition', 
                y='price_increment_condition', 
                color='skyblue', 
                label='Incremento pela Condição', 
                alpha=0.7, ax=ax)

    sns.barplot(data=top_improvements, 
                x='condition', 
                y='price_increment_grade', 
                color='orange', 
                label='Incremento pela Qualidade (Grau)', 
                alpha=0.7, ax=ax)

    # Adicionando título e rótulos
    ax.set_title('Incremento no Preço de Casas por Melhoria de Condição e Qualidade (Grau)', fontsize=14)
    ax.set_xlabel('Condição', fontsize=12)
    ax.set_ylabel('Incremento no Preço (R$)', fontsize=12)
    ax.legend(title='Tipo de Melhoria')

    # Ajustando o layout
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    # ==============================
    # 📌 **Percentual de Aumento Pós-Reforma**
    # ==============================
    st.subheader("📊 Percentual de Aumento do Valor Potencial Pós-Reforma")

    # Dados fornecidos
    top_10_pos_reforma = pd.DataFrame({
        'price': [7062500.0, 5570000.0, 5350000.0, 5110800.0, 4668000.0, 4500000.0, 4489000.0, 4208000.0, 3800000.0, 4000000.0],
        'preco_pos_reforma': [13418750.0, 11697000.0, 10700000.0, 10221600.0, 9336000.0, 9000000.0, 8978000.0, 8416000.0, 8360000.0, 8000000.0],
        'price_increment_condition': [1412500.0, 1114000.0, 1070000.0, 1022160.0, 933600.0, 900000.0, 897800.0, 841600.0, 1140000.0, 800000.0],
        'price_increment_grade': [4943750.0, 5013000.0, 4280000.0, 4088640.0, 3734400.0, 3600000.0, 3591200.0, 3366400.0, 3420000.0, 3200000.0]
    }, index=[3801, 4280, 1414, 1139, 7878, 2556, 8401, 12031, 6847, 4025])

    # Calcular o percentual de aumento para cada casa
    top_10_pos_reforma['percentual_aumento'] = (
        (top_10_pos_reforma['preco_pos_reforma'] - top_10_pos_reforma['price']) / top_10_pos_reforma['price'] * 100
    )

    # Garantir que os índices sejam strings para o eixo X
    top_10_pos_reforma = top_10_pos_reforma.reset_index()
    top_10_pos_reforma.rename(columns={'index': 'indice'}, inplace=True)
    top_10_pos_reforma['indice'] = top_10_pos_reforma['indice'].astype(str)

    # Criar o gráfico de barras com tamanho e DPI ajustados
    fig, ax = plt.subplots(figsize=(12, 6), dpi=80)  # Tamanho menor e DPI ajustado

    # Plotar o gráfico de barras
    sns.barplot(
        x=top_10_pos_reforma['indice'], 
        y=top_10_pos_reforma['percentual_aumento'], 
        palette='viridis', dodge=False, ax=ax
    )

    # Adicionar rótulos com o valor pós-reforma no topo das barras
    for i, row in top_10_pos_reforma.iterrows():
        ax.text(i, row['percentual_aumento'] + 2, f"R${row['preco_pos_reforma']:,.0f}", ha='center', fontsize=9)

    # Configurar título, eixos e limites
    ax.set_title('Percentual de Aumento do Valor Potencial Pós-Reforma', fontsize=14)
    ax.set_xlabel('Casas (Índice)', fontsize=12)
    ax.set_ylabel('Percentual de Aumento (%)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar layout para Streamlit
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


# =========================================
#         ABA 5: Análise Geográfica
# =========================================
with tab5:
    st.title("🏡 Análise Geográfica ")
    st.markdown("---")

    # Carregar os dados
    df = pd.read_csv("kc_house_data_updat.csv")
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['year'] = df['date'].dt.year

    # Calcular a média de preço por região
    df['avg_price_region'] = df.groupby('zipcode')['price'].transform('mean')  

    # Filtrar as melhores casas abaixo do preço médio
    below_avg_price = df['price'] < df['avg_price_region']  
    best_houses = df[below_avg_price & (df['condition'] >= 3) & (df['grade'] >= 7)]

    # Criar um mapa interativo com PyDeck
    st.write("### Mapa Interativo das Casas com Melhor Custo-Benefício")
    layer = pdk.Layer(
        "ScatterplotLayer",
        best_houses,
        get_position=["long", "lat"],
        get_color=[0, 0, 255, 140],
        get_radius=100,
        pickable=True,
        tooltip=True,
    )
    view_state = pdk.ViewState(
        latitude=df['lat'].mean(),
        longitude=df['long'].mean(),
        zoom=10,
        pitch=0,
    )
    r = pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Preço:</b> ${price}<br><b>Média da Região:</b> ${avg_price_region}<br><b>Condição:</b> {condition}<br><b>Quartos:</b> {bedrooms}<br><b>Banheiros:</b> {bathrooms}",
            "style": {"color": "white"}
        }
    )
    st.pydeck_chart(r)

    # Mostrar DataFrame com os imóveis selecionados
    st.write("### Casas Selecionadas para Compra")
    st.dataframe(best_houses[['price', 'avg_price_region', 'zipcode', 'bedrooms', 'bathrooms', 'condition', 'grade', 'view', 'waterfront']].head(20))

# =========================================
#         ABA 6: Insights 
# =========================================

with tab6:
    st.title("📊 Insights e Recomendações")
    st.markdown("---")
    
    st.subheader("Insight Geral")
    st.write("O CEO da House Rocket pode focar em adquirir imóveis que ofereçam boas características (qualidade de construção e condições favoráveis) a preços abaixo da média regional. As casas recomendadas para compra, localizadas no CEP 98001, apresentam preços abaixo da média regional, o que representa uma excelente oportunidade de investimento, com boas margens de valorização. As propriedades são consistentes em termos de características, com predominância de 3 ou 4 quartos e pelo menos 2 banheiros, o que atende a uma grande demanda do mercado, especialmente para famílias.")

    st.subheader("Valorização e Reforma")
    st.write("Com relação ao impacto das reformas, é importante considerar que melhorias na qualidade (grau) têm um impacto muito maior no preço do que as melhorias na condição do imóvel. As reformas de qualidade podem resultar em aumentos significativos no valor das propriedades, especialmente para casas com classificação baixa, como grau 5, que podem ser elevadas para grau 6, com um incremento médio no preço de até $219.000.")

    st.subheader("Melhor Momento para Venda e Compra")
    st.write("A análise sazonal revela que o melhor mês para vender é abril, quando os preços médios atingem seu pico, e o melhor mês para compra é Dezembro a Fevereiro. Isso indica uma janela estratégica para maximizar o lucro na revenda das propriedades adquiridas.")

    st.subheader("Conclusões e Recomendações")
    st.write("- Investimento em imóveis abaixo da média regional, como os encontrados no CEP 98001, oferece uma boa margem de lucro.")
    st.write("- Reformas focadas na qualidade (grau) são mais rentáveis e devem ser priorizadas, pois têm um impacto substancial no preço.")
    st.write("- Monitorar o mercado e vender em abril pode otimizar os retornos, aproveitando a valorização sazonal do mercado imobiliário.")
    st.write("Com essas estratégias, o CEO da House Rocket pode maximizar seus lucros, investindo em propriedades com alto potencial de valorização e aproveitando as melhores condições do mercado.")
