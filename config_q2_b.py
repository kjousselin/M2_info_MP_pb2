

########################### CONFIGURATION (Entrées/Sorties/Debug) du programme de la PB2 QUESTION 3 ########################## 


############ Dossier et fichiers entrées ############

#dossier_entree = 'C:/DocDataM2/S3UE4_info/'
dossier_entree = ""

# cas des urls non traité
# fichier_mots = 'https://math.univ-angers.fr/~jaclin//site2023/lzNxo3B9R_ds2/concurrence/2023/multiprocessing/_attachments/gutenberg.txt'

fichier_mots = 'gutenberg.txt'
fichier_mots = 'words'
fichier_mots = '/usr/share/dict/words'


############ Dossier et fichiers sortie ############

dossier_sortie = "./resulats/"
fichier_sortie = f'bilan_q2_b_{fichier_mots}.txt'
fichier_sortie2 = f'bilan__q2_b_liste_de_tous_les_anagrammes_{fichier_mots}.txt'


############ Mode debug (pour limiter le nb de mots) ############

debug = False


############ Affichage de l'histogramme des mots ############

display_graph = True