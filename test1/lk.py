
from classes import *
from trajet import *
from graphe import *

def verifier_tour(tour,t,graph):
    t1,t2=t
    nouveau_tour=tour.copy()
    nouveau_tour.chem=nouveau_tour.chem[:t1+1]+nouveau_tour.chem[t2:t1:-1]+nouveau_tour.chem[t2+1:]
    tour.calcul_cout()
    nouveau_tour.calcul_cout()
    
    if set(nouveau_tour.chem) != set(graph.g.keys()):
        return None,False
    
    return nouveau_tour,True

def choix_y1(c_xi,i,chemin,g):
    for j in range(i+1,len(chemin.chem)-1):
        if c_xi - g.g[chemin.chem[i]][chemin.chem[j]] > 0:
            return (i,j)
    return None

def choix_xi(Y,x1,chemin,g):
    b=True
    for j in range(len(chemin.chem)-1):
        if b:
            b=False
            chemin2,b2=verifier_tour(chemin,(j,x1[0]),g)
            xi=(x1[-1],j)
            if b2:
                for yi in Y:
                    if yi==xi:
                        b=True
        if not b:
            return xi,chemin2
            
        
    return None,Chemin()

def choix_yi(X,Y,gain,chemin,g):
    c_xi=g.g[chemin.chem[X[-1][0]]][chemin.chem[X[-1][1]]]
    for j in range(X[-1][-1]+1,len(chemin.chem)-1):
        if gain + c_xi - g.g[chemin.chem[X[-1][-1]]][chemin.chem[j]]>0:
            yi=(X[-1],j)
            b=True
            for x in X:
                if yi==X[-1]:
                    b=False
            if b:
                if choix_xi(Y+[yi],X[0],chemin,g)[0]!=None:
                    return yi,c_xi - g.g[chemin.chem[X[-1][-1]]][chemin.chem[j]]
    return None,False
                    

def LK(g,chemin):

    for i in range(len(chemin.chem)):
        k=1
        x1=(i,(i+1)%len(chemin.chem))
        c_x1=g.g[chemin.chem[i]][chemin.chem[i+1]]
        y1=choix_y1(c_x1,i+1,chemin,g)
        X,Y=[x1],[y1]
        gain=0
        if y1:
            b=True
            while b:
                k+=1
                xi,chemin2=choix_xi(Y,x1,chemin,g)
                if xi==None:
                    b=False
                if chemin2.cout<chemin.cout:
                    chemin=chemin2.copy()
                    k=1
                    b=False
                b2=True
                while b and b2:
                    yi,gain_int=choix_yi(X,Y,gain,chemin,g)
                    if yi==None:
                        k=2
                        X,Y=X[:1],Y[:1]
                        b=False
                    gain+=gain_int
                    b2=False
        
    return chemin
            
            
def get_neighbours_not_in_tour(node, tour):
    neighbours = graphe.g[node]  # Supposez que graphe.g[node] renvoie tous les voisins de node
    return [neighbour for neighbour in neighbours if neighbour not in tour]
            

def lin_kernighan(graphe, chemin_initial):
    chemin_meilleur = chemin_initial
    amelioration = True

    while amelioration:
        amelioration = False
        for t1 in chemin_initial.chem:
            i = 1
            x_choices = [(t1, t2) for t2 in chemin_initial.chem if t1 != t2]
            for x1 in x_choices:
                y_choices = [(x1[1], t3) for t3 in graphe.g.keys() if (x1[1], t3) not in x_choices]
                for y1 in y_choices:
                    if y1[1]!=y1[0]:
                        G1 = graphe.g[x1[1]][x1[0]] - graphe.g[y1[1]][y1[0]]
                        if G1 > 0:
                            i += 1
                            x2_choices = [(y1[1], t2) for t2 in chemin_initial.chem if y1[1] != t2 and (y1[1], t2) != y1]
                            for x2 in x2_choices:
                                if (x2[1], t1) in chemin_initial.chem and x2 != y1:
                                    nouveau_chemin = chemin_initial.chem[:]
                                    # Reverse the segment between x1[1] and x2[0]
                                    start = nouveau_chemin.index(x1[1])
                                    end = nouveau_chemin.index(x2[0])
                                    if start < end:
                                        nouveau_chemin[start:end+1] = reversed(nouveau_chemin[start:end+1])
                                    else:
                                        nouveau_chemin[end:start+1] = reversed(nouveau_chemin[end:start+1])
                                    nouveau_cout = sum(graphe.g[nouveau_chemin[k]][nouveau_chemin[k+1]] for k in range(len(nouveau_chemin)-1))
                                    if nouveau_cout < chemin_meilleur.cout:
                                        chemin_meilleur = Chemin(nouveau_chemin, nouveau_cout)
                                        amelioration = True
                                        break
        chemin_initial = chemin_meilleur
    return chemin_meilleur
            

