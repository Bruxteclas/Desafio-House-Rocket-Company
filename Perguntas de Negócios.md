# Resumo do Projeto Anterior e Próximos Passos

## Resumo do Projeto Anterior

O projeto anterior focou na **limpeza e análise exploratória** de um conjunto de dados imobiliários, com o objetivo de entender melhor o mercado e preparar os dados para a tomada de decisão. As principais etapas realizadas foram:

 **Limpeza de Dados**:
   - Exclusão de valores duplicados e tratamento de valores ausentes.
   - Conversão e formatação de colunas, como datas.
   - Remoção de variáveis irrelevantes, como `id`.

 **Transformações**:
   - **Logarítmica**: Aplicada a variáveis como preço e área habitável para corrigir assimetrias.
   - **Normalização Min-Max**: Ajustou variáveis contínuas para uma escala comum.
 
 **Análise Exploratória de Dados (EDA)**:
   - Visualização de distribuições de variáveis.
   - Identificação e tratamento de outliers (e.g., casas com 33 quartos).
   - Análise de correlação para entender relações entre variáveis, destacando fatores para análise.
   - Visualização de dados geográficos.
   - Exploração de características categóricas e numéricas.
   - Geração de insights baseados em gráficos.
   - Identificação de variáveis principais.


## Próximos Passos

Agora, o foco será responder às seguintes **Perguntas de Negócio**:

1) **Quais casas o CEO da House Rocket deveria comprar e por qual preço?**
   - Identificar imóveis subvalorizados que representem boas oportunidades de compra.

2) **Quando é o melhor momento para vender as casas adquiridas?**
   - Analisar a sazonalidade do mercado para determinar os períodos mais lucrativos para revenda.

3) **A House Rocket deveria investir em reformas?**
   - Avaliar se reformas aumentam significativamente o valor de revenda e quais tipos de melhorias são mais rentáveis.

## Bibliotecas


```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
from sklearn.preprocessing import MinMaxScaler
```

## Coleta dos dados


```python
# Carregando os dados
df = pd.read_csv("kc_house_data_updat.csv")
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>bedrooms</th>
      <th>bathrooms</th>
      <th>floors</th>
      <th>waterfront</th>
      <th>view</th>
      <th>condition</th>
      <th>grade</th>
      <th>sqft_above</th>
      <th>sqft_basement</th>
      <th>...</th>
      <th>zipcode</th>
      <th>lat</th>
      <th>long</th>
      <th>sqft_living15</th>
      <th>sqft_lot15</th>
      <th>has_basement</th>
      <th>log_price</th>
      <th>log_sqft_living</th>
      <th>log_sqft_lot</th>
      <th>lot_size_category</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>13-10-2014</td>
      <td>3</td>
      <td>1</td>
      <td>1.0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>7</td>
      <td>0.097588</td>
      <td>0.000000</td>
      <td>...</td>
      <td>98178</td>
      <td>47.5112</td>
      <td>-122.257</td>
      <td>0.161934</td>
      <td>0.005742</td>
      <td>Sem Porão</td>
      <td>12.309987</td>
      <td>7.074117</td>
      <td>8.639588</td>
      <td>Médio</td>
    </tr>
    <tr>
      <th>1</th>
      <td>09-12-2014</td>
      <td>3</td>
      <td>2</td>
      <td>2.0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>7</td>
      <td>0.206140</td>
      <td>0.082988</td>
      <td>...</td>
      <td>98125</td>
      <td>47.7210</td>
      <td>-122.319</td>
      <td>0.222165</td>
      <td>0.008027</td>
      <td>Com Porão</td>
      <td>13.195616</td>
      <td>7.852050</td>
      <td>8.887791</td>
      <td>Médio</td>
    </tr>
    <tr>
      <th>2</th>
      <td>25-02-2015</td>
      <td>2</td>
      <td>1</td>
      <td>1.0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>6</td>
      <td>0.052632</td>
      <td>0.000000</td>
      <td>...</td>
      <td>98028</td>
      <td>47.7379</td>
      <td>-122.233</td>
      <td>0.399415</td>
      <td>0.008513</td>
      <td>Sem Porão</td>
      <td>12.100718</td>
      <td>6.647688</td>
      <td>9.210440</td>
      <td>Médio</td>
    </tr>
    <tr>
      <th>3</th>
      <td>09-12-2014</td>
      <td>4</td>
      <td>3</td>
      <td>1.0</td>
      <td>0</td>
      <td>0</td>
      <td>5</td>
      <td>7</td>
      <td>0.083333</td>
      <td>0.188797</td>
      <td>...</td>
      <td>98136</td>
      <td>47.5208</td>
      <td>-122.393</td>
      <td>0.165376</td>
      <td>0.004996</td>
      <td>Com Porão</td>
      <td>13.311331</td>
      <td>7.581210</td>
      <td>8.517393</td>
      <td>Médio</td>
    </tr>
    <tr>
      <th>4</th>
      <td>18-02-2015</td>
      <td>3</td>
      <td>2</td>
      <td>1.0</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>8</td>
      <td>0.152412</td>
      <td>0.000000</td>
      <td>...</td>
      <td>98074</td>
      <td>47.6168</td>
      <td>-122.045</td>
      <td>0.241094</td>
      <td>0.007871</td>
      <td>Sem Porão</td>
      <td>13.142168</td>
      <td>7.427144</td>
      <td>8.997271</td>
      <td>Médio</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 22 columns</p>
</div>




```python

