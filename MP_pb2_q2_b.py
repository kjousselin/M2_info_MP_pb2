# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 09:06:07 2022

@author: Kévin Jousselin


https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/anagrammes/anagrammes.html


REMARQUE : penser à modifier le fichier de config : config_q2_b.py : notamment les lignes 'dossier_entree' et 'fichier_mots'.


Question 2_b
    Dans cette version encore améliorée :
        Les anagrammes sont ajoutés à un dictionnaire (les clé étant les mots dont les lettres sont triées par ordre alphabétique).

Conclusion :
    Cette version améliorée dépasse mes attentes en terme d'efficacité : moins de 4 secondes pour 'gutenberg.txt' ainsi que pour 'words'.
    voir les fichiers : 

        bilan_q2_b_gutenberg.txt.txt
        bilan_q2_b_liste_de_tous_les_anagrammes_gutenberg.txt.txt

        bilan_q2_b_words.txt
        bilan_q2_b_liste_de_tous_les_anagrammes_words.txt

    et accessoirement :
        repartition_mots_par_taille_gutenberg.txt.png
        repartition_mots_par_taille_words.png

"""

import time
import numpy as np
import matplotlib.pyplot as plt
import os


# Gestion des entrées et sorties
import config_q2_b

dossier_entree = config_q2_b.dossier_entree
dossier_sortie = config_q2_b.dossier_sortie
fichier_mots = config_q2_b.fichier_mots
fichier_sortie = config_q2_b.fichier_sortie
fichier_sortie2 = config_q2_b.fichier_sortie2

# Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)


# durée totale du programme
T0 = time.time()  


# Récupérer tous les mots du fichier
liste_mots = []
with open(dossier_entree+fichier_mots, encoding = 'utf8') as h:
    for ligne in h:
        liste_mots.append(ligne[:-1])


# Création des deux fichiers de sortie
f = open(dossier_sortie+fichier_sortie, 'w')
f.write(f'Bilan concernant les anagrammes du fichier {fichier_mots}\n')
g = open(dossier_sortie+fichier_sortie2, 'w')
g.write(f'Listes des anagrammes (de plus de deux mots) du fichier {fichier_mots}\n')

# Mode débug : travail sur un nb limité de mots
debug = False
max_debug = 100000
if debug : 
    f.write(f"Mode debug activé : liste rognée à {max_debug} mots :\n")
    g.write(f"Mode debug activé : liste rognée à {max_debug} mots :\n")    
    print(f"Mode debug activé : liste rognée à {max_debug} mots :\n")
    liste_mots = liste_mots[:max_debug]
f.close()
g.close()


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


# Dictionnaire final : les clés sont les mots triés dans l'ordre alphabétique, les valeurs est la liste des anagrammes correspondants
dictionnaire_final = {}


# Parcours des différentes listes de mots
for p, liste_mots in enumerate(Liste_mots_selon_taille):
    
    print(f'\n Traitement des mots de longueur {p} :')        
    nb_mots_sous_liste = len(liste_mots)
    print(f"Nombre de mots de longueur {p} : {nb_mots_sous_liste}")
    
    # Initialisations : ce dictionnaire temporaire regroupera tous les anagrammes dont les mots sont de longueurs 'p'
    dico_temp = {}
    
    t0 = time.time()
    
    for k, mot_k in enumerate(liste_mots):  # Parcours des mots
        
        """
        if k%1000 ==0:          # Visualiser la progression
            print(k,end='\n')
        #print(k,end=' ')
        """
                
        # le mot k est décomposé et trié par ordre alphabétique
        mot_k_trie = list(mot_k)
        mot_k_trie.sort()
        mot_k_trie = "".join(mot_k_trie)
        
        # Le mot_k est ajouté à la liste des anagrammes si la clé existe, sinon la clé est créée
        if dico_temp.get(mot_k_trie) != None:
            dico_temp[mot_k_trie].append(mot_k)
        else:
            dico_temp[mot_k_trie] = [mot_k]

    # Pour répondre à la question :        
    for ana in dico_temp:   
        longueur = len(dico_temp[ana])
        if nb_ensembles_selon_taille.get(longueur) != None:
            nb_ensembles_selon_taille[longueur] += 1       # Ajouter 1 à la clé
        else:
            nb_ensembles_selon_taille[longueur] = 1        # ou bien créer la clé si elle n'existe pas
    
    # Ajouter les anagrammes trouvés au dictionnaire général qui contiendra tous les anagrammes
    dictionnaire_final.update(dico_temp)
        
    t1 = time.time()  

    print(f"Terminé, en {round(t1-t0, 2)} secondes.")

   
    # Iscription des résultats dans les fichiers de sortie
    with open(dossier_sortie+fichier_sortie, 'a') as f:
        f.write(f"Nb de mots de longueur {p} : {nb_mots_sous_liste}\n")
        f.write(f"Nb de listes distinctes d'anagrammes de longueur {p} : {len(dico_temp)}\n")
        
    with open(dossier_sortie+fichier_sortie2, 'a') as g:        
        liste_anag_long_p_hors_mots_seuls = [dico_temp[cle] for cle in dico_temp if len(dico_temp[cle])>1]
        g.write(f"{len(liste_anag_long_p_hors_mots_seuls)} listes d'anagrammes de mots de {p} lettres :\n")
        g.write(f"{liste_anag_long_p_hors_mots_seuls}\n\n")



# durée totale du programme
T1 = time.time()        


# Réponse à la question posée :
f = open(dossier_sortie+fichier_sortie, 'w')
f.write(f"\nRéponse à la question posée :")
print(f"\nRéponse à la question posée :")
for cle in nb_ensembles_selon_taille:
    if cle == 1:
        f.write(f"\nIl y a {nb_ensembles_selon_taille[cle]} mots seuls.")
        print(f"\nIl y a {nb_ensembles_selon_taille[cle]} mots seuls.")
    else:
        f.write(f"\nIl y a {nb_ensembles_selon_taille[cle]} ensembles de {cle} anagrammes.")
        print(f"\nIl y a {nb_ensembles_selon_taille[cle]} ensembles de {cle} anagrammes.")

f.write(f"\nLe programme s'est executé en {(T1-T0)//60} minutes et {round((T1-T0)%60,2)} secondes.\n")
print(f"\nLe programme s'est executé en {(T1-T0)//60} minutes et {round((T1-T0)%60,2)} secondes.\n")

f.close()


    
    


