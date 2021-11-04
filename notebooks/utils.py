import netpixi
from netpixi.data.gt import *
import cpnet
from graph_tool import spectral
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
sns.set()
from matplotlib import rcParams
import statsmodels.formula.api as smf
import csv
import pandas as pd
from graph_tool import util
from graph_tool import Graph

def media(sport, df_desempenho_media):
    df_temp = df_desempenho_media.loc[df_desempenho_media.index==sport]
    valor = df_temp.iloc[0]['desempenho']
    return valor


def desempenho(medalha):
    if(medalha == "Gold"):
        return 3
    elif(medalha == "Silver"):
        return 2
    elif(medalha == "Bronze"):
        return 1
    else:
        return 0

def cria_vertices(g, lista, indice_corte):
    for i in range(len(lista)):
        propriedade = "time"
        cor = 0xff0000
        if i >= indice_corte:
            cor = 0x00ff00
            propriedade = "evento"
        
        #adiciona vértice
        g.add_vertex()
        v = g.vertex(i)
        
        #adiciona propriedade
        g.vp['tipo'][v] = propriedade
        
        #adiciona nome
        g.vp['nome'][v] = lista[i]
        
        #adiciona cor
        g.vp['color'][v] = cor

def arestas(time, evento, desempenho, desempenho_media, lista_arestas):
    if (desempenho > desempenho_media):
        lista_arestas.append((time, evento))

def create_edgs_links(v_p_list, g):
    for dupla in v_p_list:
        pais = dupla[0]
        esporte = dupla[1]
        str_index_pais = util.find_vertex(g,g.vp["nome"], pais) 
        index_pais = int(str(str_index_pais).split(" ")[4].replace("'","")) #pega o índice do pais
        str_index_esporte = util.find_vertex(g,g.vp['nome'],esporte) 
        index_esporte = int(str(str_index_esporte).split(" ")[4].replace("'","")) #pega o índice do esporte
        g.add_edge(index_pais, index_esporte) #adiciona a aresta no grafo

def elimina_ultimo_caracter(string):
    return string[0: -1]

def acerta_nome_paises(pais, dicionario):
    if pais in dicionario:
        return dicionario[pais]
    return pais