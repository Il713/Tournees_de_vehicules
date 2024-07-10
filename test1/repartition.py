# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:37:28 2023
"""

import numpy as np

def k_means(X, K, max_iters=100):
    """
    Implémentation simple de l'algorithme K-means

    Args:
    X : np.array de taille (N, D) où N est le nombre de données et D est la dimensionnalité
    K : int, nombre de clusters
    max_iters : int, nombre maximum d'itérations

    Returns:
    centers : Liste de Sommets avec les centres de clusters
    assignments : np.array de taille (N,) avec les affectations de cluster pour chaque point
    """
    N, D = len(X),len(X)

    # Initialisation aléatoire des centres de clusters
    centers = X[np.random.choice(np.arange(N), size=K)]

    for _ in range(max_iters):
        # Calcul des distances entre les points de données et les centres
        distances = np.linalg.norm(X[:, np.newaxis] - centers, axis=-1)

        # Affectation de chaque point au cluster le plus proche
        assignments = np.argmin(distances, axis=-1)

        # Mise à jour des centres de clusters
        for k in range(K):
            centers[k] = X[assignments == k].mean(axis=0)

    # Conversion des centres en instances de Sommet
    sommet_centers = [Sommet(x=center[0], y=center[1]) for center in centers]

    return sommet_centers, assignments

def extract_data(graph_dict):
    data = []
    for outer_key in graph_dict:
        for inner_key in graph_dict[outer_key]:
            sommet = graph_dict[outer_key][inner_key]
            data.append([sommet.x, sommet.y])
    return np.array(data)

def apply_k_means(graph_dict, K, max_iters=100):
    return k_means(graph_dict, K, max_iters)

