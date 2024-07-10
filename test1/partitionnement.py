
from classes import *
from graphe import *
import random as rd
import numpy as np

def k_moyenne(K,g,f_chem,max_iters=100000):
    
    l=list(g.g.keys())
    P=[]
    G=np.inf
    sommets=[]
    for i in range(len(l)):
        sommets+=[g.dico[l[i]]]
    l2=sommets.copy()
    
    indices=np.random.choice(len(sommets), K, replace=False)
    centroids = [sommets[i] for i in indices]

    for _ in range(max_iters):
        labels = {sommet: np.argmin([np.sqrt((sommet.x - c.x)**2 + (sommet.y - c.y)**2) for c in centroids]) for sommet in sommets}

        new_centroids = [Sommet(np.mean([s.x for s in sommets if labels[s] == k]),
                                np.mean([s.y for s in sommets if labels[s] == k]),
                                "centroid_"+str(k)) for k in range(K)]

        
        
        if all(c1.x == c2.x and c1.y == c2.y for c1, c2 in zip(centroids, new_centroids)):
            break

        centroids = new_centroids

    return centroids, labels