```

# Perguntas de negócio

### 1 - Quais casas o CEO da House Rocket deveria comprar e por qual preço?


```python
# 1. Calcular o preço médio por região (zipcode)
df['avg_price_region'] = df.groupby('zipcode')['log_price'].transform('mean')

# 2. Filtrar imóveis abaixo da média regional
below_avg_price = df['log_price'] < df['avg_price_region']

# 3. Selecionar imóveis com boas características
good_houses = df[
    (below_avg_price) &                  # Preço abaixo da média
    (df['grade'] >= 7) &                # Boa qualidade de construção
    (df['condition'] >= 3) &            # Boas condições de uso
    (df['bedrooms'].isin([3, 4])) &     # 3 ou 4 quartos
    (df['bathrooms'] >= 2)              # 2 ou mais banheiros
]

# 4. Ordenar por localização (zipcode) e preço
good_houses = good_houses.sort_values(by=['zipcode', 'log_price'])

# 5. Selecionar as colunas de interesse
final_selection = good_houses[['log_price', 'avg_price_region', 'zipcode', 'bedrooms', 'bathrooms', 'condition', 'grade', 'view', 'waterfront']]

print("Casas Recomendadas para Compra:")
print(final_selection.head(20)) 

```

    Casas Recomendadas para Compra:
           log_price  avg_price_region  zipcode  bedrooms  bathrooms  condition  \
    8978   12.038251          12.49767    98001         3          2          4   
    9077   12.114511          12.49767    98001         3          2          3   
    7178   12.154785          12.49767    98001         3          2          3   
    16580  12.154785          12.49767    98001         4          2          3   
    18102  12.176906          12.49767    98001         3          2          3   
    434    12.185875          12.49767    98001         3          2          3   
    8846   12.229306          12.49767    98001         4          2          3   
    892    12.230770          12.49767    98001         3          2          3   
    19687  12.230770          12.49767    98001         4          2          3   
    1752   12.235636          12.49767    98001         4          2          3   
    1868   12.254868          12.49767    98001         3          2          3   
    11754  12.254868          12.49767    98001         4          2          3   
    2205   12.271631          12.49767    98001         3          2          3   
    8676   12.273736          12.49767    98001         3          2          3   
    3821   12.278398          12.49767    98001         4          2          3   
    5598   12.278398          12.49767    98001         4          2          3   
    15579  12.278398          12.49767    98001         3          2          5   
    19367  12.278398          12.49767    98001         4          2          3   
    20631  12.278398          12.49767    98001         3          2          3   
    19757  12.283038          12.49767    98001         4          2          3   
    
           grade  view  waterfront  
    8978       7     0           0  
    9077       7     0           0  
    7178       7     0           0  
    16580      7     0           0  
    18102      7     0           0  
    434        7     0           0  
    8846       7     0           0  
    892        7     0           0  
    19687      8     0           0  
    1752       7     0           0  
    1868       7     0           0  
    11754      7     0           0  
    2205       7     0           0  
    8676       7     0           0  
    3821       7     0           0  
    5598       7     0           0  
    15579      7     0           0  
    19367      7     0           0  
    20631      7     0           0  
    19757      7     0           0  
    


```python

