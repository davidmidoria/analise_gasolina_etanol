# importando as bibliotecas 

import matplotlib.pyplot as plt
import seaborn as sns
import requests as rq
import zipfile as zp
import io
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap 
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

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

# estados da união 
estados = {"AC": "Acre","AL": "Alagoas","AP": "Amapá","AM": "Amazonas","BA": "Bahia","CE": "Ceará","DF": "Distrito Federal","ES": "Espírito Santo","GO": "Goiás","MA": "Maranhão","MT": "Mato Grosso","MS": "Mato Grosso do Sul","MG": "Minas Gerais","PA": "Pará","PB": "Paraíba","PR": "Paraná","PE": "Pernambuco","PI": "Piauí","RJ": "Rio de Janeiro","RN": "Rio Grande do Norte","RS": "Rio Grande do Sul","RO": "Rondônia","RR": "Roraima","SC": "Santa Catarina","SP": "São Paulo","SE": "Sergipe","TO": "Tocantins"}

# regiões
siglas_para_regioes = {
    'SE':'Sudeste',
    'S' :'Sul',
    'N' : 'Norte',
    'NE': 'Nordeste',
    'CO': 'Centro-oeste'
}

# retirando colunas que não serão utilizadas do DataSet

gas_eta=pd.DataFrame(gas_eta,columns=['Regiao - Sigla','Estado - Sigla','Municipio','Produto','Data da Coleta','Valor de Venda','Bandeira'])

# transformando os dados da coluna valor da venda para float
gas_eta['Valor de Venda']=gas_eta['Valor de Venda'].apply(lambda x: float(x.replace(',','.')))

# transformando os dados de data para datetime
gas_eta['Data da Coleta']=pd.to_datetime(gas_eta['Data da Coleta'],dayfirst=True)

# trocando o nome de siglas para o nome dos estados 
gas_eta['Estado - Sigla']=gas_eta['Estado - Sigla'].apply(lambda x:estados[x])

# trocando o nome das siglas das regiões para o nome das regiões
gas_eta['Regiao - Sigla']=gas_eta['Regiao - Sigla'].apply(lambda x:siglas_para_regioes[x])

# manipulando o nome dos municipios
gas_eta['Municipio']=gas_eta['Municipio'].apply(lambda x:x.replace(' ','\n'))

# trocando o nome das colunas em quê o valor foi alterado
gas_eta.rename(columns={'Estado - Sigla':'Estado','Regiao - Sigla':'Regiao'},inplace=True)


# criando o dataframe com o dado mdc=media diaria dos preços combustiveis 

# nesse dataframe tranformamos os valores da coluna produtos em colunas é as data em indices
# além disso acrescentamos as datas em que não foram feitas coletas utilizando o metodo nearest
# para que fosse atribuido a essas linhas o valor de indice mais proximo 
mdc=gas_eta.pivot_table(columns='Produto',index='Data da Coleta',values='Valor de Venda', aggfunc='mean').reindex(pd.date_range(start='2023-05-01',end='2023-06-30'),method='nearest')

# media no valor do combustivel nos ultimos dois meses 

media_combustivel=mdc.mean()

# media do valor por estado 

media_por_estado=gas_eta.pivot_table(columns='Produto',index='Estado',values='Valor de Venda', aggfunc='mean')

# dicionario com os estados com maior valor de combustiveis por estado

dic_combustives_estado={'GASOLINA_ADITIVADA':media_por_estado['GASOLINA ADITIVADA'].sort_values(ascending=False)[:5],
'GASOLINA':media_por_estado['GASOLINA'].sort_values(ascending=False)[:5],
'ETANOL':media_por_estado['ETANOL'].sort_values(ascending=False)[:5]
}
#media municipal
media_municipal=gas_eta.pivot_table(columns='Produto',index='Municipio',values='Valor de Venda', aggfunc='mean')

# dicionarios com os municipios com maior valor de combustivel 
 
municipios_mais_caros={'GASOLINA':media_municipal['GASOLINA'].sort_values(ascending=False)[:5],
'GASOLINA ADITIVADA':media_municipal['GASOLINA ADITIVADA'].sort_values(ascending=False)[:5],
'ETANOL':media_municipal['ETANOL'].sort_values(ascending=False)[:5]}

