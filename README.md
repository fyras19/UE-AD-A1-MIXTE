# Description du projet

Ce projet est une application basée sur une architecture mixte (GRPC et GraphQL) de microservices. Le schéma suivant indique les types d'architecture considérés entre les différents microservices. 
![Alt text](sch%C3%A9ma.png)
Dans le cadre de ce TP, nous nous sommes concentrés sur les 3 microservices "user", "booking" et "showtime" et on s'est limité au TP vert. Le repository contient des fichiers .py correspondant à chaque microservice.
Nous avons repris les mêmes endpoints du microservice "user" du TP REST en changeant après avoir transformé l'architecture des microservices "Movie", "Showtime" et "Booking" à l'architecture indiquée sur le schéma précédent. 

## Microservice "Movie"

Le microservice "movie" a été largement implémenté en suivant le tutoriel. Il gère les fonctionnalités liées aux films, telles que l'ajout d'un film, la modification de sa note, la suppression et la récupération d'informations sur les films. L'interaction directe avec ce microservice peut se faire via "http://localhost:3001/graphql".

## Microservice "Booking"

 Dans le cadre de l'architecture gRPC, ce mivroservice est à la fois un client pour le microservice "Showtime" et un serveur pour le microservice "User". Au sein du microservice "booking", nous avons implémenté des fonctionnalités de réservation des films. Les requêtes GET permettent d'avoir des informations sur toutes les réservations, ou celles correspondantes à un utilisateur particulier. Tandis que les requêtes POST permettent d'apporter des modifications sur la base de données des réservations, comme l'ajout d'une réservation pour un utilisateur donné.

## Microservice "Showtime"

Dans ce microservice, il n'y a que des requêtes GET qui ont été implémentées. Une pour récupérer tous les films programmés et une autres pour récupérer ceux programmés à une date donnée

## Microservice "User"

C'est le microservice principal qui fait appel à quasiment tous les fonctions implémentés dans les autres microservices. 

## Comment utiliser ce repository via Docker-Compose

Pour utiliser ce repository et explorer les fonctionnalités des différents microservices, suivez ces étapes :

1. Clonez le repository sur votre machine locale.
2. Lancez la commande "docker-compose up --build" dans un terminal
3. Testez les fonctionnalités des microservices à l'aide des requêtes HTTP appropriées (GET, POST, PUT, DELETE, etc.) indiqués dans le fichier user.py. Vous pouvez également tester directement les autres microservices (par exemple via une query GraphQL pour le microservice "movie").


## Auteurs

- JEBARI Aymane
- YAHYAOUI Firas
