
import numpy as np
from classes import *
from graphe import *
import itertools as its

def dijkstra( graphe, deb, fin):
    ''' Applique l'algorithme de Dijkstra afin de déterminer le plus court chemin
    entre les sommets deb et fin et la distance entre ces sommets'''
    if deb==fin:
        return [0],[]
    chemin=Chemin()
    s=deb
    liste={}
    for x in graphe.g:
        liste[x]=(np.inf,deb)
    liste[deb]=(0,deb)
    visitee=[] #liste des sommets déjà visités
    attente=[deb] #liste des sommets à traiter

    while s!=fin: # itération jusqu'à atteindre le sommet d'arrivée et se termine car graphe supposé connexe
        s=attente.pop()
        visitee+=[s]
        voisins=list(graphe.g[s].keys())
        for x in voisins:
            dist=graphe.g[s][x]
            if x not in visitee:
                attente+=[x]
            if liste[s][0]+dist<liste[x][0]:
                liste[x]=(liste[s][0]+dist,s)
    s=fin
    dist=liste[fin][0]
    D=dist
    while s!=deb:
        y=liste[s]
        chemin=chemin+s
        dist,s=y
    chemin=chemin+deb
    chemin.reverse()
    return D,chemin

def glouton(g_eff): #algorithme glouton de type plus proche voisin
    """Implémente l'heuristique de plus proche voisin et renvoie
    un chemin passant par tous les sommets du graphe effectif"""
    points=g_eff.points
    chemin=Chemin()
    visite=[]
    attente=[]
    attente.append(points[0])
    chemin.chem.append(points[0])
    while attente:
        s=attente.pop()
        if visite:
            mini=visite[0],g_eff.g[s][visite[0]]
        else:
            tmp=list(g_eff.g[s].keys())
            mini=tmp[0],g_eff.g[s][tmp[0]]
        for x in g_eff.g[s]: # détermine le sommet non visité le plus proche du sommet courant
            if mini[0] in visite and x!=s:
                mini=x,g_eff.g[s][x]
            elif x not in visite and x!=s and mini[1]<g_eff.g[s][x]:
                mini=x,g_eff.g[s][x]
        
        visite.append(s)
        if mini[0] not in visite:
            attente+=[mini[0]]
        if not mini[0] in chemin.chem:
            chemin.chem.append(mini[0])
        
    for i in range(len(chemin.chem)):
        chemin.chem[i]=g_eff.dico[chemin.chem[i]]
        chemin.chem[i].pos=chemin.chem[i].id=i
        chemin.chem[i].pred=chemin.chem[(i-1)%len(chemin.chem)]
        chemin.chem[i].succ=chemin.chem[(i+1)%len(chemin.chem)]
        
        
    return chemin

def opt_2(g,chemin):
    """Implémente l'heuristique 2-opt et considère des permutations
    d'arêtes et renvoie un chemin de coût inférieure ou égale à
    celui du chemin initial"""
    t=chemin
    t.calcul_cout(g)
    t2=t.copy()
    for i in range(len(chemin.chem)-1):
        for j in range(i+2, len(chemin.chem)-2):
            if g.g[chemin.chem[i].nom][chemin.chem[i+1].nom]+g.g[chemin.chem[j].nom][chemin.chem[j+1].nom]>g.g[chemin.chem[i].nom][chemin.chem[j+1].nom]+g.g[chemin.chem[j].nom][chemin.chem[i+1].nom]:
                t2.remplace(i, j, g)
                t2.calcul_cout(g)
                if t2.cout<t.cout:
                    t=t2.copy()
                else:
                    t2=t.copy()
    return t
    
def opt_3(g,chemin):
    """Implémente l'heuristique 3-opt et renvoie un chemin de coût
    inférieur ou égale à celui du chemin initial. 
    Plus efficace que opt_2 mais de complexité temporelle supérieure"""
    t=chemin
    t.calcul_cout(g)
    t2=t.copy()
    for i in range(len(chemin.chem)-1):
        for j in range(i+2, len(chemin.chem)-2):
            for k in range(j+2,len(chemin.chem)-2):
                permutations=list(its.permutations([i,j,k]))[1:]
                for perm in permutations:
                    if g.g[chemin.chem[i].nom][chemin.chem[i+1].nom]+g.g[chemin.chem[j].nom][chemin.chem[j+1].nom]>g.g[chemin.chem[perm[0]].nom][chemin.chem[perm[1]+1].nom]+g.g[chemin.chem[perm[1]].nom][chemin.chem[perm[2]+1].nom]+g.g[chemin.chem[perm[2]].nom][chemin.chem[perm[0]+1].nom]:
                        t2.remplace(perm[0],perm[1],g)
                        t2.remplace(perm[1],perm[1],g)
                        t2.calcul_cout(g)
                        if t2.cout<t.cout:
                            t=t2.copy()
                        else:
                            t2=t.copy()
    return t
