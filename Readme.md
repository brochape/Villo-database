# Villo database
## Projet pour le cours de base de données ULB 2014-2015
## Bruno Rocha Pereira et Antoine Carpentier

### Requirements

* python2
* virtualenv2
* pip2

### Installation

Tip : remplacer python2/virtualenv2/pip2 dans les commandes qui suivent par l'équivalent pour Python 2 sur votre système

1. Créer un virtualenv à la racine du projet : 
    `virtualenv2 .`

2. Activer le virtualenv :
    `source bin/activate`

3. Installer les dépendances : 
    `pip2 install -r requirements`

### Lancement

1. Se déplacer dans le dossier source : 
    `cd src`

2. Créer la database : 
    `make database`

3. Lancer l'application : 
    `make`

4. L'application est accessible sur un navigateur web à l'addresse `http://localhost:5000`