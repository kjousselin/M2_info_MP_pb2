# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 09:06:07 2022

@author: Kévin Jousselin
"""

"""

https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/anagrammes/anagrammes.html

Anagrammes

On souhaite extraire d’un dictionnaire de mots tous les ensembles d’anagrammes, par exemple :

'subnote', 'subtone', 'unbesot'
'waister', 'waiters', 'wariest', 'wastier', 'wastrie'
'unroyalist', 'unsolitary'
'hydropneumopericardium', 'pneumohydropericardium'
'persécuter', 'récepteurs', 'répercutes'

Plus précisément, on voudrait que le programme d’une part enregistre dans un fichier tous les ensembles trouvés, et d’autre part affiche à l’écran un résumé, à savoir le nombre d’ensembles trouvés par cardinalité, par exemple :

15 ensembles de 2 anagrammes
11 ensembles de 3 anagrammes
8 ensembles de 4 anagrammes

On a 2 jeux de données : le fichier /usr/share/dict/words et ce fichier. L’objectif est d’obtenir ces résultats en un temps acceptable (moins de 5 mn).

Question 1
    Ecrire une première version naïve, la plus simple possible. Conclusion ?

    
    
    Dans cette version naïve : 
        - je récupère tous les mots du document et les insert dans une liste,
        - je parcours les mots 'mot_k' de la liste,
        - je trie ses lettres dans l'ordre alphabétique,
        - puis recherche dans les mots suivants, tous les anagrammes 'mot_i' de 'mot_k'.
        - Je retire tous les anagrammes trouvés au fur et à mesure.
        
    Conclusion : 
        Même si ce premier programme ne réponds pas encore entièrement à la question, le temps de calcul n'est
        pas un temps acceptable (environ 25h !!).

"""

import time
import numpy as np
import os

# Gestion des entrées et sortie

#dossier = 'C:/DocDataM2/S3UE4_info/'
dossier_entree = ""
dossier_sortie = "./resulats/"

fichier_mots = 'words'
#fichier_mots = 'gutenberg.txt'
fichier_sortie = f'bilan_q1_{fichier_mots}.txt'


os.makedirs(dossier_sortie, exist_ok=True)

# Mode debug : limité le nb de mots
debug = True
max_debug = 10000

# Récupérer tous les mots du fichier
liste_mots = []
with open(dossier_entree+fichier_mots, encoding = 'utf8') as f:
    for ligne in f:
        liste_mots.append(ligne[:-1])

# Mode débug
if debug: 
    liste_mots = liste_mots[:max_debug]
    print(f"\nMode debug activé : dico rogné à {max_debug} mots :")


nb_mots = len(liste_mots)                           # Nb de mots récupérés
long_max = max([len(mot) for mot in liste_mots])    # Taille du plus long mot        


# initialisations
nb_mots_restants = nb_mots
Liste_anagrammes = []
nb_ensemble_selon_taille = np.zeros(100, dtype='int')      # L[k] contient le nombre d'ensemble d'anagrammes de cardinal k

print(f"\nNombre de mots du dictionnaire '{fichier_mots}' : {nb_mots}\n")


t0 = time.time()


for k, mot_k in enumerate(liste_mots):  # Parcours des mots
    
    # Suivi de la progression
    if k%1000 ==0:
        print(k,end='\n')
    #print(k,end=' ')
    
    # liste des anagrammes du mot k
    anagrammes_k = [mot_k]      
    
    # le mot k est décomposé et trié par ordre alphabétique
    mot_k_trie = list(mot_k)
    mot_k_trie.sort()    
    
    # Parcours des mots suivants
    for i, mot_i in enumerate(liste_mots[k+1:]):     
               
        # le mot i est décomposé et trié par ordre alphabétique
        mot_i_trie = list(mot_i)
        mot_i_trie.sort()
        
        # Si mot_i est un anagrame de mot_k, alors, on l'ajoute à la liste de ses anagrammes
        if mot_k_trie == mot_i_trie:
            liste_mots.pop(i)                   # on supprime le mot i de la liste pour qu'il ne soit pas testé à nouveau parmi les mots 'k'
            anagrammes_k.append(mot_i)          # Le mot i est ajouté à la liste des anagrammes du mot k

    nb_ensemble_selon_taille[len(anagrammes_k)] += 1            
    if len(anagrammes_k)>1:
        print(f"{anagrammes_k}")
        Liste_anagrammes.append(anagrammes_k)   # La liste des anagrammes du mot k est ajoutée à la liste des anagrammes.
        
        
t1 = time.time()        


# Archivage des résultats dans un fichier de sortie
with open(dossier_sortie+fichier_sortie, 'w') as f:

    if debug : 
        f.write(f"\nMode debug activé : dico rogné à {max_debug} mots :\n")
    
    f.write(f"Temps de recherche : {(t1-t0)//60} minutes et {round((t1-t0)%60,2)} secondes.\n")
    f.write(f"Nombre d'anagrammes trouvés : {len(Liste_anagrammes)}, dont :\n")
    f.write(f"Selon la taille :\n {nb_ensemble_selon_taille}\n\n")
    f.write(f'{Liste_anagrammes}')

# Affichage des résultats dans la console
print(f"Temps de recherche : {(t1-t0)//60} minutes et {round((t1-t0)%60,2)} secondes.")
print(f"Nombre d'anagrammes trouvés : {len(Liste_anagrammes)}, dont :")
print(f"Selon la taille {nb_ensemble_selon_taille}")

    
    
    
    
    
    
    


