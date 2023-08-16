
![Combustivel](https://adaptive.com.br/wp-content/uploads/2020/04/Como-evitar-problemas-de-abastecimento-img_1.jpg)


# <center> <font color = 'royalblue'> Dados para abastecer o carro </font> </center>


## <center> <font color = 'goldenrod'> Análise exploratória relacionada à série histórica de preço de venda dos combustíveis </font> </center>

Este projeto foi desenvolvido pelo Squad 8 do Módulo 4 do curso Data Analytics da Resília Educação em parceria com o iFood. Aplicando a Metodologia Ágil Scrum e a organização por funções proposto pela Resília, seguem os papéis desempenhados:

[Aron Bernardo](https://www.linkedin.com/in/aron-bernardo-data-analytics/) - Product Owner / Co-Facilitador

[David Williams](https://www.linkedin.com/in/david-williams-pyrrho/) - Scrum Master / Gestor de Conhecimento

[Luciana Nunes](https://www.linkedin.com/in/luhonunes/) - Equipe de Desenvolvimento / Gestora de Gente e Engajamento

[Michael Barbosa](https://www.linkedin.com/in/michaelbcleite/) - Equipe de Desenvolvimento / Colaborador

Neste projeto, fomos designados pela Agência Nacional de Petróleo e Gás Natural e Biocombustíveis (ANP) para conduzir uma análise exploratória das séries históricas de preço de venda dos combustíveis no Brasil. A ANP é uma instituição de referência quando se trata de dados e informações sobre a indústria de petróleo e gás em nosso país. A agência desempenha um papel crucial ao manter o Banco de Dados de Exploração e Produção (BDEP), além de fornecer estatísticas oficiais sobre reservas, refino, produção de petróleo, gás e biocombustíveis, promovendo pesquisas sobre qualidade de combustíveis e lubrificantes, comportamento de preços e desenvolvimento do setor.

Neste relatório, detalharemos cada etapa de nossa análise, desde a coleta e tratamento dos dados até a apresentação de resultados claros e conclusões significativas. Ao final, esperamos fornecer uma compreensão mais profunda dos comportamentos dos preços dos combustíveis no Brasil, contribuindo para a missão contínua da ANP de fornecer informações precisas e relevantes para o setor de petróleo e gás.

---

## <center> <font color = 'seagreen'> **Objetivo da Análise** </font> </center>

O objetivo principal desta análise exploratória é investigar e compreender os comportamentos dos preços de venda dos combustíveis ao longo dos dois últimos meses do ano atual. Através dessa análise, buscamos responder a uma série de perguntas específicas que abordam tanto as tendências gerais quanto as variações regionais e setoriais nos preços dos combustíveis. Nossa meta é oferecer uma visão abrangente das flutuações dos preços, identificando possíveis padrões, correlações e insights relevantes. Isso permitirá uma melhor compreensão das dinâmicas do mercado de combustíveis e ajudará a informar decisões futuras relacionadas à indústria de petróleo e gás.

---

## <center> <font color = 'seagreen'> **Fontes de Dados** </font> </center>

Para realizar esta análise exploratória, utilizamos dados provenientes do portal Gov.br e disponibilizados pela Agência Nacional de Petróleo e Gás Natural e Biocombustíveis (ANP). A ANP é reconhecida por sua expertise em coletar e fornecer informações precisas sobre a indústria de petróleo e gás no Brasil.

Obtivemos os arquivos dos dois últimos meses do ano atual, os quais contêm a série histórica dos preços de venda dos combustíveis em todo o território brasileiro. Esses dados fornecem uma representação detalhada dos preços praticados em diferentes regiões, estados, municípios e bandeiras de venda.

[Dados Maio](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2023/precos-gasolina-etanol-05.csv)

[Dados Junho](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2023/precos-gasolina-etanol-06.csv)

A utilização desses dados confiáveis e abrangentes nos permite conduzir uma análise robusta e informada sobre as tendências e comportamentos dos preços dos combustíveis, fornecendo insights valiosos para a ANP e para o setor como um todo.

---

## <center> <font color = 'seagreen'> **Perguntas a serem Respondidas** </font> </center>

1. Como se comportaram os preços dos combustíveis durante os dois meses citados? Os valores tiveram uma tendência de queda ou diminuição?
1. Qual o preço médio dos combustíveis nesses dois meses?
1. Qual a frequencia de coleta de dados por dia da semana 
1. Quais os 5 estados com o preço médio dos combustíveis mais caros?
1. Qual o preço médio dos combustíveis por estado?
1. Qual o município que possui o menor preço para os combustíveis?
1. Qual o município que possui o maior preço para os combustíveis?
1. Qual a região que possui o maior valor médio da gasolina (comum e aditivada)?
1. Qual a região que possui o menor valor médio do etanol?
1. Há alguma correlação entre o valor dos combustíveis e a região onde ele é vendido?
1. Quais as bandeira mais caras?
1. Há alguma correlação entre o valor dos combustíveis e a bandeira que vende ele?
1. O valor do petróleo influencia no valor da gasolina?

---

## <center> <font color = 'seagreen'> **Métodos Utilizados** </font> </center>


Nossa análise exploratória foi conduzida seguindo uma série de etapas bem definidas, visando garantir a qualidade dos resultados e insights obtidos. Abaixo, descrevemos sucintamente as etapas que seguimos:

- **Coleta e Importação de Dados:** 

    Baixamos os dados dos dois últimos meses do ano atual disponibilizados pela ANP e importamos esses conjuntos de dados no ambiente de análise.

- **Limpeza e Pré-processamento:**

    Realizamos uma limpeza detalhada dos dados, tratando valores ausentes, eliminando duplicatas e garantindo que os tipos de dados estavam corretos para cada coluna. Também verificamos se não havia outliers que poderiam distorcer nossas análises.

- **Cálculos e Derivação de Novas Variáveis:**

    Calculamos o preço médio dos combustíveis para cada mês e também exploramos a possibilidade de criar novas variáveis que pudessem enriquecer nossas análises.

- **Visualizações Gráficas:**

    Utilizamos as bibliotecas Matplotlib, Geopandas e Seaborn para criar uma variedade de gráficos, como gráficos de linha para acompanhar as tendências de preços ao longo do tempo, gráficos de barras para comparar preços entre estados e regiões, e gráficos de dispersão para explorar correlações entre variáveis.

- **Análise de Correlações:**

    Utilizamos ferramentas como o coeficiente de correlação para determinar se havia relação entre o preço dos combustíveis e outras variáveis, como a região ou o valor do petróleo.

- **Perguntas Adicionais:**

    Para responder cada uma das perguntas listadas, fornecendo visualizações e análises relevantes para cada caso, aplicamos métodos específicos, como agrupamento por dia da semana para a frequência de coleta de dados e análises de regressão para examinar a relação entre o preço do petróleo e o valor da gasolina.

- **Apresentação dos Resultados:**

    Utilizamos formatação em Markdown para criar descrições detalhadas de cada etapa, incluindo explicações dos gráficos e tabelas, e destacamos os insights obtidos.

Ao seguir essas etapas e utilizar as bibliotecas Python como Pandas, Numpy, Seaborn, Geopandas e Matplotlib, fomos capazes de conduzir uma análise abrangente e precisa das séries históricas de preço de gasolina e etanol, respondendo às perguntas propostas e explorando as perguntas adicionais de forma eficaz.

---

## <center> <font color = 'seagreen'> **Tecnologias e Ferramentas Utilizadas** </font> </center>

Neste projeto, foram utilizadas as seguintes tecnologias e programas:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![numpy](https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white) ![matplotlib](https://img.shields.io/badge/matplotlib-3776AB?style=for-the-badge&logo=matplotlib&logoColor=white) ![seaborn](https://img.shields.io/badge/seaborn-4DB6AC?style=for-the-badge&logo=seaborn&logoColor=white) ![geopandas](https://img.shields.io/badge/geopandas-4EAE53?style=for-the-badge&logo=geopandas&logoColor=white)


Essas tecnologias e ferramentas foram fundamentais para a análise dos dados e a criação dos gráficos que forneceram insights valiosos sobre a análise exploratória relacionada à série histórica de preço de venda dos combustíveis.

---

## <center> <font color = 'seagreen'> **Instruções de Uso** </font> </center>

Na pasta (), você encontrará os arquivos necessários para explorar a análise de dados das séries históricas de combustíveis no Brasil.

### Arquivo .py (Códigos e Construção):

- Este arquivo contém todos os códigos que foram desenvolvidos para realizar a análise e construção do projeto.
- Os códigos estão organizados e comentados para facilitar a compreensão.

### Arquivo .ipynb (Demonstrações e Respostas/Insights):

- Abra o arquivo .ipynb no ambiente do Jupyter Notebook ou Google Colab.
- Utilize células de código para executar as demonstrações de tabelas, gráficos ou cálculos que você deseja apresentar.
- As células Markdown fornecem as respostas e insights correspondentes a cada pergunta e tópico analisado.

---

## <center> <font color = 'seagreen'> **Considerações Finais** </font> </center>

Ao concluirmos esta análise exploratória das séries históricas dos preços dos combustíveis no Brasil, fica evidente o impacto significativo que o mercado de combustíveis exerce sobre a economia e a vida cotidiana dos cidadãos. Por meio desta investigação detalhada, pudemos discernir tendências, correlações e variações que nos proporcionam insights valiosos sobre os comportamentos dos preços ao longo dos dois últimos meses.

Compreender como os preços de gasolina e etanol se comportam e quais fatores influenciam essas variações é essencial para consumidores, empresas e decisores políticos. A indústria de petróleo e gás é altamente dinâmica, e esta análise contribui para o aprimoramento das tomadas de decisões informadas no setor. Além disso, as respostas às perguntas propostas, bem como às perguntas adicionais, fornecerão insights estratégicos para a Agência Nacional de Petróleo e Gás Natural e Biocombustíveis (ANP), que poderão embasar políticas públicas e orientações para a indústria.

Ao abordar tópicos como a frequência de coleta de dados, a influência do valor do petróleo e as variações entre bandeiras, esta análise estabelece uma base sólida para a compreensão das dinâmicas complexas do mercado de combustíveis no Brasil. Esperamos que este relatório seja uma contribuição valiosa para a busca contínua de transparência, eficiência e entendimento no setor de petróleo e gás, proporcionando benefícios para toda a sociedade.

---

## <center> <font color = 'seagreen'> **Contribuições** </font> </center> 

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões para melhorias, sinta-se à vontade para abrir uma issue neste repositório.

---