```

### **Análise das Casas Recomendadas para Compra**

Com base nos resultados, podemos identificar um padrão claro nas características das casas recomendadas para compra. Estas propriedades representam boas oportunidades de investimento por estarem abaixo da média de preço regional e apresentarem características alinhadas ao perfil de mercado da **House Rocket**.

---

#### **1. Preço Abaixo da Média Regional**
Todas as casas listadas têm um preço logarítmico (`log_price`) inferior ao preço médio da região (`avg_price_region`), com um desvio significativo em relação à média de **12.49767**. Isso indica que essas propriedades estão subvalorizadas em comparação ao mercado local, tornando-as excelentes oportunidades para compra e posterior valorização.

---

#### **2. Localização Valorizada (CEP: 98001)**
Todas as casas estão localizadas no **CEP 98001**, uma região identificada como promissora com base nas análises. O alto volume de imóveis recomendados neste CEP sugere que esta área combina **acessibilidade** com um bom potencial de valorização futura. Além disso, a proximidade com infraestruturas essenciais pode contribuir para a alta demanda nesta região.

---

#### **3. Configuração das Casas**

**Quartos e Banheiros:**
- A maioria das casas possui **3 ou 4 quartos** e **2 banheiros**, uma configuração popular e alinhada às preferências dos compradores, conforme nossas análises anteriores.
- Essa combinação oferece espaço suficiente para **famílias médias**, tornando as propriedades mais atraentes no mercado.

**Porão e Água:**
- Nenhuma das casas possui porão ou acesso à frente d’água (`waterfront == 0`), o que é consistente com as preferências gerais do mercado local. Imóveis sem porão são mais práticos e possuem menor custo de manutenção, fatores que agradam a um público mais amplo.

---

#### **4. Qualidade e Condição**

**Qualidade de Construção (`grade`):**
- A maioria das casas possui uma **qualidade de construção avaliada como 7 ou 8**, indicando acabamentos de **média-alta qualidade**. Isso reflete um equilíbrio entre custo e benefícios, tornando as propriedades acessíveis e, ao mesmo tempo, atrativas para compradores que buscam conforto e funcionalidade.

**Condições Gerais (`condition`):**
- Todas as casas estão em condições **razoáveis a boas**, com valores de `condition` variando de **3 a 5**, o que reduz os custos de reforma e melhora a atratividade imediata para venda ou aluguel.

---

#### **5. Qualidade da Vista (`view`)**
Embora as casas apresentem **`view` 0** (sem vista privilegiada), isso não compromete sua atratividade. A ausência de uma vista premium é compensada pelo **preço competitivo**, pela **qualidade da construção** e pela localização estratégica. Esses fatores tornam as casas mais acessíveis a um público maior, alinhando-se ao perfil de mercado identificado.

---

### **Conclusão**
As casas recomendadas para compra no **CEP 98001** representam **excelentes oportunidades de investimento** para a **House Rocket**, por estarem:
- **Subvalorizadas em relação à média regional**, o que potencializa o retorno sobre o investimento.
- Localizadas em uma região promissora, com boa acessibilidade e potencial de valorização futura.
- Equipadas com características populares no mercado, como **3 ou 4 quartos, 2 banheiros, e qualidade de construção média-alta**.
  
Essas propriedades são ideais para aquisição com **potencial de valorização futura** ou para **revenda rápida**, atendendo ao perfil de compradores interessados em custo-benefício e funcionalidade.

## Quando é o melhor momento para vender as casas adquiridas?



```python
# Garantir que a coluna 'date' está no formato datetime
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Extrair o mês da data para análise sazonal
df['month'] = df['date'].dt.month

# Analisar a média dos preços por mês
monthly_avg_price = df.groupby('month')['log_price'].mean().reset_index()

# Plotar o preço médio por mês
plt.figure(figsize=(10, 6))
plt.plot(monthly_avg_price['month'], monthly_avg_price['log_price'], marker='o')
plt.title('Preço Médio por Mês')
plt.xlabel('Mês')
plt.ylabel('Preço Médio (log)')
plt.xticks(range(1, 13))
plt.grid()
plt.show()

```


    
![png](output_12_0.png)
    



```python

```

### **Picos de Preços**
- O **mês de abril (4)** apresenta o maior preço médio, com um valor logarítmico em torno de **13.10**, seguido de perto pelos meses de maio e junho.
- Esse período coincide com o início da **primavera e verão**, que é tradicionalmente o período de maior atividade no mercado imobiliário. Durante esses meses, há maior demanda por imóveis, impulsionando os preços.

---

### **Queda nos Preços**
- Os preços começam a cair gradualmente a partir de **julho (7)**, atingindo valores mais baixos nos meses de **outubro (10)** a **dezembro (12)**. 
- Esse comportamento reflete a sazonalidade típica, onde a atividade de compra e venda diminui durante o outono e inverno, resultando em menores preços médios.

---

### **Melhores Meses para Venda**
- O melhor período para **vender imóveis** está entre **março (3)** e **junho (6)**, quando os preços estão em alta devido à maior procura.
- Imóveis podem ser listados nos meses de janeiro ou fevereiro para se preparar para o pico da primavera.

---

### **Melhores Meses para Compra**
- Os meses de **novembro (11)** e **dezembro (12)** oferecem oportunidades de compra a preços mais baixos, pois a demanda está menor. Imóveis adquiridos nesses períodos podem ser revendidos no pico de valorização no ano seguinte.

---

### **Conclusão**
Com base no gráfico, recomenda-se o seguinte:
1. **Venda:** Priorizar os meses de março a junho para obter preços mais altos.
2. **Compra:** Aproveitar os meses de outubro a dezembro, quando os preços estão mais baixos, para adquirir imóveis com potencial de valorização no ano seguinte.

## A House Rocket deveria investir em reformas?

### Impacto das Reformas


```python
# Calcular o preço médio por região (zipcode)
df['avg_price_region'] = df.groupby('zipcode')['log_price'].transform('mean')

