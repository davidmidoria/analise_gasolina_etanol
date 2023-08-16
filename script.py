# importando as bibliotecas 

import matplotlib.pyplot as plt
import seaborn as sns
import requests as rq
import zipfile as zp
import io
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap 
import pandas as pd
import numpy as np
import unicodedata 

# importando arquivos 

# URL do arquivo ZIP para mapa coroplético de municipios
link = "http://www.usp.br/nereus/wp-content/uploads/BR_Municipios_2021.zip"

# Fazer o download do arquivo ZIP e extrair seu conteúdo
respons = rq.get(link)
zip_fil = zp.ZipFile(io.BytesIO(respons.content))
zip_fil.extractall("/content/brasil_municipios_folder")

# Importar o shapefile
brasil_municipios = gpd.read_file("/content/brasil_municipios_folder/BR_Municipios_2021.shp")

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

# dias da semana
dia_semana={'2023-05-01': 'Segunda-feira', '2023-05-02': 'Terça-feira', '2023-05-03': 'Quarta-feira', '2023-05-04': 'Quinta-feira', '2023-05-05': 'Sexta-feira', '2023-05-06': 'Sábado', '2023-05-07': 'Domingo', '2023-05-08': 'Segunda-feira', '2023-05-09': 'Terça-feira', '2023-05-10': 'Quarta-feira', '2023-05-11': 'Quinta-feira', '2023-05-12': 'Sexta-feira', '2023-05-13': 'Sábado', '2023-05-14': 'Domingo', '2023-05-15': 'Segunda-feira', '2023-05-16': 'Terça-feira', '2023-05-17': 'Quarta-feira', '2023-05-18': 'Quinta-feira', '2023-05-19': 'Sexta-feira', '2023-05-20': 'Sábado', '2023-05-21': 'Domingo', '2023-05-22': 'Segunda-feira', '2023-05-23': 'Terça-feira', '2023-05-24': 'Quarta-feira', '2023-05-25': 'Quinta-feira', '2023-05-26': 'Sexta-feira', '2023-05-27': 'Sábado', '2023-05-28': 'Domingo', '2023-05-29': 'Segunda-feira', '2023-05-30': 'Terça-feira', '2023-05-31': 'Quarta-feira', '2023-06-01': 'Quinta-feira', '2023-06-02': 'Sexta-feira', '2023-06-03': 'Sábado', '2023-06-04': 'Domingo', '2023-06-05': 'Segunda-feira', '2023-06-06': 'Terça-feira', '2023-06-07': 'Quarta-feira', '2023-06-08': 'Quinta-feira', '2023-06-09': 'Sexta-feira', '2023-06-10': 'Sábado', '2023-06-11': 'Domingo', '2023-06-12': 'Segunda-feira', '2023-06-13': 'Terça-feira', '2023-06-14': 'Quarta-feira', '2023-06-15': 'Quinta-feira', '2023-06-16': 'Sexta-feira', '2023-06-17': 'Sábado', '2023-06-18': 'Domingo', '2023-06-19': 'Segunda-feira', '2023-06-20': 'Terça-feira', '2023-06-21': 'Quarta-feira', '2023-06-22': 'Quinta-feira', '2023-06-23': 'Sexta-feira', '2023-06-24': 'Sábado', '2023-06-25': 'Domingo', '2023-06-26': 'Segunda-feira', '2023-06-27': 'Terça-feira', '2023-06-28': 'Quarta-feira', '2023-06-29': 'Quinta-feira', '2023-06-30': 'Sexta-feira'}


# estados da união 
estados = {"AC": "Acre","AL": "Alagoas","AP": "Amapá","AM": "Amazonas","BA": "Bahia","CE": "Ceará","DF": "Distrito Federal","ES": "Espírito Santo","GO": "Goiás","MA": "Maranhão","MT": "Mato Grosso","MS": "Mato Grosso do Sul","MG": "Minas Gerais","PA": "Pará","PB": "Paraíba","PR": "Paraná","PE": "Pernambuco","PI": "Piauí","RJ": "Rio de Janeiro","RN": "Rio Grande do Norte","RS": "Rio Grande do Sul","RO": "Rondônia","RR": "Roraima","SC": "Santa Catarina","SP": "São Paulo","SE": "Sergipe","TO": "Tocantins"}

