# -*- coding: utf-8 -*-
"""
Created on Wed May 31 18:07:19 2023
"""
import numpy as np
import random as rd


def pos_init(n, N):
    L=[]
    for i in range(0,N):
        L=L+[[rd.randint(0, n-1)]]
    return L

def liste_proba(i,LS,A,B,n,alpha,beta):
    LP=[0]*n
    S=0
    for k in range(n):
        if k not in LS:
            S=S+B[i][k]**alpha * A[i][k]**(-beta)
    for j in range(n):
        if j not in LS:
            LP[j]=B[i][j]**alpha *A[i][j]**alpha/S
    return LP

def choix_sommet(LP):
    a=rd.random()
    S=LP[0]
    i=0
    while S<a:
        i+=1
        S+=LP[i]
    return i

def tour_complet(A,B,n,N, alpha, beta):
    L=pos_init(n,N)
    for i in range(0,n-1):
        for f in range(N):
            LP=liste_proba(L[f][-1],L[f], A,B,n,alpha, beta)
            j=choix_sommet(LP)
            L[f]=L[f]+[j]
    return L

def actualise_pheromones(L,A,B,n,N,r):
    for i in range(n):
        for j in range(n):
            B[i][j]=r*B[i][j]
    for f in range(N):
        S=0
        for i in range(n-1):
            S=S+A[L[f][i]][L[f][i+1]]
        for i in range(n-1):
            B[L[f][i]][L[f][i+1]]=B[L[f][i]][L[f][i+1]]+1/S
    return B


def plus_court_chem(A,N,NV,r, alpha, beta):
    n=len(A)
    B=[[0.01 for i in range(n)]for j in range(n)]
    lmin=float('inf')
    for i in range(0,NV):
        L=tour_complet(A,B,n,N,alpha,beta)
        B=actualise_pheromones(L, A, B, n, N, r)
        for f in range(N):
            S=0
            for i in range(n-1):
                S=S+A[L[f][i]][L[f][i+1]]
            if S<lmin:
                lmin=S
                Ll=L[f]
    return lmin, Ll
        