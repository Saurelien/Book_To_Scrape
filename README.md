#################################################
####### descritpion projet Book To Scrape #######
#################################################


# J'ai été affecté par mon Lead Dev Sam afin de produire une version beta d'un programme pour suivre les prix des livres sur demande auprès de Books To Scrape. Les données récupéré sont stockée dans plusieurs fichiers au format csv par catégorie.


########################################################
############## Virtual Env & dependancies ##############
########################################################


# Les packages nécéssaires ce trouvent dans le requirements.txt
* Requests
* BeautyfulSoup
* CSV


# Installation de l'environnement virtuel sous windows
* Un environement est dans la bonne pratique nommé " env " mais il peut aussi porter le nom du projet qu'il va contenir.
* Initiez la commande
* python -m venv <environment name> " <environement name> est le nom de l'environement virtuel qui contiendra le projet "
* Pour activer l'environnement virtuel :
* source <env name>/bin/activate
* Sous windows <env name>/Scripts/activate.bat


########################################################
##################    Utilisation    ###################
########################################################

# Le programme est contenu dans un seul fichier " main.py "
* Dans l'interpreteur python tapez : main.py pour lancer le programme.
* Executez ce fichier produira les fichiers csv demandé.