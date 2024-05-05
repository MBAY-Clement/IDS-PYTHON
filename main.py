########################################
##########  Projet Python - IDS ########
########################################

# lancement du programme : python3 main.py
# Pour arrêter le programme : Ctrl+C
# Pour voir les logs : cat logs.txt
# Pour voir les adresses IP blacklistées : cat blacklist.txt 
# Pour rajouter une adresse IP à la blacklist : echo "adresse_ip" >> blacklist.txt

import os
import platform
import threading
import signal
import time

# Fonction de détection de l'OS
def detect_os_version():
    # Détecte l'OS et sa version
    system_info = platform.uname()
    os_name = system_info.system
    os_version = system_info.release
    return os_name, os_version

# Fonction pour surveiller la création d'un nouveau utilisateur
def watch_user_creation_linux():
    # Compte le nombre d'utilisateurs dans /etc/passwd
    last_user_count = len(open('/etc/passwd').readlines())
    while not exit_flag[0]:
        current_user_count = len(open('/etc/passwd').readlines())
        if current_user_count > last_user_count:
            print("New user detected !") 
            # Obtenir le dernier utilisateur ajouté
            new_user_info = os.popen("tail -n 1 /etc/passwd | cut -d: -f1,3").read().strip()
            # Variable avec la date et l'heure
            date = os.popen("date").read()
            # Écrire dans le fichier logs.txt la création de l'utilisateur et la date de création
            with open("logs.txt", "a") as f:
                # Affiche le nom et l'UID de l'utilisateur
                f.write("Nouvel utilisateur créé : " + new_user_info + "\n")
                f.write("Date de création de l'utilisateur : " + date + "\n")
                f.write("\n")
            last_user_count = current_user_count

# Fonction détection d'un nouveau groupe
def watch_group_creation_linux():
    #Compte le nombre de groupes dans /etc/group
    last_group_count = len(open('/etc/group').readlines())
    while not exit_flag[0]:
        current_group_count = len(open('/etc/group').readlines())
        if current_group_count > last_group_count:
            print("New group detected !")
            #Variable avec la date et l'heure
            date = os.popen("date").read()
                #Écrire dans le fichier logs.txt la création du groupe et la date de création
            with open("logs.txt", "a") as f:
                f.write("Nouveau groupe créé : " + os.popen("tail -n 1 /etc/group").read())
                f.write("Date de création du groupe : " + date + "\n")
                f.write("\n")
            last_group_count = current_group_count


# Fonction détection d'un utilisateur ajouté à un groupe
def lire_fichier_groupes():
    # Chemin vers le fichier /etc/group
    chemin_fichier = "/etc/group"
    
    #dictionnaire pour stocker les groupes et les utilisateurs correspondants
    groupes_utilisateurs = {}
    
    # Ouvre le fichier en mode lecture
    with open(chemin_fichier, 'r') as fichier:
        # Itère à travers chaque ligne du fichier
        for ligne in fichier:
            # Sépare la ligne en nom de groupe et utilisateurs
            elements = ligne.strip().split(':')
            # Vérifie s'il y a au moins trois éléments dans la ligne
            if len(elements) >= 3:
                groupe = elements[0]
                utilisateurs = elements[3].split(',') if len(elements) >= 4 else []
                # Ajoute le groupe et les utilisateurs au dictionnaire
                groupes_utilisateurs[groupe] = utilisateurs

    return groupes_utilisateurs


# Fonction pour surveiller l'ajout d'un utilisateur à un groupe
def surveiller_ajout_utilisateur_groupes():
    # Stocke les groupes et les utilisateurs actuels
    groupes_actuels = lire_fichier_groupes()
    
    while not exit_flag[0]:
        # Attend quelques secondes avant de vérifier à nouveau
        #time.sleep(5)
        
        # Obtient les groupes et les utilisateurs actuels
        nouveaux_groupes = lire_fichier_groupes()
        
        # Compare les groupes actuels avec les nouveaux groupes
        for groupe, utilisateurs in nouveaux_groupes.items():
            if groupe in groupes_actuels:
                # Vérifie les nouveaux utilisateurs ajoutés au groupe
                nouveaux_utilisateurs = set(utilisateurs) - set(groupes_actuels[groupe])
                if nouveaux_utilisateurs:
                    #ajouter un texte dans le fichier logs.txt avec l'heure 
                    with open("logs.txt", "a") as f:
                        f.write("Utilisateur ajouté au groupe " + groupe + " : " + ', '.join(nouveaux_utilisateurs) + "\n")
                        f.write("\n")
                    print(f"L'utilisateur {', '.join(nouveaux_utilisateurs)} a été ajouté au groupe {groupe}.")
        # Met à jour les groupes actuels
        groupes_actuels = nouveaux_groupes
    


