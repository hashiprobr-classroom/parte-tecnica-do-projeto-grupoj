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
import itertools

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
    if (desempenho > desempenho_media*0.3):
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


def similaridade(lista1, lista2):
    numero = 0
    for evento in lista1:
        if evento in lista2:
            numero +=1
    return numero

def cria_nome_times(g, c):
    indice = 0
    for v in g.vertices():
        isEvent = g.vp['tipo'][v] #booelan 
        if (isEvent == "time"):
            c.add_vertex() #adiciona vértice
            vertice = c.vertex(indice) #último vértice adicionado
            c.vp['nome'][vertice] = g.vp['nome'][v] #atribui nome
            indice += 1

def lista_esporte_por_time(g):
    resposta_dict = dict()
    resposta_list = []
    for vertice in g.vertices():
        isEvent = g.vp['tipo'][vertice] #booelan 
        if (isEvent == "time"):
            nome = g.vp['nome'][vertice] #pega o nome
            resposta_list.append(nome)
            resposta_dict[nome] = []
            for vizinho in vertice.all_neighbors():
                resposta_dict[nome].append(g.vp['nome'][vizinho]) #adiciona os vizinhos
    return resposta_dict, resposta_list


def cria_arestas(grafo, dicionario, lista_nomes):
    
    distribuicao = []

    #compara cada um dos nomes com o resto da lista
    for a, b in itertools.combinations(lista_nomes, 2):
        lista_eventos_a = dicionario[a] #lista de eventos de a
        lista_eventos_b = dicionario[b] #lista de eventos de b
        n_eventos = similaridade(lista_eventos_a, lista_eventos_b) #número de eventos que ambos participaram
        if (n_eventos > 0):
            distribuicao.append(n_eventos)
            str_index_a = util.find_vertex(grafo, grafo.vp['nome'], a) 
            index_a = int(str(str_index_a).split(" ")[4].replace("'","")) #pega o índice do a

            str_index_b = util.find_vertex(grafo, grafo.vp['nome'], b) 
            index_b = int(str(str_index_b).split(" ")[4].replace("'","")) #pega o índice do b

            grafo.add_edge(index_a, index_b) #adiciona a aresta no grafo
            e = grafo.edge(index_a, index_b) #pega a aresta criada
            grafo.ep['peso'][e] = n_eventos #adiciona ocorrência
    return distribuicao