# dicionario com os municipios  mais baratos 

municipios_mais_baratos={'GASOLINA':media_municipal['GASOLINA'].sort_values()[:5],
'GASOLINA ADITIVADA':media_municipal['GASOLINA ADITIVADA'].sort_values()[:5],
'ETANOL':media_municipal['ETANOL'].sort_values()[:5]}

# media no valor dos combustiveis

preco_por_regiao=gas_eta.pivot_table(columns='Regiao',index='Produto',values='Valor de Venda', aggfunc='mean')

# media por data e produto, dividido por região 

media_regiao_data=gas_eta.pivot_table(columns='Regiao',values='Valor de Venda',index=['Produto','Data da Coleta'],aggfunc='mean').dropna()


# cores padrão dos gráficos
 
cores={'GASOLINA ADITIVADA':'#d11507','GASOLINA':'#a51b0b','ETANOL':'RoyalBlue'}

# uma função para encontrar o percentual de crescimento ou de queda, devolve uma string com o percentual é o nome
def percentual(obj):
    calculo=(obj[-1]/obj[0]-1)*100
    sinal=( '+'if calculo>0 else '')
    return f'{sinal}{calculo:.2f}% {obj.name}'.replace('.',',')

# cria um gráfico de linha com um  scatter na ponta é com a possibilidade de um comentario obs: foi construida para somente dados temporais.

def linha_comentada(x,y,comentario='',cor='grey'):
    plt.plot(x,y,color=cor,linewidth=2.5)
    plt.scatter(x[-1],y[-1],color=cor)
    plt.annotate(comentario, xy=(x[-1],y[-1]), xytext=((x[-1])+pd.Timedelta(days=2),y[-1]),arrowprops=dict(color=cor, arrowstyle='-'),color=cor,fontsize=12,fontstyle= 'italic',fontweight= 'bold')


# recebe um dataframe onde o index é um valor temporal esse index sera a coluna x enquanto as colunas serão as linhas.


def linhas(obj):
    [linha_comentada(obj.index,obj[coluna],comentario=percentual(obj[coluna]),cor=cores[coluna]) for coluna in obj.columns]

# torna o quadro invisivel por padrão  mas se tem a possibilidade de mostrar algumas colunas do quadro e alterar sua cor.

def quadro(s_p=[],cor='grey'):
    quadro=list(filter(lambda x: x not in s_p,['right','top','bottom','left']))
    plt.gca().spines[quadro].set_visible(False)
    if s_p!= []:
        plt.gca().spines[s_p].set_color(cor)

# titulos e rotulos padrão 

def titulos_rotulos(titulo,x_rotulo_a,x_rotulo_d,y_rotulo_a,y_rotulo_d):
    plt.xticks(x_rotulo_a,x_rotulo_d,color='darkgrey')
    plt.tick_params(axis='both',color='grey')
    plt.yticks(y_rotulo_a,y_rotulo_d,color='grey')
    plt.title(f'{titulo}\n\n\n',color='darkred',fontweight= 'bold',fontsize=15, fontstyle= 'italic',loc='left')

# cria o gráfico de barras ja com seus valores no interior da barra, obs esse coi contruido para inserir o dado no formato de uma moeda.

def adicionar_rotulos(obj,barras,font=15):
    for barra in barras:
        largura = barra.get_width()
        obj.text(largura-0.5, barra.get_y() + barra.get_height() / 2, f'R${largura:.2f}'.replace('.',','), ha='right', va='center', color='white', fontweight='bold',fontsize=font)


# cores que serão usadas para colorir as barras
cor_da_barra=lambda x: ['grey','grey','grey','grey']+[cores[x]]

# cria uma certa estilização dos dados com os formatos de textos e cores no formato definido como padrão

def criar_sub(obj,valor):
    coluna=valor.name
    adicionar_rotulos(obj,obj.barh(valor.index,valor.values,color=cor_da_barra(coluna)))
    obj.set_yticks(valor.index.to_list(),valor.index.to_list(),color='grey',fontweight= 'bold',fontsize=14, fontstyle= 'italic')
    obj.set_xticks([])
    obj.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    obj.set_title(f'{coluna}\n', fontsize=20, fontweight='bold', color=cor_da_barra(coluna)[-1])

