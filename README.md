# Python - Mini programme de détection d'intrusion 

Ce programme vise à exécuter un mini Système de Détection d'Intrusion (IDS) sur votre machine pour vous alerter en cas de détection d'une anomalie. En cas d'attaque, il est capable de la bloquer.

# Compatibilité  et capacité de l'IDS

Ce programme est conçu spécifiquement pour les environnements Linux et ne requiert aucune bibliothèque Python supplémentaire.
Celui-ci permet de : 

  * Fournir des informations sur le système (version etc)
  * Detecter création d'un nouvel utilisateur / groupe 
  * Detecter l'ajout d'un utilisateur dans un groupe
  * Detecter le changement de mot de passe d'un utilisateur
  * Detecter les nouvelles connexions d'un utilisateur
  * Detecter l'ajout d'une nouvelle clé SSH
  * Detecter les nouvelles connexions SSH
  * Detecter des connexions SSH depuis une IP blacklisté
  * Detecter du brute force SSH
  * Detecter l'ouverture d'un nouveau port en écoute

Lorsque vous exécutez le script, un fichier "logs.txt" est généré dans votre répertoire actuel. À chaque fois qu'un événement de détection est déclenché, une entrée de journal est écrite dans ce fichier. Cette entrée de journal contient des informations sur l'élément déclencheur ainsi que la date et l'heure précises de l'événement.

Pour détecter les événements liés à SSH, le service SSH doit être installé et en cours d'exécution sur votre système.

# Installation et éxecution du programme 
<br>

> [!CAUTION]
> Ce programme doit être executer avec des droits root. En effet, le programme va interroger (en lecture seul) le fichier /shadow de votre système pour savoir par exemple si le mot de passe d'un utilisateur a été changé. 

<br>

**Prérequis**

  * Python 3.6 ou supérieur
  * OS : Linux
  * Service SSH de lancé
  * Execution du script en root
  * Présence d'un fichier logs.txt dans le repertoire courant
  * Présence d'un fichier blacklist.txt dans le repertoire courant contenant les IP blacklisté

<br>

**Installation et Execution**

Pour linux  uniquement : 

1. Cloner le repository :
   
    `git clone https://github.com/MBAY-Clement/IDS-PYTHON.git`

3. Acceder au repertoire :

   `cd IDS`

4. Lancer le fichier "main.py" avec des droits root

   `sudo python3 main.py`

6. Pour stopper le programme depuis un terminal :

     `CTRL + C`


# Explications des détections

Vous retrouvez ci-dessous le détails des détections proposé par le programme. Pour rappel le resultat de chaque fonction est affiché dans le terminal mais égalemen dans le fichier log.txt.
>
> **De plus lorsqu'une fonction est déclanché il est clairement écrit dans le fichier log à quelle heure celle-ci s'est déclanchée** : 


1. Information sur l'OS
   * Explication : Cette fonction permet de detecter sur quel système d'exploitation ainsi que sa version est lancé le script
   * Résultat écrit sur le fichier de log : Système d'exploitation détecté : Linux Version : XXX
<br>

2. Détection d'un nouvel utilisateur / groupe sur la machine
   * Explication : Lors de la détection de la création d'un nouvel utilisateur ou groupe sur la machine cela est noté dans le fichier logs.txt
   * Résultat écrit sur le fichier de log : Nouveau groupe créé : tata:x:1005: (nom du groupe / ID du groupe) ; Nouvel utilisateur créé : tata:1005 (nom de l'utilisateur / ID de l'user)
<br>

3. Détection de l'ajout d'un utilisateur dans un groupe
   * Explication : Lors de la détection de l'ajout d'un utilisateur dans un groupe sur la machine cela est noté dans le fichier logs.txt
   * Résultat écrit sur le fichier de log : Utilisateur ajouté au groupe (nom du groupe) : (nom de l'user)
<br>

4. Détection du changement de mot de passe d'un utilisateur
   * Explication : Lorsqu'un utilisateur change son mot de passe, cela est tracé dans le fichier de log et affiche le hash de l'ancien mot de passe puis du nouveau mot de passe
   * Résultat écrit sur le fichier de log : Mot de passe utilisateur changé : <nom de l'user> <ancien hash (mot de passe) <nouveau hash (nouveau mot de passe>

5. Détection de la connexion d'un nouvel utilisateur
   * Explication : Dès qu'un nouvel utilisateur est conencté sur la machine alors cela est détecté et tracé par le script
   * Résultat écrit sur le fichier de log : Nouvel utilisateur connecté : (nom du user)
<br>

6. Détection d'une nouvelle clé SSH
   * Explication : Dès qu'une nouvelle clé SSH est détecté pour un user (même le compte root) cela est détecté et tracé dans le fichier log.
   * Résultat écrit sur le fichier de log : Nouvelle clé SSH détectée pour l'utilisateur : (nom du user)
<br>

7. Detecter une nouvelle conenxion SSH et détecter si cette conenxion provient d'une IP blacklisté
   * Explication : Cette fonction permet de détecter et de tracer udès qu'une conenxion SSH entrante sur votre post est détecte et également vous prevenir si cette connexion vient d'une adresse IP blacklisté (IP dans le fichier blacklist.txt)
   * Résultat écrit sur le fichier de log : Nouvelle connexion SSH détectée test en cours de l'adrese IP ! -> Si IP blacklisté : Connexion SSH détectée avec une adresse IP blacklisté : (adresse ip) -> Si IP non blacklisté : Nouvelle connexion SSH détectée pour le user (nom du user) Adresse IP de la connexion SSH : (IP de connexion).
<br>

8. Détection d'un brute force SSH
   * Explication : Si le nombre de connexion SSH réfusée dans un laps de temps est supérieur à 3 alors un brute force SSH est détecté
   * Résultat écrit sur le fichier de log : Tentative de connexion brute force SSH détectée !
<br>

9. Détection d'un nouveau port en écoute
    * Explication : Dès qu'un nouveau port en écoute est détecté sur la machine alors celui-ci est tracé. Si un port précedemment en écoute se clos alors cela est également tracé
    * Résultat écrit sur le fichier de log : Si port fermé : Port fermé détecté ! ; Si nouveau port en écoute détecté : Nouveau port ouvert en écoute détecté ! Port ouvert en écoute : (affiche le nouveau port ouvert)
<br>

**Exemple**

Vous retrouvez-ci dessous une video démonstrative lorsque le programme est execute / détecte quelque chose : 




https://github.com/MBAY-Clement/IDS-PYTHON/assets/59869618/95c30e21-f5db-498a-8251-105062b58412

(PS : Le compte tata a été supprimé de la machine. ;) )


   
#  Futur axes d'amélioration 

* Gestion de la performance et de la consommation de ressources : Actuellement, dès que le programme est lancé, il se montre très gourmand et consomme énormément de CPU / RAM, ce qui peut ralentir la machine. Il est  alors nécessaire de prévoir des axes d'amélioration afin qu'une fois le programme exécuté, celui-ci soit le plus transparent possible pour l'utilisateur.

* Envoi du rapport de logs par mail de manière journalière : Un axe intéressant serait l'envoi quotidien du rapport de logs par mail à l'utilisateur de la machine. Même s'il se trouve à distance, il pourra ainsi avoir un œil sur ce qu'il se passe sur sa machine.

* Integration d'un Webhooks discord. Grâce à ce Webhook dès qu'une fonction de détection est trigger, alors un message (comprenant les informations) est envoyé sur le discord de l'utilisateur pour l'informer. 