# Detection changement mot de passe utilisateur avec diff 
def watch_password_change_linux():
    #recopie le fichier /etc/shadow
    os.system("cp /etc/shadow /tmp/shadow")
    while not exit_flag[0]:
        # Compare les fichiers /etc/shadow et /tmp/shadow
        diff = os.popen("diff /etc/shadow /tmp/shadow").read()
        if diff:
            # Ajoute un texte dans le fichier logs.txt avec l'heure
            #affiche le nom de l'utilisateur et le mot de passe 
            with open("logs.txt", "a") as f:
                f.write("Mot de passe utilisateur changé : \n" + diff + "\n")
                f.write("Date de changement du mot de passe : " + os.popen("date").read() + "\n")
                f.write("\n")
            print("Mot de passe utilisateur changé : \n", diff)
            # Recopie le fichier /etc/shadow
            os.system("cp /etc/shadow /tmp/shadow")


# Dectection connexion d'un nouvel utilisateur 
def watch_user_login_linux():
    # Compte le nombre d'utilisateurs connectés
    last_user_count = len(os.popen("who").readlines())
    while not exit_flag[0]:
        current_user_count = len(os.popen("who").readlines())
        
        if current_user_count > last_user_count:
            print("New user logged in !")
            # Obtenir le dernier utilisateur connecté
            new_user_info = os.popen("who | tail -n 1").read().strip()
            # Variable avec la date et l'heure
            date = os.popen("date").read()
            # Écrire dans le fichier logs.txt la connexion de l'utilisateur et la date de connexion
            with open("logs.txt", "a") as f:
                # Affiche le uniquement le nom de l'utilisateur
                f.write("Nouvel utilisateur connecté : " + new_user_info.split()[0] + "\n")
                f.write("Date de connexion de l'utilisateur : " + date + "\n")
                f.write("\n")
            print("Nouvel utilisateur connecté : " + new_user_info.split()[0] + "\n")
            last_user_count = current_user_count
        #Si un utilisateur se déconnect on met alors à jour le nombre d'utilisateur connecté
        else:
            last_user_count = current_user_count

