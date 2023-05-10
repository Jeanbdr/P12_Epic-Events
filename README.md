# EPIC EVENTS 

## Description 

Le projet 12 de la formation "DA Python" d'Openclassrooms a pour but de réaliser un crm avec une partie utilisant une API rest et le site admin Django pour la société Epic Events

Cette API doit permettre à un utilisateur (sous couvert d'autorisations nécessaires) de créer et modifier des clients, contrats et événements.

## Fonctionnalitées :

    - Se connecter 
    - Consulter, créer et modifier des clients, contrats et événements (selon le degrés d'autorisation)

## Mise en place du projet : 

    !! Une application type Postman ainsi que l'application PostgreSQL sont nécessaire pour ce projet !!

    - Télécharger le projet (bouton code et download ZIP)
    - Déplacer vous vers le projet à l'aide de la console de votre ordinateur
    - Créer un environnement virtuel : 
        
        python -m venv env

    - Activer l'environnement virtuel :

        macOS et linux : env/bin/activate
        Windows : env\Scripts\activate

    - Installer les packages nécessaires :

        pip install -r requirements.txt

    - Déaplcer vous dans le dossier epicevents :

        cd epicevents

    - Réaliser les migrations :

        python manage.py migrate

    - Créer un superuser afin d'accéder au site admin :

        python manage.py createsuperuser
    
    - Lancer le serveur depuis la console :

        python manage.py runserver

    - Une documentation Postman vous permettra ensuite d'utiliser correctement l'application.



