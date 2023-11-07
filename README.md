# Description du projet

Ce projet est une application basée sur une architecture mixte (GRPC et GraphQL) de microservices. Le schéma suivant indique les type d'architectuce entre les différentes architectures. 
![Alt text](sch%C3%A9ma.png)
Dans le cadre de ce TP, nous nous sommes concentrés sur les 3 microservices "user", "booking" et "showtime" et on s'est limité au TP vert. Le repository contient des fichiers .py correspondant à chaque microservice.
L'Open Api correspondante à chaque microservice résume les différentes requêtes que l'on peut utiliser pour interroger celui-ci ainsi que les endpoints associés.


## Microservice "Movie"

Le microservice "movie" a été largement implémenté en suivant le tutoriel. Il gère les fonctionnalités liées aux films, telles que l'ajout d'un film, la modification de sa note, la suppression et la récupération d'informations sur les films. 

## Microservice "Booking"

Au sein du microservice "booking", nous avons implémenté des fonctionnalités de réservation des films. Les requêtes GET permettent d'avoir des informations sur toutes les réservations, ou celles correspondantes à un utilisateur particulier. Tandis que les requêtes POST permettent d'apporter des modification sur la base de données des réservations, comme l'ajout d'une réservation pour un utilisateur donné.

## Microservice "Showtime"

Dans ce microservice, il n'y a que des requêtes GET qui ont été implémentées. Une pour récupérer tous les films programmés et une autres pour récupérer ceux programmés à une date donnée

## Microservice "User"

C'est le microservice principal qui fait appel à quasiment tous les fonctions implémentés dans les autres microservices. 

## Comment utiliser ce repository via Docker-Compose

Pour utiliser ce repository et explorer les fonctionnalités des différents microservices, suivez ces étapes :

1. Clonez le repository sur votre machine locale.
2. Lancez la commande "sudo docker-compose up --build" dans un terminal (sur linux) 
3. Testez les fonctionnalités des microservices à l'aide des requêtes HTTP appropriées (GET, POST, PUT, DELETE, etc.) en se référant à l'OpenAPI de chaque microservice.


## Auteurs

- JEBARI Aymane
- YAHYAOUI Firas