#Detecter une nouvelle clé  SSH en regardant si le hash du fichier .ssh/authorized_keys de tous les utilisateurs a changé
def watch_ssh_key_linux():
    # trouver tous les utilisateurs du système grâce à /home 
    utilisateurs = os.listdir("/home")
    #print(utilisateurs)
    #recuperer le hash de tous les fichiers .ssh/authorized_keys de tous les utilisateurs
    hash_fichier = {}
    for utilisateur in utilisateurs:
        #chemin vers le fichier .ssh/authorized_keys
        chemin_fichier = "/home/" + utilisateur + "/.ssh/authorized_keys"
        #print(chemin_fichier)
        #si le fichier n'est pas présent alors on passe à l'utilisateur suivant on trouve le hash via la commande md5sum
        if not os.path.exists(chemin_fichier):
            continue
        else:
            #recuperer le hash du fichier .ssh/authorized_keys
            hash_fichier = os.popen("md5sum " + chemin_fichier).read().split()[0]
        
        # Chemin vers le fichier .ssh/authorized_keys pour l'utilisateur root
            chemin_fichier_root = "/root/.ssh/authorized_keys"
            # Si le fichier est présent, récupérer son hash
            if os.path.exists(chemin_fichier_root):
                hash_fichier_root = os.popen("md5sum " + chemin_fichier_root).read().split()[0]
            else:
                hash_fichier_root = None
                print("Le fichier de l'utilisateur root n'existe pas")

    #print(hash_fichier)    
    while not exit_flag[0]:
        #si le hash du fichier .ssh/authorized_keys de tous les utilisateurs a changé alors on affiche un message
        for utilisateur in utilisateurs:
            chemin_fichier = "/home/" + utilisateur + "/.ssh/authorized_keys"
            #si le fichier n'est pas présent alors on passe à l'utilisateur suivant
            if not os.path.exists(chemin_fichier):
                continue
            else:
                #recuperer le hash du fichier .ssh/authorized_keys
                hash_fichier_actuel = os.popen("md5sum " + chemin_fichier).read().split()[0]
                #si le hash du fichier .ssh/authorized_keys de l'utilisateur a changé alors on affiche un message
                if hash_fichier_actuel != hash_fichier:
                    print("Nouvelle clé SSH détectée pour l'utilisateur : " + utilisateur)
                    #ajouter un texte dans le fichier logs.txt avec l'heure 
                    with open("logs.txt", "a") as f:
                        f.write("Nouvelle clé SSH détectée pour l'utilisateur : " + utilisateur + "\n")
                        f.write("Date de création de la clé SSH : " + os.popen("date").read() + "\n")
                        f.write("\n")
                    #mettre à jour le hash du fichier .ssh/authorized_keys
                    hash_fichier = hash_fichier_actuel


                if os.path.exists(chemin_fichier_root):
                    hash_fichier_actuel_root = os.popen("md5sum " + chemin_fichier_root).read().split()[0]
                    if hash_fichier_actuel_root != hash_fichier_root:
                        print("Nouvelle clé SSH détectée pour l'utilisateur root")
                        with open("logs.txt", "a") as f:
                            f.write("Nouvelle clé SSH détectée pour l'utilisateur root\n")
                            f.write("Date de création de la clé SSH : " + os.popen("date").read() + "\n")
                            f.write("\n")
                        hash_fichier_root = hash_fichier_actuel_root

# Fonction pour detecter l'ouverture d'une session ssh et si connexion ssh via ip blacklisté depuis blacklist.txt
def watch_ssh_login_linux():
    #taper la commande journalctl -u ssh.service et regarder si il y a des nouvelles connexions
    while not exit_flag[0]:
        #recuperer les nouvelles connexions ssh
        ssh_log_old = os.popen("journalctl -u ssh.service | grep 'session opened'").read()
        # compter le nombre de ligne du journal
        nb_ligne = len(ssh_log_old.splitlines())
        #print(nb_ligne)
    #regarder a chaque seconde si il y a des nouvelles connexions
        time.sleep(1)
        ssh_log_new = os.popen("journalctl -u ssh.service | grep 'session opened'").read()
        #compter le nombre de ligne du journal
        nb_ligne_new = len(ssh_log_new.splitlines())
        #si le nombre de ligne a changé alors il y a une nouvelle connexion
        if nb_ligne_new > nb_ligne:
            print("Nouvelle connexion SSH détectée test en cours de l'adrese IP !")
            #ajouter un texte dans le fichier logs.txt l'info de connexion avec l'heure et le nom de l'utilisateur
            user_information = os.popen("journalctl -u ssh.service | grep 'session opened'  | tail -n 1").read()
            ip_information = os.popen("journalctl -u ssh.service | grep 'Accepted password for'  | tail -n 2").read()

            if ip_information.split()[10] in open("blacklist.txt").read():
                print("Connexion SSH détectée avec une adresse IP blacklisté : " + ip_information.split()[10])
                #ajouter un texte dans le fichier logs.txt avec l'heure 
                with open("logs.txt", "a") as f:
                    f.write("Connexion SSH détectée avec une adresse IP blacklisté : " + ip_information.split()[10] + "\n")
                    f.write("Date de connexion de la conenxion SSH malveillante : " + os.popen("date").read() + "\n")
                    f.write("\n")
                continue
            else :
                print("Connexion autorisée pour l'adresse IP : " + ip_information.split()[10])
                #ajouter un texte dans le fichier logs.txt avec l'heure
                with open("logs.txt", "a") as f:
                    f.write("Nouvelle connexion SSH détectée pour le user : " + user_information.split()[10] + "\n")
                    f.write("Adresse IP de la connexion SSH : " + ip_information.split()[10] + "\n")
                    f.write("Date de connexion de la conenxion SSH : " + os.popen("date").read() + "\n")
                    f.write("\n")
            #mettre à jour le nombre de ligne
            nb_ligne = nb_ligne_new