# regiões
siglas_para_regioes = {
    'SE':'Sudeste',
    'S' :'Sul',
    'N' : 'Norte',
    'NE': 'Nordeste',
    'CO': 'Centro\noeste'
}

# retirando colunas que não serão utilizadas do DataSet

gas_eta=pd.DataFrame(gas_eta,columns=['Regiao - Sigla','Estado - Sigla','Municipio','Produto','Data da Coleta','Valor de Venda','Bandeira'])

# criando a coluna com os dias da semana

gas_eta['Dia da Semana']=gas_eta['Data da Coleta']
gas_eta['Dia da Semana']=gas_eta['Dia da Semana'].apply(lambda x: dia_semana['-'.join(x.split('/')[::-1])])

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

# rotulador de gráficos de barras horizontais  
def rotulacao(ax, bars,s1='R$',s2='',altura=0.4,font=12):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{s1}{height:.2f}{s2}'.replace('.',','),xy=(bar.get_x() + bar.get_width() / 2, height-altura),xytext=(0, 3),textcoords="offset points",ha='center', va='bottom',color='white',fontsize=font,fontstyle= 'italic',fontweight= 'bold')


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

# tira o percentual pega os 4 maiores e soma o resto
def media_5(quantidade_item,nome_extra):
    percentual=(quantidade_item/quantidade_item.sum())*100
    quatro_maiores=percentual[:4]
    quatro_maiores[nome_extra]=percentual[4:].sum()
    return quatro_maiores

# pega os itens definidos previamente e tira uma media entre os demais 

def escolher_item(itens,itens_filtro,demais_itens):
    itens_f=itens[itens_filtro]
    itens_f[demais_itens]=itens.drop(itens_filtro).mean()
    return itens_f.sort_values()

# grafico da correlação entre as bandeiras

