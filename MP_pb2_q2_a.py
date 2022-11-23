# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 09:06:07 2022

@author: Kévin Jousselin
"""

"""

https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/anagrammes/anagrammes.html

Question 2    
    Dans cette version améliorée :  J'ai remarqué que les anagrammes avaient la même taille,
                                    J'ai donc commencé par regrouper les mots de la même taille

Conclusion :
    Cette première version améliorée divise le temps de travail par 5 (durée environ 5h au lieu de 25h, mais ce n'est pas satisfaisant)
    voir les fichiers : 
        
        bilan_q2_a_gutenberg.txt.txt
        bilan_q2_a_liste_de_tous_les_anagrammes_gutenberg.txt.txt
        
        bilan_q2_a_words.txt
        bilan_q2_a_liste_de_tous_les_anagrammes_words.txt    
        
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import os


# Gestion des entrées et sorties

#dossier = 'C:/DocDataM2/S3UE4_info/'
dossier_entree = ""
dossier_sortie = "./resulats/"

fichier_mots = 'gutenberg.txt'
#fichier_mots = 'words'

fichier_sortie = f'bilan_q2_a_{fichier_mots}.txt'
fichier_sortie2 = f'bilan_q2_a_liste_de_tous_les_anagrammes_{fichier_mots}.txt'

os.makedirs(dossier_sortie, exist_ok=True)


# Récupérer tous les mots du fichier
liste_mots = []
with open(dossier_entree+fichier_mots, encoding = 'utf8') as h:
    for ligne in h:
        liste_mots.append(ligne[:-1])


# durée totale du programme
T0 = time.time()        


# Création des deux fichiers de sortie
f = open(dossier_sortie+fichier_sortie, 'w')
g = open(dossier_sortie+fichier_sortie2, 'w')

# Mode débug : travail sur un nb limité de mots
debug = True
max_debug = 100000
if debug : 
    f.write(f"Mode debug activé : liste rognée à {max_debug} mots :\n")
    g.write(f"Mode debug activé : liste rognée à {max_debug} mots :\n")    
    print(f"Mode debug activé : liste rognée à {max_debug} mots :\n")
    liste_mots = liste_mots[:max_debug]
g.close()
f.close()


nb_mots = len(liste_mots)                           # Nb de mots récupérés
long_max = max([len(mot) for mot in liste_mots])    # Taille du plus long mot        


f = open(dossier_sortie+fichier_sortie, 'a')
f.write(f"Le fichier '{fichier_mots}' contient {nb_mots} mots.\n\n")
f.close()


# Trie par taille : création de la liste de liste (vide)
Liste_mots_selon_taille = [] 
for k in range(0, long_max+1):
    Liste_mots_selon_taille.append([])                  # L = [ [], [], ..., [] ]

    
# Trie par taille : ajout des mots dans les listes : Liste_mots_selon_taille[k] est la liste des anagrammes de taille k
for mot in liste_mots:
    (Liste_mots_selon_taille[len(mot)]).append(mot)     # L[3] = ['1st','2nd', '3-D', '3-d', '3rd', ... ]


# Histogramme des longueurs de mot (répartition des most selon la taille)
long = []    
for liste in Liste_mots_selon_taille:
    long.append(len(liste))   
plt.hist(range(long_max+1), weights = long , bins = range(long_max+1))
plt.xlabel('Longueur du mots (nombre de caractères)')
plt.ylabel('Nombre de mots')
plt.title(f'Répartition du nombre de mots en fonction\nde la longueur dans le fichier "{fichier_mots}"')
plt.savefig(dossier_sortie+f"repartition_mots_par_taille_{fichier_mots}.png")
plt.show()


# Dictionnaire dic[k] contient le nombre d'ensemble d'anagrammes de cardinal k
nb_ensembles_selon_taille = {}      


# Parcours des différentes listes de mots (la liste p-ième liste contient les mots à p caractères)
for p, liste_mots in enumerate(Liste_mots_selon_taille):
    
    print(f'\n Traitement des mots de longueur {p} :')
    nb_mots_sous_liste = len(liste_mots)
    print(f"Nombre de mots de longueur {p} : {nb_mots_sous_liste}")

    # initialisations
    nb_mots_restants = nb_mots_sous_liste
    Liste_anagrammes_long_p = []    
    
    t0 = time.time()
    
    #k = 0
    
    for k, mot_k in enumerate(liste_mots):  # Parcours des mots
        
        """
        if k%1000 ==0:          # Visualiser la progression
            print(k,end='\n')
        #print(k,end=' ')
        """
        
        anagrammes_k = [mot_k]      # liste des anagrammes du mot k
        
        # le mot k est décomposé et trié par ordre alphabétique
        mot_k_trie = list(mot_k)
        mot_k_trie.sort()    
        
        # Parcours des mots suivants pour rechercher ses anagrammes
        for i, mot_i in enumerate(liste_mots[k+1:]):     
                   
            # le mot i est décomposé et trié par ordre alphabétique
            mot_i_trie = list(mot_i)
            mot_i_trie.sort()
            
            # Si mot_i est un anagrame de mot_k, alors, on l'ajoute à la liste de ses anagrammes
            if mot_k_trie == mot_i_trie:
                liste_mots.pop(i)                   # on supprime le mot i de la liste pour qu'il ne soit pas testé à nouveau parmi les mots 'k'
                anagrammes_k.append(mot_i)          # Le mot i est ajouté à la liste des anagrammes du mot k
        
        # Pour répondre à la question :
        try :
            nb_ensembles_selon_taille[len(anagrammes_k)] += 1       # Ajouter 1 à la clé           
        except:
            nb_ensembles_selon_taille[len(anagrammes_k)] = 1        # ou bien créer la clé si elle n'existe pas
                
        if len(anagrammes_k)>1:
            Liste_anagrammes_long_p.append(anagrammes_k)   # La liste des anagrammes du mot k est ajoutée à la liste des anagrammes.
            
    t1 = time.time()  

    print(f"Terminé, en {round(t1-t0, 2)} secondes.")

    # Iscription des résultats dans les fichiers de sortie
    with open(dossier_sortie+fichier_sortie, 'a') as f:
        f.write(f"Nb de mots de longueur {p} : {nb_mots_sous_liste}\n")
        f.write(f"Nb de listes distinctes d'anagrammes de longueur {p} : {len(Liste_anagrammes_long_p)}\n")
        
    with open(dossier_sortie+fichier_sortie2, 'a') as g:
        g.write(f"Anagrammes de longueur {p} :\n{Liste_anagrammes_long_p}\n\n")


# durée totale du programme
T1 = time.time()        


# Réponse à la question posée : inscription dans les fichiers de sortie
f = open(dossier_sortie+fichier_sortie, 'a')
f.write(f"\nRéponse à la question posée : \n")
print(f"\nRéponse à la question posée : \n")
for cle in nb_ensembles_selon_taille:
    if cle == 1:
        f.write(f"\nIl y a {nb_ensembles_selon_taille[cle]} mots seuls.")
        print(f"\nIl y a {nb_ensembles_selon_taille[cle]} mots seuls.")
    else: 
        f.write(f"\nIl y a {nb_ensembles_selon_taille[cle]} ensembles de {cle} anagrammes.")
        print(f"\nIl y a {nb_ensembles_selon_taille[cle]} ensembles de {cle} anagrammes.")

f.write(f"\nLe programme s'est executé en {(T1-T0)//60} minutes et {round((t1-t0)%60,2)} secondes.\n")
print(f"\nLe programme s'est executé en {(T1-T0)//60} minutes et {round((t1-t0)%60,2)} secondes.\n")

f.close()