# Fonction détection de brute force SSH
def watch_ssh_bruteforce_linux():

    count_bruteforce = 0
    nb_ligne_old = 0
    old_ssh_success_count = 0

    while not exit_flag[0]:
        #recuperer les nouvelles connexions ssh
        ssh_log_old = os.popen("journalctl -u ssh.service | grep 'Failed password'").read()
        # compter le nombre de ligne du journal
        nb_ligne = len(ssh_log_old.splitlines())

        # SSH succes 
        ssh_success = os.popen("journalctl -u ssh.service | grep 'session opened'").read()
        ssh_success_count = len(ssh_success.splitlines())
        #print(ssh_success_count)

        #print("Le compteur detection SSH bruteforce est à : " + str(count_bruteforce))

        #Si nombre de ligne = nombre de ligne + 1 alors on incrémente le compteur
        if nb_ligne > nb_ligne_old:
            count_bruteforce = count_bruteforce + 1
            #Par default au lancement du programme le nombre de ligne est à 0 donc on affiche pas le message
            #print("Connexion SSH échouée détectée le compteur detection SSH bruteforce est à : " + str(count_bruteforce))
        else :
            #si le nombre de ligne augmente alors on remet le compteur à zero
            if ssh_success_count > old_ssh_success_count:
                count_bruteforce = 0
                print("Connexion SSH réussie détectée le compteur detection SSH bruteforce est à : " + str(count_bruteforce))
            
        #si le compteur est égale à 3 alors on affiche un message
        if count_bruteforce == 3:
            print("Tentative de connexion brute force SSH détectée !")
            #ajouter un texte dans le fichier logs.txt avec l'heure 
            with open("logs.txt", "a") as f:
                f.write("Tentative de connexion brute force SSH détectée !\n")
                f.write("Date de la tentative de connexion brute force SSH : " + os.popen("date").read() + "\n")
                f.write("\n")
            count_bruteforce = 0
        #mettre à jour le nombre de ligne
        nb_ligne_old = nb_ligne
        old_ssh_success_count = ssh_success_count


#Fonction pour détecter un nouvel port ouvert en écoute sur la machine
def watch_new_open_port_linux():
    #recupérer les ports ouverts en écoute
    ports_old = os.popen("netstat -tuln > /tmp/ports_old")
    with open("/tmp/ports_old", "r") as f:
    # Compte le nombre de lignes dans le fichier
        count_line = len(f.readlines())
    

    while not exit_flag[0]:
        #recupérer les ports ouverts en écoute et les écrire dans un fichier temporaire
        os.system("netstat -tuln > /tmp/ports")
        #comparer les ports ouverts en écoute
        ports_new = os.popen("netstat -tuln > /tmp/ports_new")
        #ajouter un délai de 5 secondes pour laisser le temps de lancer la commande netstat -tuln
        time.sleep(1)
        with open("/tmp/ports_new", "r") as f:
            # Compte le nombre de lignes dans le fichier
            count_line_new = len(f.readlines())
        #print(count_line_new)
        #print("COmpteur a execution du script : " + str(count_line))
        #print ("compteur apres execution du script : " + str(count_line_new))

        #si le nombre de ligne de count_line_new est inférieur à count_line alors un port a été fermé 
        if count_line_new < count_line:
            print("Port fermé détecté !")
            #ajouter un texte dans le fichier logs.txt avec l'heure 
            with open("logs.txt", "a") as f:
                f.write("Port fermé détecté !\n")
                f.write("Date de fermeture du port : " + os.popen("date").read() + "\n")
                f.write("\n")
            #copier le fichier ports_new dans ports_old
            os.system("cp /tmp/ports_new /tmp/ports_old")
            #mettre à jour le nombre de ligne
            count_line = count_line_new

        #comparer les fichiers ports_old et ports_new
        diff = os.popen("diff /tmp/ports /tmp/ports_old").read()
        #print(diff)
        #si il y a une différence alors on affiche un message
        if diff:
            print("Nouveau port ouvert en écoute détecté !")
            #afficher le uniquement le nouveau port ouvert en écoute 
            diff = os.popen("diff /tmp/ports_old /tmp/ports | grep '>'").read()
            print(diff)

            #ajouter un texte dans le fichier logs.txt avec l'heure 
            with open("logs.txt", "a") as f:
                f.write("Nouveau port ouvert en écoute détecté !\n")
                f.write("Port ouvert en écoute :\n ")
                f.write(diff)
                f.write("Date de l'ouverture du port : " + os.popen("date").read() + "\n")
                f.write("\n")
            #copier le fichier ports_new dans ports_old
            os.system("cp /tmp/ports_new /tmp/ports_old")
            #mettre à jour le nombre de ligne
            count_line = count_line_new
            