def grafico_correlacao(cor,titulo,item,cor2='white'):

    maiores_media=media_5(gas_eta['Bandeira'][gas_eta['Produto']==item].value_counts(),'Outras Bandeiras')
    media_combustiveis=gas_eta.pivot_table(columns='Bandeira',index=['Produto','Data da Coleta'],values='Valor de Venda', aggfunc='mean')
    media_diaria_b=media_combustiveis[maiores_media[:4].index].copy()
    media_diaria_b[maiores_media[4:].index[0]]=media_combustiveis.drop(columns=maiores_media[:4].index).T.mean()
    media_valor=escolher_item(media_combustiveis.loc[item].mean(),maiores_media[:4].index,maiores_media[4:].index[0])

    fig=plt.figure(figsize=(20,7))
    g1=plt.subplot(131)
    g2=plt.subplot(132)
    g3=plt.subplot(133)

    rotulacao(g1,g1.bar(maiores_media.index,maiores_media.values,color=cor),s1='',s2='%',altura=2.8)
    g1.set_yticks([])
    g1.set_xticks(maiores_media.index,(i.replace(' ','\n')for i in maiores_media.index),color='grey',fontweight= 'bold',fontsize=12, fontstyle= 'italic')
    g1.spines[['top', 'right','left']].set_visible(False)
    g1.set_title(f'participação de mercado\n', fontsize=20, fontweight='bold', color=cor)


    adicionar_rotulos(g2,g2.barh(media_valor.index,media_valor.values,color=cor))
    g2.set_yticks(media_valor.index,media_valor.index,color='grey',fontweight= 'bold',fontsize=15, fontstyle= 'italic')
    g2.set_xticks([])
    g2.spines[['top', 'right','left']].set_visible(False)
    g2.set_title(f'preço medio das bandeiras\n', fontsize=20, fontweight='bold', color=cor)

    sns.heatmap(media_diaria_b.loc[item].corr(), annot=True, cmap=LinearSegmentedColormap.from_list('CustomColors',[cor2,cor]), center=0, linewidths=.5, cbar=False,ax=g3,annot_kws={"size": 15,'fontweight':'bold'})
    g3.set_xticklabels((i.replace(' ','\n')for i in media_diaria_b.loc[item].corr().index ), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')  # Rótulos do eixo X rotacionados em 45 graus
    g3.set_yticklabels((i.replace(' ','\n')for i in media_diaria_b.loc[item].corr().index ), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')
    g3.set_title(f'correlação entre as bandeiras\n', fontsize=20, fontweight='bold', color=cor)
    g3.set_ylabel('') 
    g3.set_xlabel('') 

    fig.suptitle(titulo, fontsize=30, fontweight='bold', color=cor,fontstyle= 'italic', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0.10, 1, 0.9])
    plt.subplots_adjust(wspace=0.4) 

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

# gráfico contendo os valores medios de combustiveis de cada região 

def grafico_regiao():
    fig=plt.figure(figsize=(20,7))
    g1=plt.subplot(131)
    g2=plt.subplot(132)
    g3=plt.subplot(133)
    core=['royalblue','grey','grey','grey','#a51b0b']


    rotulacao(g1,g1.bar(media_regiao_data.loc['ETANOL'].mean().sort_values().index,media_regiao_data.loc['ETANOL'].mean().sort_values().values,color=core))
    g1.set_yticks([])
    g1.set_xticks(media_regiao_data.loc['ETANOL'].mean().sort_values().index,media_regiao_data.loc['ETANOL'].mean().sort_values().index,color='black',fontweight= 'bold',fontsize=14, fontstyle= 'italic')
    g1.spines[['top', 'right','left']].set_visible(False)
    g1.set_title(f'etanol\n', fontsize=20, fontweight='bold', color='royalblue')


    rotulacao(g2,g2.bar(media_regiao_data.loc['GASOLINA'].mean().sort_values().index,media_regiao_data.loc['GASOLINA'].mean().sort_values().values,color=core))
    g2.set_yticks([])
    g2.set_xticks(media_regiao_data.loc['GASOLINA'].mean().sort_values().index,media_regiao_data.loc['GASOLINA'].mean().sort_values().index,color='black',fontweight= 'bold',fontsize=14, fontstyle= 'italic')
    g2.spines[['top', 'right','left']].set_visible(False)
    g2.set_title(f'gasolina\n', fontsize=20, fontweight='bold', color='#a51b0b')

    rotulacao(g3,g3.bar(media_regiao_data.loc['GASOLINA ADITIVADA'].mean().sort_values().index,media_regiao_data.loc['GASOLINA ADITIVADA'].mean().sort_values().values,color=core))
    g3.set_yticks([])
    g3.set_xticks(media_regiao_data.loc['GASOLINA ADITIVADA'].mean().sort_values().index,media_regiao_data.loc['GASOLINA ADITIVADA'].mean().sort_values().index,color='black',fontweight= 'bold',fontsize=14, fontstyle= 'italic')
    g3.spines[['top', 'right','left']].set_visible(False)
    g3.set_title(f'gasolina aditivada\n', fontsize=20, fontweight='bold', color='#d11507')

    fig.suptitle('Media regional do valor do combustivel', fontsize=30, fontweight='bold', color='darkred',fontstyle= 'italic', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0.10, 1, 0.9])
    plt.subplots_adjust(wspace=0.4) 

