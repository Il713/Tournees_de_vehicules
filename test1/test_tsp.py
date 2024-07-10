
from classes import *
from graphe import *
from trajet import *
from repartition import *
from partitionnement import *
import random as rd
from lk import *
from matplotlib import pyplot as plt

from chemin_fourmi import *

import lk_heuristic as lk

from LK_eff import *

import time

from import_graphe_tsp import *

def trace_graphe(graphe,clusters,colors):
    plt.clf()
    
    for s1 in graphe.g:
        for s2 in graphe.g[s1]:
            plt.plot([graphe.dico[s1].x,graphe.dico[s2].x],[graphe.dico[s1].y,graphe.dico[s2].y],linewidth=1,color='k')
    
    for sommet in graphe.g:
        b=True
        for i in range(len(clusters)):
            if sommet in clusters[i]:
                plt.scatter(graphe.dico[sommet].x,graphe.dico[sommet].y,color=colors[i])
                b=False
            
        if b:
            plt.scatter(graphe.dico[sommet].x,graphe.dico[sommet].y,color='k')


def trace_chemin(chemin,col,k):
    for i in range(len(chemin.chem)-1):
        s1,s2 = chemin.chem[i],chemin.chem[i+1]
        plt.plot([s1.x+10000*k,s2.x+10000*k],[s1.y,s2.y],linewidth=1,color=col)
    

g_tsp=Graphe_TSP("a280.tsp")

g_eff=g_tsp.to_graph_eff()
g_eff.simplify()

print('Le graphe a été généré')

nb_mission=1
colors=['r','g','b','c','m','y'] # couleur pour l'affichage d'au plus 6 tournées dans le graphe

resultat={'glouton':[],'2-opt':[],'lin-kernighan':[]}

k=0
clusters=g_tsp.sommets

for _ in range(100000):
    s_t_gl=time.time()
    chem_gl=glouton(g_eff)
    e_t_gl=time.time()
    print("Le chemin glouton est généré")
    s_t2=time.time()
    chem_opt=opt_2(g_eff,chem_gl.copy())
    e_t2=time.time()
    print("Le chemin 2-opt est généré")

    chem_gl2=chem_gl.copy()

    for i in range(len(chem_gl2.chem)):
        chem_gl2.chem[i].id=chem_gl2.chem[i].pos=i
        chem_gl2.chem[i].pere=chem_gl2.chem[(i-1)%len(chem_gl2.chem)]
        chem_gl2.chem[i].fils=chem_gl2.chem[(i+1)%len(chem_gl2.chem)]

    s_t_lk=time.time()
    tsp_data=ppc(g_eff, chem_gl2.copy())
    e_t_lk=time.time()
    chem_lk=Chemin()
    for x in tsp_data.tour.get_nodes():
        chem_lk+=x
    chem_lk.calcul_cout(g_eff)

    chem_gl.calcul_cout(g_eff)
    chem_opt.calcul_cout(g_eff)

    resultat['glouton']+=[(chem_gl.cout,e_t_gl-s_t_gl)]
    resultat['2-opt']+=[(chem_opt.cout, e_t2-s_t2)]
    resultat['lin-kernighan']+=[(chem_lk.cout, e_t_lk-s_t_lk)]

print()
print("Le graphe est",str(g_eff.g))
print("Le chemin obtenu par l'algorithme glouton est",str(chem_gl),", son coût est de",chem_gl.cout,"et il a pris",e_t_gl-s_t_gl)
print("Le chemin obtenu par l'algorithme 2-opt est",str(chem_opt),", son coût est de",chem_opt.cout,"et il a pris",e_t2-s_t2)
print("Le chemin obtenu par l'algorithme de Lin-Kernighan est",str(chem_lk),", son coût est de",chem_lk.cout,"et il a pris",e_t_lk-s_t_lk)
print()
print()
print()
trace_chemin(chem_gl,colors[k],0)
plt.savefig("w.png")
plt.clf()
trace_graphe(g_eff,clusters,colors)
trace_chemin(chem_opt,colors[k+1],0)
plt.savefig("r.png")