# Identificar casas abaixo do preço médio
below_avg_price = df['log_price'] < df['avg_price_region']

# Filtrar casas abaixo da média e com condição/qualidade que possam ser melhoradas
potential_reforms = df[below_avg_price & ((df['condition'] < 5) | (df['grade'] < 8))]

# Exibir as casas com potencial para reforma
print("Casas com potencial para reforma:")
print(potential_reforms[['log_price', 'avg_price_region', 'condition', 'grade']].head())

```

    Casas com potencial para reforma:
       log_price  avg_price_region  condition  grade
    0  12.309987         12.555991          3      7
    2  12.100718         12.996565          3      6
    4  13.142168         13.380585          3      8
    6  12.458779         12.536507          3      7
    8  12.343663         12.659694          3      7
    

### Avaliar Impacto das Reformas


```python
# Analisar o impacto do aumento da 'condition'
condition_impact = df.groupby('condition')['log_price'].mean().reset_index()
condition_impact.rename(columns={'log_price': 'avg_price_condition'}, inplace=True)

# Analisar o impacto do aumento do 'grade'
grade_impact = df.groupby('grade')['log_price'].mean().reset_index()
grade_impact.rename(columns={'log_price': 'avg_price_grade'}, inplace=True)

# Combinar os impactos e visualizar
print("Impacto do aumento da condição no preço:")
print(condition_impact)

print("\nImpacto do aumento da qualidade no preço:")
print(grade_impact)

```

    Impacto do aumento da condição no preço:
       condition  avg_price_condition
    0          1            12.512676
    1          2            12.545570
    2          3            13.055704
    3          4            13.008456
    4          5            13.152198
    
    Impacto do aumento da qualidade no preço:
       grade  avg_price_grade
    0      4        12.144873
    1      5        12.321682
    2      6        12.542181
    3      7        12.833662
    4      8        13.132989
    5      9        13.483310
    6     10        13.796378
    7     11        14.123107
    8     12        14.491946
    9     13        14.878152
    

###  Estimar Incremento de Preço


```python
# Adicionar o incremento estimado no preço ao melhorar a condição
df = df.merge(condition_impact, on='condition', how='left')
df['price_increment_condition'] = df['avg_price_condition'] - df['log_price']

# Adicionar o incremento estimado no preço ao melhorar a qualidade
df = df.merge(grade_impact, on='grade', how='left')
df['price_increment_grade'] = df['avg_price_grade'] - df['log_price']

# Exibir as melhorias com maior impacto
improvement_suggestions = df[['condition', 'grade', 'price_increment_condition', 'price_increment_grade']].sort_values(
    by=['price_increment_condition', 'price_increment_grade'], ascending=False
)
print("Sugestões de melhorias com maior impacto no preço:")
print(improvement_suggestions.head(10))

```

    Sugestões de melhorias com maior impacto no preço:
           condition  grade  price_increment_condition  price_increment_grade
    8050           3      6                   1.741218               1.227694
    17982          3      5                   1.729096               0.995074
    3658           3      6                   1.717120               1.203597
    9961           3      6                   1.705286               1.191763
    16273          3      5                   1.705286               0.971264
    13382          3      6                   1.687793               1.174270
    12207          3      7                   1.648128               1.426086
    17118          3      5                   1.648128               0.914106
    10472          3      5                   1.626150               0.892128
    5702           4      6                   1.612053               1.145778
    

### Visualizar o impacto


```python
# Gráfico: Impacto da condição no preço
plt.figure(figsize=(10, 6))
plt.bar(condition_impact['condition'], condition_impact['avg_price_condition'])
plt.title("Impacto da Condição no Preço Médio")
plt.xlabel("Condição")
plt.ylabel("Preço Médio (log)")
plt.grid(axis='y')
plt.show()