# gráfico da correlção entre combustiveis 
def correlacao_combustivel():    
    fig=plt.figure(figsize=(18,6))
    g1=plt.subplot(131)
    g2=plt.subplot(132)
    g3=plt.subplot(133)


    etanol= sns.heatmap(media_regiao_data.loc['ETANOL'].corr(), annot=True, cmap=LinearSegmentedColormap.from_list('CustomColors',['white','Blue']), center=0, linewidths=.5, cbar=False,ax=g3,annot_kws={"size": 15,'fontweight':'bold'})
    etanol.set_title('Etanol \n', color='Blue', fontweight='bold', fontsize=15, fontstyle='italic', loc='left')

    gasolina = sns.heatmap(media_regiao_data.loc['GASOLINA'].corr(), annot=True, cmap=LinearSegmentedColormap.from_list('CustomColors',['white','#a51b0b']), center=0, linewidths=.5, cbar=False,ax=g2,annot_kws={"size": 15,'fontweight':'bold'})
    gasolina.set_title('Gasolina \n', color='#a51b0b', fontweight='bold', fontsize=15, fontstyle='italic', loc='left')

    gasolina_aditivada = sns.heatmap(media_regiao_data.loc['GASOLINA ADITIVADA'].corr(), annot=True, cmap=LinearSegmentedColormap.from_list('CustomColors',['white','#d11507']), center=0, linewidths=.5, cbar=False,ax=g1,annot_kws={"size": 15,'fontweight':'bold'})
    gasolina_aditivada.set_title('Gasolina Aditivada \n', color='#d11507', fontweight='bold', fontsize=15, fontstyle='italic', loc='left')
    # Reduzir nomes exibidos no eixo x e y
    g1.set_xticklabels(g1.get_xticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')  # Rótulos do eixo X rotacionados em 45 graus
    g1.set_yticklabels(g1.get_yticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')
    g1.set_ylabel('') 
    g1.set_xlabel('') 

    g2.set_xticklabels(g2.get_xticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')  # Rótulos do eixo X rotacionados em 45 graus
    g2.set_yticklabels(g2.get_yticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')
    g2.set_ylabel('') 
    g2.set_xlabel('') 

    g3.set_xticklabels(g3.get_xticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')  # Rótulos do eixo X rotacionados em 45 graus
    g3.set_yticklabels(g3.get_yticklabels(), rotation=0,color='grey',fontsize=12, fontweight='bold',fontstyle= 'italic')
    g3.set_ylabel('') 
    g3.set_xlabel('') 


    # Configurar rótulos do cbar
    # cor_grafico = LinearSegmentedColormap.from_list('CustomColors', [corX,corY], N=27)# cor do gráfico de barras
    fig.suptitle('Correlação entre os valores dos combustiveis Brasil', fontsize=30, fontweight='bold', color='darkred',fontstyle= 'italic', x=0.05, ha='left')
    plt.tight_layout(rect=[0, 0.10, 1, 0.9])
    plt.subplots_adjust(wspace=0.4) 
    plt.show()

# Função para remover acentuação
def remove_accent(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

# Remover acentos e padronizar formatação da coluna "Municipio" em df_combustivel
brasil_municipios['NM_MUN'] = brasil_municipios['NM_MUN'].apply(lambda x: remove_accent(x.upper()))

def panzer():
    municipios=gas_eta[['Municipio','Produto']].copy()
    municipios['Municipio']=municipios['Municipio'].apply(lambda x:x.replace('\n',' '))

    # Realizar o merge com base na coluna "Municipio"
    municipios_merged = brasil_municipios.merge(municipios, left_on='NM_MUN', right_on='Municipio', how='left')
    # Definir cores para os tipos de combustível
    tipo_to_color = {
        'GASOLINA ADITIVADA': 'red',
        'GASOLINA': 'darkred',
        'ETANOL': 'darkblue'}

    # Plotar o mapa com pontos coloridos para indicar o tipo de combustível
    fig, ax = plt.subplots(figsize=(12, 8))
    brasil_municipios.plot(linewidth=0.01, ax=ax, color='silver', edgecolor='lightgray')

    # Plotar os pontos coloridos
    for index, row in municipios_merged.iterrows():
        if row['Produto'] in tipo_to_color:  # Verificar se o tipo de combustível está na lista
            centroid = row['geometry'].centroid
            ax.plot(centroid.x, centroid.y, marker='o', color=tipo_to_color[row['Produto']], markersize=2)

    # Configurar legenda
    legend_labels = {v: k for k, v in tipo_to_color.items()}
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=10, label=legend_labels[c]) for c in tipo_to_color.values()]
    legend = ax.legend(handles=handles, title='Tipo de Combustível', prop={'size': 8})

    # Remover informações, labels, índices, eixos e grades
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Distribuição da coleta de dados dos Combustíveis', color='maroon', fontweight='bold', fontsize=15, fontstyle='italic', loc='right')
    plt.show()


def lancamento_dados():
    percentuall_semana=gas_eta['Dia da Semana'].value_counts()/gas_eta['Dia da Semana'].value_counts().sum()*100
    plt.figure(figsize=(10,7))
    rotulacao(plt,plt.bar(percentuall_semana.index,percentuall_semana.values),altura=1.5,s1='',s2='%',font=10)
    quadro(['bottom'])
    plt.xticks(percentuall_semana.index,color='black',fontweight= 'bold',fontsize=10, fontstyle= 'italic')
    plt.tick_params(axis='both',color='grey')
    plt.yticks([])
    plt.title('lançamento diario dos dados\n\n\n',color='royalblue',fontweight= 'bold',fontsize=15, fontstyle= 'italic',loc='left')
    plt.show()