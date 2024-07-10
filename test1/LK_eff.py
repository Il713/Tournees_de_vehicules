
import lk_heuristic.models.tsp as lk

from lk_heuristic.utils.cost_funcs import euc_2d

import math
import logging
import time

def d(n1,n2):
    
    return ((n1.x-n2.x)**2+ (n1.y-n2.y)**2)**0.5

def ppc(graphe2, chemin2):
    """ Détermine le plus court chemin en exploitant 
        l'heuristique de Lin-Kernighan"""
    chemin=chemin2.chem
    graphe=graphe2.g
    
    def d2(n1,n2):
        if n1==n2:
            return 0 
        else:
            return graphe[n1.nom][n2.nom]
            
    
    bt=(5,5)
    red_lvl=4
    red_cycle=4
    tour_type='cycle'
    file_name=None
    runs=1
    solution_method='lk2_improve'
    
    best_tour=None
    best_cost=math.inf
    mean_cost=0
    tsp=lk.Tsp(chemin, d2, False, bt, red_lvl, red_cycle, tour_type, logging.DEBUG)
    
    for run in range(1, runs+1):
        if tsp.shuffle:
            tsp.tour.shuffle()
    
        tsp.tour.set_cost(tsp.cost_matrix)
        
        print('start')
        start_time=time.time()
        tsp.methods[solution_method]()
        end_time=time.time()
        print('end')
        
        if tsp.tour.cost < best_cost:
            best_tour=tsp.tour.get_nodes()
            best_cost= tsp.tour.cost
        mean_cost+= (tsp.tour.cost-mean_cost)/run
    
        print(f"[Run:{run}] --> Cost: {tsp.tour.cost:.3f} / Best: {best_cost:.3f} / "+
              "Mean: {mean_cost:.3f} ({end_time - start_time:.3f}s)")
    
    return tsp