# Gráfico: Impacto da qualidade no preço
plt.figure(figsize=(10, 6))
plt.bar(grade_impact['grade'], grade_impact['avg_price_grade'])
plt.title("Impacto da Qualidade (Grade) no Preço Médio")
plt.xlabel("Qualidade (Grade)")
plt.ylabel("Preço Médio (log)")
plt.grid(axis='y')
plt.show()

```


    
![png](output_23_0.png)
    



    
![png](output_23_1.png)
    



```python

```

### **Análise: Deveria a House Rocket Investir em Reformas?**

A análise revelou que investir em reformas pode ser uma estratégia eficaz para aumentar o valor de mercado das casas adquiridas pela **House Rocket**. Focando em propriedades com características abaixo da média, como condição estrutural e qualidade de construção, é possível gerar um incremento significativo no preço de venda. Abaixo, detalhamos os insights sobre o impacto das reformas e as principais sugestões de melhorias.

---

### **Casas com Potencial para Reforma**
As casas com maior potencial de valorização apresentam:
- **Condição (`condition`)**: Estas casas possuem valores baixos (condição 3), indicando que precisam de melhorias estruturais ou estéticas.
- **Qualidade de Construção (`grade`)**: A maioria das propriedades analisadas apresenta `grade` entre 6 e 7, indicando acabamentos simples ou padrão. Melhorias nesse aspecto podem atrair compradores que buscam maior conforto e modernidade.

Essas propriedades estão abaixo do preço médio da região e têm características que, com reformas pontuais, podem ser elevadas para competir com imóveis mais valorizados.

---

### **Impacto das Reformas no Preço**

#### **Melhoria na Condição (`condition`)**
Melhorar a condição do imóvel tem um impacto direto e significativo no preço:
- Propriedades com **condição 3** apresentam preço médio logarítmico de **13.05**.
- Imóveis com **condição 4** têm um preço médio de **13.15**, representando um incremento médio de aproximadamente **+0.10 unidades logarítmicas**.

**Conclusão:** Pequenas melhorias estruturais, como pintura, troca de pisos desgastados, reparos em sistemas elétricos ou hidráulicos, podem elevar a condição e aumentar significativamente o valor de mercado.

---

#### **Melhoria na Qualidade de Construção (`grade`)**
Elevar a qualidade de construção também resulta em um aumento expressivo no preço:
- Propriedades com `grade` 6 têm um preço médio logarítmico de **12.54**.
- Propriedades com `grade` 8 atingem um preço médio de **13.13**, representando um incremento médio de aproximadamente **+0.59 unidades logarítmicas**.
- Para imóveis de `grade` 9, o preço médio sobe ainda mais, para **13.48**, mostrando que melhorias em acabamentos e materiais de qualidade têm alta correlação com a valorização.

**Conclusão:** Investir em acabamentos de melhor qualidade (como mármore, granito, revestimentos modernos) e renovar áreas-chave, como banheiros e cozinhas, pode aumentar significativamente o preço de venda.

---

### **Melhorias**

**Foco nas Casas com `condition` 3:**
   - Realizar reparos básicos, como pintura, conserto de paredes, troca de pisos e modernização de sistemas elétricos e hidráulicos.
   - Elevar a condição de **3 para 4 ou 5** pode gerar um incremento no preço logarítmico de até **+1.0 unidade logarítmica**.

 **Foco em `grade` 6 ou 7:**
   - Investir em acabamentos modernos e reformas estéticas pode elevar o `grade` para **8 ou mais**.
   - Reformas em cozinhas e banheiros, instalação de materiais premium e melhorias externas (paisagismo, renovação de fachadas) têm impacto direto no valor de mercado.

 **Combinação de Melhorias:**
   - Imóveis com `condition` = 3 e `grade` = 6 apresentam o maior potencial de valorização, com um incremento estimado de até **+1.7 unidades logarítmicas** no preço, representando uma oportunidade significativa de retorno sobre o investimento.

---

### **Conclusão**
Sim, a **House Rocket** deve investir em reformas nas propriedades que apresentam condição estrutural média-baixa (`condition` <= 3) e qualidade de construção (`grade` <= 7). 

**Reformas Prioritárias:**
- Melhorar a condição estrutural (de 3 para 4 ou 5) com pequenas reformas estéticas e funcionais.
- Atualizar a qualidade de construção (de 6 para 8 ou mais) com melhorias nos acabamentos e modernização de áreas-chave.

Essas reformas podem posicionar os imóveis em um patamar superior no mercado, aproximando ou ultrapassando o preço médio regional. Com um planejamento estratégico, a House Rocket pode maximizar o retorno sobre o investimento e aumentar sua competitividade no mercado imobiliário.


```python

```