def trouver_indice(l,x):
    n=len(l)
    trouve=False
    i=0
    while i<n and not trouve:
        if l[i]==x:
            trouve=True
        else:
            i+=1
    return i

def dejapris(t,n):
    trouve=False
    i=0
    while i<n and not trouve:
        if t[i]==t[n]:
            trouve=True
        else:
            i+=1
    return trouve

def copier(v,w):
    if len(w.chem)<len(v.chem):
        w.chem=v.chem.copy()
    else:
        for i in range(len(w.chem)):
            w.chem[i]=v.chem[i]
    
def est_mieux(g,i,G,t,chemin):
    G=0
    for j in range(i):
        G+=g.g[chemin.chem[t[2*j]]][chemin.chem[t[2*j+1]]]-g.g[chemin.chem[t[2*j+1]]][chemin.chem[t[2*j+2]]]
    G+=g[chemin.chem[t[2*i]]][chemin.chem[t[2*i+1]]]
    return G-g[chemin.chem[t[2*i+1]]][chemin.chem[0]]>0

def yvoisin(i,x):
    a=2*i+2
    if x%2==0:
        b=x+a-1
    else:
        b=x+1
    return b%a


def est_un_tour(chemin,nouvc,t,i,n):
    sens=1
    nbcases=0
    ind=0
    saut=False
    c=Chemin()
    c.chem=[0]*n
    copier(c,nouvc)
    while ind!=0 or nbcases==0:
        if nbcases<len(nouvc.chem):
            nouvc.chem[nbcases]=chemin.chem[ind%len(chemin.chem)]
        else:
            nouvc=nouvc+chemin.chem[ind]
        if len(t)<2*i+3:
            dep=trouver_indice(t[0:],chemin.chem[ind%len(chemin.chem)])
                                        
        else:
            dep=trouver_indice(t[0:2*i+2],chemin.chem[ind%len(chemin.chem)])
        if dep==2*i+2 or saut:
            ind=(ind+sens)%n
            saut=False
        else:
            arr=yvoisin(i,dep)
            ind=trouver_indice(chemin.chem,t[arr])
            saut=True
            if arr%2==0:
                k=arr+1
            else:
                k=arr-1
            if chemin.chem[ind-1]==t[k]:
                sens=1
            else:
                sens=-1
    return nbcases==n
            
    


def LK(g,chemin):
    n=len(chemin.chem)
    t=[-1]*n
    dic={}
    for i in range(n):
        dic[chemin.chem[i]]=i
    tcomp=[0]*(n+1)
    c2=Chemin()
    c2.chem=[0]*n
    nouvc=Chemin()
    copier(c2,nouvc)
    print(type(nouvc))
    i=0
    tvois=0
    G=0
    
    def etape2():
        i=0
        t[0]=tcomp[0]
        tcomp[0]=tcomp[0]+1
        tcomp[1]=0
        etape3()
    def etape3():
        ind=trouver_indice(chemin.chem, chemin.chem[t[0]])
        if tcomp[i]==0:
            t[1]=dic[chemin.chem[(ind+1)%n]]
            tvois=dic[chemin.chem[(ind+2)%n]]
        else:
            t[1]=dic[chemin.chem[(ind+n-1)%n]]
            tvois=dic[chemin.chem[(ind+n-2)%n]]
        tcomp[1]=tcomp[1]+1
        tcomp[2]=0
        etape4()
    def etape4():
        if tcomp[2]!=t[0] and tcomp[2]!=t[1] and tcomp[2]!=tvois and chemin.chem[t[0]]!=chemin.chem[t[1]] and chemin.chem[t[1]]!=chemin.chem[tcomp[2]] and g.g[chemin.chem[t[0]]][chemin.chem[t[1]]]-g.g[chemin.chem[t[1]]][chemin.chem[tcomp[2]]] :
            t[2]=tcomp[2]
            tcomp[2]=tcomp[2]+1
            tcomp[3]=0
            etape5()
        else:
            tcomp[2]=tcomp[2]+1
            if tcomp[2]==n:
                etape11()
            else:
                etape4()
    def etape5():
        nonlocal i
        i+=1
        etape6()
    def etape6():
        ind=trouver_indice(chemin.chem,chemin.chem[t[2*i]])
        if tcomp[2*i+1]==0:
            t[2*i+1]=chemin.chem[(ind+1)%n]
            tvois=chemin.chem[(ind+2)%n]
        else:
            t[2*i+1]=chemin.chem[(ind+n-1)%n]
            tvois=chemin.chem[(ind+n-2)%n]
        tcomp[2*i+1]=tcomp[2*i+1]+1
        if not dejapris(t,2*i+1) and est_un_tour(chemin,nouvc,t,i,n):
            if est_mieux(g,i,G,t,chemin):
                copier(nouvc,chemin)
                etape12()
            else:
                tcomp[2*i+2]=0
                etape7()
        else:
            if tcomp[2*i+1]==2:
                etape8()
            else:
                etape6()
    def etape7():
        t[2*i+2]=tcomp[2*i+2]
        tcomp[2*i+2]+=1
        if not(dejapris(t,2*i+2) and t[2*i+2]!=tvois and G-g.g[chemin.chem[t[2*i+1]]][chemin.chem[t[2*i+2]]]>0):
            tcomp[2*i+3]=0
            etape5()
        else:
            if comp[2*i+2]==n:
                etape8()
            else:
                etape7()
        
    def etape8():
        if tcomp[4]==n:
            etape9()
        else:
            i=1
            etape7()
    def etape9():
        if tcomp[3]==2:
            etape10()
        else:
            i=1
            etape6()
    def etape10():
        if tcomp[2]==n:
            etape11()
        else:
            i=0
            etape4()
    def etape11():
        if tcomp[1]==2:
            etape12()
        else:
            i=0
            etape3()
    def etape12():
        if tcomp[0]==n:
            return chemin.chem
        else:
            etape2()
    
    return etape2()
        