# criação de uma  imagem com três gráficos de barras 

def barra_3(dicionario,titulo=''):
    fig=plt.figure(figsize=(20,7))
    x=131
    for  a,y in enumerate(dicionario.keys()):
        criar_sub(plt.subplot(x+a),dicionario[y][::-1])
    fig.suptitle(titulo, fontsize=30, fontweight='bold', color='darkred',fontstyle= 'italic', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0.10, 1, 0.9])
    plt.subplots_adjust(wspace=0.4) 

# criação da função com o gráfico do Brasil
def mapa_estados(obj,coluna,corX,corY,titulo,cor_titulo='maroon'):
    estados_merged = brasil_estados.merge(obj, left_on='NM_UF', right_on=coluna)

    fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [0.6, 0.2]})# criar figura
    cor_grafico = LinearSegmentedColormap.from_list('CustomColors', [corX,corY], N=27)# cor do gráfico de barras
    
    #gráfico da bandeira
    estados_merged.plot(column=obj.name, cmap=LinearSegmentedColormap.from_list('CustomColors',[corX,corY]), legend=False, ax=axes[0])# gráfico bandeira
    axes[0].set_xticks([])# configurações do mapa
    axes[0].set_yticks([])
    axes[0].spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    
    #gráfico de barras
    adicionar_rotulos(axes[1],plt.barh(obj.index,obj.to_list(), color=cor_grafico(np.linspace(0, 1, 27))),font=10)# gráfico de barras
    axes[1].set_xticks([])# configurações do gráfico de barras
    axes[1].set_yticks(obj.index.to_list(),obj.index.to_list(),color=corY,fontweight= 'bold',fontsize=11, fontstyle= 'italic')
    axes[1].set_xticks([])
    axes[1].spines[['top', 'right', 'bottom', 'left']].set_visible(False)

    #Adicionar título centralizado
    fig.suptitle(titulo, fontsize=20, fontweight='bold', color=cor_titulo,fontstyle= 'italic', ha='center')
    plt.tight_layout  # Para acomodar o título acima dos gráficos
    plt.show()


# grafico de linha dos combustiveis
def grafico_combustiveis():
    datas_n = ['2023-05-01', '2023-05-08', '2023-05-15', '2023-05-22', '2023-06-01',  '2023-06-08', '2023-06-15', '2023-06-22', '2023-07-01']
    data_e = ['1a Mai','2a Mai','3a Mai','4a Mai','1a Jun', '2a Jun', '3a Jun', '4a Jun', '1a Jul']
    valor_n=[4.0,4.5,5.0,5.5]
    valor_e=['R$ 4,00','R$ 4,50','R$ 5,00','R$ 5,50']
    titulo='Percentual de mudança nos valores do combustivel\nentre maio e junho'
    plt.figure(figsize=(8,4))
    linhas(mdc)
    quadro(['bottom','left'])
    titulos_rotulos(titulo,datas_n,data_e,valor_n,valor_e)
    plt.show()

#  grafico de barras contendo os estados com maior valor do preço da gasolina

def estados_maior_preco():
    barra_3(dic_combustives_estado,'Os estados com maior valor de combustivel')

# grafico com a media da gasolina por estado
def media_gasolina():
    mapa_estados(media_por_estado['GASOLINA'].sort_values(),'Estado','#df927e','#a51b0b','Media estadual da gasolina')

# grafico com a media da gasolina aditivada
def media_gasolina_adit():
    mapa_estados(media_por_estado['GASOLINA ADITIVADA'].sort_values(),'Estado','#f89880','#d11507','Media estadual da gasolina aditivada')

# grafico com a media do etanol 

def media_etanol():
    mapa_estados(media_por_estado['ETANOL'].sort_values(),'Estado','#aeb1f1','RoyalBlue','Media estadual do etanol',cor_titulo='RoyalBlue')

# gráfico com os 5 municipios mais baratos 
def municipios_baratos():
    barra_3(municipios_mais_baratos,'Os Municipios com menor  valor no combustivel')

# gráfico com os 5 municipios mais caros 

def municipios_caros():
    barra_3(municipios_mais_caros,'Os Municipios com maior valor no combustivel')