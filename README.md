# 🚀 **House Rocket - Análise Imobiliária com Dados**

**Web Site:** [Analysis Results](https://desafio-house-rocket-company-ry72wjvngckmrxxrwsomsj.streamlit.app/)

## 📚 **Visão Geral**

O House Rocket é um projeto baseado em análise de dados históricos de vendas de imóveis. O objetivo é usar essas informações para identificar as melhores oportunidades de compra de imóveis, determinar o momento ideal para vendê-los e analisar o impacto de reformas no valor das propriedades.

![Captura de tela 2025-01-31 150918](https://github.com/user-attachments/assets/207c0997-91a7-4e93-8612-7afb3272e822)

## 💡 **Objetivo**

O objetivo principal do projeto é utilizar os dados para tomar decisões estratégicas que maximizem o retorno sobre o investimento em imóveis. As questões abordadas incluem:

1. **Quais imóveis o CEO da House Rocket deve comprar e por qual preço?**
2. **Quando é o melhor momento para vender as propriedades adquiridas?**
3. **Investir em reformas? Se sim, quais melhorias são mais rentáveis?**

## 🔧 **Tecnologias e Ferramentas Utilizadas**

Este projeto foi desenvolvido com Python e utiliza várias bibliotecas poderosas para análise de dados e visualizações, incluindo:

- **Pandas**: Manipulação e análise de dados.
- **Matplotlib & Seaborn**: Criação de gráficos e visualizações interativas.
- **NumPy**: Funções matemáticas e operações com arrays.
- **Scikit-learn**: Pré-processamento de dados, incluindo normalização e transformação logarítmica.`

### 🗂 **Descrição de arquivos**

- **Conjunto de Dados/**: Contém os arquivos de dados brutos e processados.
- **notebooks/**: Jupyter Notebooks para limpeza de dados, EDA e análise de oportunidades.

### **Entendimento dos dados:**

| Coluna            | Descrição                                                                           |
|--------------------|-------------------------------------------------------------------------------------|
| id                | Identificação única da casa.                                                       |
| date              | Data da venda.                                                                     |
| price             | Preço da casa.                                                                     |
| bedrooms          | Número de quartos.                                                                 |
| bathrooms         | Número de banheiros.                                                               |
| sqft_living       | Área habitável em pés quadrados.                                                   |
| sqft_lot          | Tamanho do terreno em pés quadrados.                                               |
| floors            | Número de andares.                                                                 |
| waterfront        | Indicador de proximidade à água (0 = não, 1 = sim).                                |
| view              | Qualidade da vista                                                                 |
| Grade             | Classificação da qualidade de construção (1-13).                                   |
| Condition         | condição física geral do imóvel                                                    |
| sqft_above        | pés quadrados_acima                                                                |
| sqft_basement	    | porão de pés quadrados                                                             |       
| yr_built          | Ano de construção.                                                                 |
| yr_renovated      | Ano de renovação (0 se nunca foi renovada).                                        |
| zipcode           | CEP da localização.                                                                |
| lat, long         | Coordenadas geográficas.                                                           |
| sqft_living15     | Área habitável de 15 vizinhos próximos, em pés quadrados.                          |
| sqft_lot15        | Área do terreno de 15 vizinhos próximos, em pés quadrados.                         |


---

## 📝 **Etapas Realizadas no Projeto**

### 1️⃣ **Carregamento e Limpeza de Dados**
Os dados brutos foram carregados e processados para garantir que estavam em um formato adequado para análise:
- Remoção de valores duplicados e ausentes.
- Conversão de colunas de data e de variáveis numéricas.
- Exclusão de variáveis irrelevantes, como `id`.

### 2️⃣ **Análise Exploratória de Dados (EDA)**
Realizou-se uma análise exploratória para entender as principais características dos dados, como:
- **Distribuição de preços, áreas e características dos imóveis**.
- **Identificação de outliers** e tratamento de valores extremos.
- **Análise de correlação** entre variáveis (como qualidade e condição do imóvel versus preço).
- **Características de Mercado** análise geográfica e preferências características mais valorizadas pelos compradores de imóveis

### 3️⃣ **Identificação de Oportunidades de Compra**
As casas com características favoráveis e preço abaixo da média regional foram filtradas:
- Seleção de imóveis com **boa condição** e **boa qualidade** de construção.
- Identificação de imóveis **subvalorizados** com potencial de valorização.

### 4️⃣ **Análise de Impacto das Reformas**
Foi realizado um estudo sobre como reformas na condição e qualidade do imóvel podem impactar seu valor de revenda:
- O impacto da **condição** e **qualidade (grau)** no preço foi estimado.
- Identificação de **imóveis com potencial para reforma**, que poderiam gerar lucro após melhorias.

### 5️⃣ **Análise Sazonal**
Analisou-se o comportamento do mercado ao longo dos meses para identificar os melhores períodos para venda:
- **Preço médio por mês** para identificar os meses com maior valorização.

---

## 📊 **Resultados e Insights**

### 🔑 **Casas Recomendadas para Compra**

Casas no **CEP 98001** foram identificadas como as melhores oportunidades de compra, com preços abaixo da média regional. Características dessas casas incluem:
- **Preço entre $169.100 a $216.000**.
- **3 ou 4 quartos** e **2 ou mais banheiros**.
- **Boa condição e qualidade de construção (grau 7-8)**.

### 📅 **Melhor Mês para Venda**
O **melhor mês para vender** foi identificado como **abril**, com o preço médio mais alto de **$559.208,53**.

### 🛠 **Impacto das Reformas**
A análise mostrou que **melhorias na qualidade (grau)** aumentam significativamente o valor das casas, mais do que as melhorias na **condição**. Em média, melhorar o grau de construção pode resultar em aumentos de até **$3.000.000**.

---

## 🤝 **Contribua**

Sinta-se à vontade para contribuir para o projeto:
- **Reportar bugs** ou **propor melhorias**.
- **Fazer Fork** e adicionar novas funcionalidades ou otimizações.
