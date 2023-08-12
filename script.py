# importando as bibliotecas 

import matplotlib.pyplot as plt
import seaborn as sns
import requests as rq
import zipfile as zp
import io
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap as lsc
import matplotlib.ticker as mticker
import pandas as pd

# importando arquivos 
# URL do arquivo ZIP para mapa coroplético
url = "http://www.usp.br/nereus/wp-content/uploads/BR_UF_2021.zip"

# Fazer o download do arquivo ZIP e extrair seu conteúdo
response = rq.get(url)
zip_file = zp.ZipFile(io.BytesIO(response.content))
zip_file.extractall("/content/brasil_estados_folder")

# Importar o shapefile
brasil_estados = gpd.read_file("/content/brasil_estados_folder/BR_UF_2021.shp")

# importando o DataSet anp meses 5 e 6

gas_eta_5=pd.read_csv('https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2023/precos-gasolina-etanol-05.csv' ,sep=';')
gas_eta_6=pd.read_csv('https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/2023/precos-gasolina-etanol-06.csv',sep=';')
gas_eta=pd.concat([gas_eta_5,gas_eta_6])

# retirando colunas que não serão utilizadas do DataSet

gas_eta=pd.DataFrame(gas_eta,columns=['Regiao - Sigla','Estado - Sigla','Municipio','Produto','Data da Coleta','Valor de Venda','Bandeira'])

# transformando os dados da coluna valor da venda para float
gas_eta['Valor de Venda']=gas_eta['Valor de Venda'].apply(lambda x: float(x.replace(',','.')))

# transformando os dados de data para datetime
gas_eta['Data da Coleta']=pd.to_datetime(gas_eta['Data da Coleta'],dayfirst=True)


# criando o dataframe com o dado mdc=media diaria dos preços combustiveis 

# nesse dataframe tranformamos os valores da coluna produtos em colunas é as data em indices
# além disso acrescentamos as datas em que não foram feitas coletas utilizando o metodo nearest
# para que fosse atribuido a essas linhas o valor de indice mais proximo 
mdc=gas_eta.pivot_table(columns='Produto',index='Data da Coleta',values='Valor de Venda', aggfunc='mean').reindex(pd.date_range(start='2023-05-01',end='2023-06-30'),method='nearest')

# media no valor do combustivel nos ultimos dois meses 

media_combustivel=mdc.mean()

# media do valor por estado 

media_por_estado=gas_eta.pivot_table(columns='Produto',index='Estado - Sigla',values='Valor de Venda', aggfunc='mean')

# dicionario com os estados com maior valor de combustiveis por estado

dic_combustives_estado={'ETANOL':media_por_estado['ETANOL'].sort_values(ascending=False)[:5],
'GASOLINA':media_por_estado['GASOLINA'].sort_values(ascending=False)[:5],
'GASOLINA_ADT':media_por_estado['GASOLINA ADITIVADA'].sort_values(ascending=False)[:5]
}
#media municipal
media_municipal=gas_eta.pivot_table(columns='Produto',index='Municipio',values='Valor de Venda', aggfunc='mean')

# dicionarios com os municipios com maior valor de combustivel 
 
municipios_mais_caros={'GASOLINA':media_municipal['GASOLINA'].sort_values(ascending=False)[:3],
'GASOLINA ADITIVADA':media_municipal['GASOLINA ADITIVADA'].sort_values(ascending=False)[:3],
'ETANOL':media_municipal['ETANOL'].sort_values(ascending=False)[:3]}

# dicionario com os municipios  mais baratos 

municipios_mais_baratos={'GASOLINA':media_municipal['GASOLINA'].sort_values()[:3],
'GASOLINA ADITIVADA':media_municipal['GASOLINA ADITIVADA'].sort_values()[:3],
'ETANOL':media_municipal['ETANOL'].sort_values()[:3]}

# media no valor dos combustiveis

preco_por_regiao=gas_eta.pivot_table(columns='Regiao - Sigla',index='Produto',values='Valor de Venda', aggfunc='mean')

# media por data e produto, dividido por região 

media_regiao_data=gas_eta.pivot_table(columns='Regiao - Sigla',values='Valor de Venda',index=['Produto','Data da Coleta'],aggfunc='mean').dropna()


