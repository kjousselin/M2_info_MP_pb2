# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 09:06:07 2022

@author: Kévin Jousselin


https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/anagrammes/anagrammes.html


REMARQUE : penser à modifier le fichier de config : config_q3.py : notamment les lignes 'dossier_entree' et 'fichier_mots'.

Question 3
    Paralléliser l’algorithme et l’implémenter à l’aide du module multiprocessing.

Conclusion :
    Cette version avec multiprocessing est, bien que performante, plus lente (environ 30 secondes pour l'un ou l'autre des fichiers)
    
    Ceci peut être expliqué ainsi : les processus sont rapides (individuellement) mais leur chargement est lent. 
                                    l'algorithme serait plus efficace avec des processus dont l'exécution serait plus lente
                                    
                              
    voir les fichiers-bilan : 
        
        bilan_q3_gutenberg.txt.txt
        bilan_q3_liste_de_tous_les_anagrammes_gutenberg.txt.txt
        
        bilan_q3_words.txt
        bilan_q3_liste_de_tous_les_anagrammes_words.txt    
    
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import os


# Gestion des entrées et sorties
import config_q3

dossier_entree = config_q3.dossier_entree
dossier_sortie = config_q3.dossier_sortie
fichier_mots = config_q3.fichier_mots
fichier_sortie = config_q3.fichier_sortie
fichier_sortie2 = config_q3.fichier_sortie2

# Création du dossier de sortie s'il n'existe pas
os.makedirs(dossier_sortie, exist_ok=True)



class MyProcess_recherche(multiprocessing.Process):
    
    def __init__(self, liste_mots, queue_taille):
        multiprocessing.Process.__init__(self)   # Obligatoire
        self.liste_mots = liste_mots
        self.queue_taille = queue_taille

    def run(self):        
        
        for sous_liste in self.liste_mots:
            
            # longueur des mots considérés
            p = len(sous_liste[1][0])   
        
            # Nb de mots dans la sous_liste considérée
            print(f'\n Traitement des mots de longueur {p} :')
            nb_mots_sous_liste = sous_liste[0]    
            print(f"Nombre de mots de longueur {p} : {nb_mots_sous_liste}")
            
            # on extrait uniquement les mots
            sous_liste = sous_liste[1]  
            
            # Initialisations : ce dictionnaire temporaire regroupera tous les anagrammes dont les mots sont de longueurs 'p'
            dico_temp = {}
            
            t0 = time.time()
            
            # Parcours des mots
            for k, mot_k in enumerate(sous_liste):  
                
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
                self.queue_taille.put(longueur)

        
            # Iscription des résultats dans les fichiers de sortie
            with open(dossier_sortie+fichier_sortie, 'a') as f:
                f.write(f"Nb de mots de longueur {p} : {nb_mots_sous_liste}\n")
                f.write(f"Nb de listes distinctes d'anagrammes de longueur {p} : {len(dico_temp)}\n")
                
            with open(dossier_sortie+fichier_sortie2, 'a') as g:        
                liste_anag_long_p_hors_mots_seuls = [dico_temp[cle] for cle in dico_temp if len(dico_temp[cle])>1]
                g.write(f"{len(liste_anag_long_p_hors_mots_seuls)} listes d'anagrammes de mots de {p} lettres :\n")
                g.write(f"{liste_anag_long_p_hors_mots_seuls}\n\n")        
                
                
            t1 = time.time()  
            print(f"Terminé, en {round(t1-t0, 2)} secondes.")


# Cette classe de processus récupère les données de la queue pour les traiter
class MyProcess_archivage(multiprocessing.Process):
           
    def __init__(self, queue_taille, queue_rep):
        multiprocessing.Process.__init__(self)   # Obligatoire
        self.queue_taille = queue_taille
        self.queue_rep = queue_rep
        self.dico_rep = None

    def run(self):

        nb_ensembles_selon_taille = {}

        # Récupération des données de la queue : longueur des listes d'anagrammes        
        while not self.queue_taille.empty():
            longueur = self.queue_taille.get()
            
            if nb_ensembles_selon_taille.get(longueur) != None:
                nb_ensembles_selon_taille[longueur] += 1       # Ajouter 1 à la clé
            else:
                nb_ensembles_selon_taille[longueur] = 1        # ou bien créer la clé si elle n'existe pas
            #print(queue_taille.qsize())
                
        # Envoie de la réponse
        self.queue_rep.put(nb_ensembles_selon_taille)