def get_neighbors(node, tour, exclude=[]):
    return [n for n in tour if n != node and n not in exclude]

def get_next(tour, node):
    idx = tour.index(node)
    return tour[(idx + 1) % len(tour)]

def two_opt_swap(tour, sequence):
    i1 = tour.index(sequence[0])
    i2 = tour.index(sequence[2])
    i3 = tour.index(sequence[4])
    return tour[:i1+1] + tour[i1+1:i2+1][::-1] + tour[i2+1:i3+1] + tour[i3+1:]

def LK(graphe, tour):
    b=True
    while b:
        max_gain = 0
        for t1 in tour.chem:
            for x1 in get_neighbors(t1, tour.chem):
                t2 = get_next(tour.chem, x1)
                for y1 in get_neighbors(t2, tour.chem, exclude=[x1]):
                    t3 = get_next(tour.chem, y1)
                    if t1!=t2 and t2!=t3:
                        g1 = graphe.g[t1][t2] - graphe.g[t2][t3]
                        if g1 > 0:
                            for x2 in get_neighbors(t3, tour.chem, exclude=[t2]):
                                t4 = get_next(tour.chem, x2)
                                for y2 in get_neighbors(t4, tour.chem, exclude=[t3, x1]):
                                    t5 = get_next(tour.chem, y2)
                                    if t3!=t4 and t4!=t5:
                                        g2 = g1 + graphe.g[t3][t4] - graphe.g[t4][t5]
                                        if g2 > max_gain:
                                            max_gain = g2
                                            best_sequence = [t1, t2, t3, t4, t5]
        if max_gain > 0:
            tour.chem = two_opt_swap(tour.chem, best_sequence)
        else:
            b=False
    return tour

def LK(graphe, tour, max_iterations_without_improvement=1000):
    iterations_without_improvement = 0
    while iterations_without_improvement < max_iterations_without_improvement:
        max_gain = 0
        for t1 in tour.chem:
            for x1 in get_neighbors(t1, tour.chem):
                t2 = get_next(tour.chem, x1)
                for y1 in get_neighbors(t2, tour.chem, exclude=[x1]):
                    t3 = get_next(tour.chem, y1)
                    g1 = graphe.g[t1][t2] - graphe.g[t2][t3]
                    if g1 > 0:
                        for x2 in get_neighbors(t3, tour.chem, exclude=[t2,t3]):
                            t4 = get_next(tour.chem, x2)
                            for y2 in get_neighbors(t4, tour.chem, exclude=[t3, x1, t4]):
                                t5 = get_next(tour.chem, y2)
                                g2 = g1 + graphe.g[t3][t4] - graphe.g[t4][t5]
                                if g2 > max_gain:
                                    max_gain = g2
                                    best_sequence = [t1, t2, t3, t4, t5]
        if max_gain > 0:
            tour.chem = two_opt_swap(tour.chem, best_sequence)
            iterations_without_improvement = 0
        else:
            iterations_without_improvement += 1
    return tour