# Fonction pour gérer le signal SIGINT (Ctrl+C) et arrêter le programme
def signal_handler(sig, frame):
    print("Exiting...")
    exit_flag[0] = True
    # Ajouter une déclaration de débogage pour voir si la fonction est déclenchée
    print("(Ctrl+C) détecté fin du programme" )


#########################################
########## Fonction principale ##########
#########################################

def main():
    global exit_flag
    exit_flag = [False]

    os_name, os_version = detect_os_version()
    print("Système d'exploitation détecté :", os_name)
    print("Version :", os_version)

    # Écrire l'OS dans le fichier logs.txt
    with open("logs.txt", "a") as f:
        # Écrire à quelle heure le programme a été lancé
        f.write("###############################################\n")
        f.write("Heure de lancement du programme : " + str(os.popen("date").read()) + "\n")
        f.write("Système d'exploitation détecté : " + os_name + "\n")
        f.write("Version : " + os_version + "\n")
        f.write("\n")

    # Créer deux threads pour exécuter les fonctions en parallèle
    thread_user = threading.Thread(target=watch_user_creation_linux)
    thread_group_creation = threading.Thread(target=watch_group_creation_linux)
    thread_group = threading.Thread(target=surveiller_ajout_utilisateur_groupes)
    thread_password = threading.Thread(target=watch_password_change_linux)
    thread_user_login = threading.Thread(target=watch_user_login_linux)
    thread_ssh_key = threading.Thread(target=watch_ssh_key_linux)
    thread_ssh_login = threading.Thread(target=watch_ssh_login_linux)
    thread_ssh_bruteforce = threading.Thread(target=watch_ssh_bruteforce_linux)
    thread_new_open_port = threading.Thread(target=watch_new_open_port_linux)


    # Démarrer les threads
    thread_user.start()
    thread_group_creation.start()
    thread_group.start()
    thread_password.start()
    thread_user_login.start()
    thread_ssh_key.start()
    thread_ssh_login.start()
    thread_ssh_bruteforce.start()
    thread_new_open_port.start()

    # Ajouter un gestionnaire de signal pour capturer Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Attendre que les threads se terminent
    thread_user.join()
    thread_group_creation.join()
    thread_group.join()
    thread_password.join()
    thread_user_login.join()
    thread_ssh_key.join()
    thread_ssh_login.join()
    thread_ssh_bruteforce.join()
    thread_new_open_port.join()

    # Écrire à quelle heure le programme s'est terminé
    with open("logs.txt", "a") as f:
        f.write("Heure de fin du programme : " + str(os.popen("date").read()) + "\n")
        f.write("###############################################\n")
    
    #supprimer le fichier /tmp/shadow utile pour la detection du changement de mot de passe fonction watch_password_change_linux()
    os.system("rm /tmp/shadow")
    #supprimer le fichier /tmp/ports_old utile pour la detection de l'ouverture d'un nouveau port fonction watch_new_open_port_linux()
    os.system("rm /tmp/ports_old")
    #supprimer le fichier /tmp/ports utile pour la detection de l'ouverture d'un nouveau port fonction watch_new_open_port_linux()
    os.system("rm /tmp/ports_new")


# Appeler la fonction principale si le script est exécuté
if __name__ == "__main__":
    main()

# Fin du programme