if __name__ == '__main__':


    display = True    
    display_graph = config_q3.display_graph   # True or False

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
    g.write(f'Listes des anagrammes (de plus de deux mots) du fichier "{fichier_mots}":\n\n')
    
        
    # Mode débug : travailler éventuellement sur un nb limité de mots
    debug = config_q3.debug     # True or False
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
        (Liste_mots_selon_taille[len(mot)]).append(mot)     # exemple : L[3] = ['1st','2nd', '3-D', '3-d', '3rd', ... ]
    
    
    # Histogramme des longueurs de mot (répartition des most selon la taille)
    long = []    
    for liste in Liste_mots_selon_taille:
        long.append(len(liste))   
    plt.hist(range(long_max+1), weights = long , bins = range(long_max+1))
    plt.xlabel('Longueur du mots (nombre de caractères)')
    plt.ylabel('Nombre de mots')
    plt.title(f'Répartition du nombre de mots en fonction\nde la longueur dans le fichier "{fichier_mots}"')
    plt.savefig(dossier_sortie+f"repartition_mots_par_taille_{fichier_mots}.png")
    if display_graph: plt.show()
    

    # Suppression des listes vides
    while [] in Liste_mots_selon_taille:
        Liste_mots_selon_taille.remove([])
    
    
    # Création de deux files de de partage permettant de récupérer et de traiter les réponses à la question (le nombre d’ensembles trouvés par cardinalité)
    queue_taille = multiprocessing.Queue()   
    queue_rep = multiprocessing.Queue()   
   
    
    # Afin de découper et répartir efficacement les mots dans les différents processus, nous allons transformer et trier la liste de liste de mots
    for l, liste in enumerate(Liste_mots_selon_taille):
        quantite = len(liste)
        Liste_mots_selon_taille[l] = (len(liste), liste)
    Liste_mots_selon_taille.sort(reverse = True)
    
    
    # Répartition des listes de mots dans les différents processus
    Decoupage_liste = []
    Nb_processus = len(Liste_mots_selon_taille)
    
    Nb_processus = config_q3.Nb_processus
    
    for div in range(Nb_processus-1):    
        Decoupage_liste.append([Liste_mots_selon_taille[div]])      # les Nb_processus recoivent une liste de mots de longueur p
    Decoupage_liste.append(Liste_mots_selon_taille[Nb_processus:])  # le dernier processus recoit le reste
    
    """
    # REFLEXION POUR UNE MEILLEUR REPARTITION DES LISTES SUR LES PROCESSUS : NON ABOUTI
    Nb_processus = 10
    moy_mots_par_proc = nb_mots / Nb_processus 
    Decoupage_liste = [ [Liste_mots_selon_taille[0]] ]
    compt_m = Decoupage_liste[0][0][0]   # Nb de mots
    compt_l = 1
    m = 1
    while m < Nb_processus-2:
        print("compt m ICI",compt_m)
        print("compt l ICI",compt_l)
        
        while compt_m < moy_mots_par_proc:
            print("\tcompt m LA",compt_m)
            print("\tcompt l LA",compt_l)
            print()
            
            Decoupage_liste[-1].append( Liste_mots_selon_taille[compt_l])
            compt_m += Liste_mots_selon_taille[compt_l][0]  #nb de mots
            compt_l += 1
            
            print("\tcompt m LA",compt_m)
            print("\tcompt l LA",compt_l)
            print()
        
        compt_m = Liste_mots_selon_taille[compt_l][0]  # nb de mots
        #Decoupage_liste.append( [Liste_mots_selon_taille[m]] )
        m += 1
        compt_l += 1
        
    for k in range(Nb_processus-1):
        print('\n\n\n')
        print(len(Decoupage_liste[k]))
        print(Decoupage_liste[k][0][0])
    """
    
                
    # Dispatch des jobs pour les Nb_processus processus, puis chargement des processus 'MyProcess_recherche' dans une liste
    liste_processus = []
    if display: print('Chargement des processus :')
    for listes in Decoupage_liste:
        L_for_1_proc = listes           # Contient la liste des mots destinés à un processus
        liste_processus.append(MyProcess_recherche(L_for_1_proc, queue_taille))  
    if display : print('terminé')
        
    
    # Active ou désactive le lancement du processus 'MyProcess_archivage'
    depart_arch = True    
    
    
    # Lancement du premier processus 'MyProcess_recherche' permettant de recherche les anagrammes :
    liste_processus[0].start()  

    
    # Lancement du processus 'MyProcess_archivage' permettant de vider la queue,
    #  et de récupérer les informations correspondant à la question (le nombre d’ensembles trouvés par cardinalité)
    process_recherche = MyProcess_archivage(queue_taille, queue_rep)
    process_recherche.start()

    
    # Lancement des processus suivant 'MyProcess_recherche' permettant de recherche les anagrammes :
    if display : print('Lancement des processus :')
    for processus in liste_processus[1:]:
        processus.start()  
    if display : print('terminé')

    
    # Attente des processus 'MyProcess_recherche'
    if display : print('Attente des processus :')
    for processus in liste_processus:
        processus.join()   # La méthode join bloque la suite du programme
                           # tant que le programme 'processus' n'est pas terminé
    
    
    # Attente du processus 'MyProcess_archivage'
    if display : print('\nAttente du processus de récupération des informations :')
    process_recherche.join()
    if display : print('terminé')
    
    
    # Vérifier que les process sont terminés :
    # print([processus.is_alive() for processus in liste_processus])
    
        
    # durée totale du programme
    T1 = time.time()        
    
    
    # Réponse à la question posée : Récupérer les résultats dans la queue
    nb_ensembles_selon_taille = queue_rep.get()
    
    
    # Réponse à la question posée : Affichage et inscription des résulats dans un fichier :
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
    
    f.write(f"\nLe programme s'est executé en {int((T1-T0)//60)} minute(s) et {round((T1-T0)%60,2)} seconde(s).\n")
    print(f"\nLe programme s'est executé en {int((T1-T0)//60)} minute(s) et {round((T1-T0)%60,2)} seconde(s).\n")
    
    f.close()


