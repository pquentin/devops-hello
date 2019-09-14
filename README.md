# Séminaire DevOps - Epitech Saint-André

DevOps, qu'est-ce que c'est ? Revenons un peu dans le temps.
Historiquement, les développeurs et les administrateurs systèmes
étaient isolés, chacun dans leur coin. Les développeurs voulaient...
développer, faire évoluer leur site web le plus vite possible. Les
administrateurs, eux, voulaient que le site soit stable. Il y a une
tension inhérente entre les deux approches. Les pratiques DevOps
cherchent à les réconcilier en rendant les développeurs responsable de
leurs sites webs et applications et en faisant adopter des méthodes
développement aux administrateurs systèmes.

Comme vous êtes des développeurs, je vais vous montrer comment gérer
un site web comme si vous étiez un développeur dans une équipe
adepte des pratiques DevOps.

Nous allons partir sur un exemple concret, une application Flask qui
va servir à introduire les concepts que j'ai jugé les plus importants
dans une introduction, parce qu'utiles au jour le jour.

Cette application Flask sera la plus basique possible : elle
n'affichera qu'un simple message dans votre navigateur. Ce qui va nous
intéresser ici, c'est tout le reste :

 * l'empaquetage de l'application dans Docker
 * l'intégration continue pour tester l'application
 * le déploiement dans Kubernetes
 * la surveillance de l'application
 * la haute disponiblité, et les mises à jour de cette application

## Pré-requis

J'ai choisi d'utiliser GitHub pour stocker le code source, Circle CI
pour l'intégration continue, et Google Cloud Platform pour le
déploiement dans Kubernetes. Rien n'oblige à utiliser ces services là
en particulier, et ils ont tous des concurrents tout aussi
performants, mais j'ai préféré utiliser des outils que je connais déjà
pour pouvoir vous aider au mieux si vous rencontrez un problème.

Du coup, il faut un compte GitHub, pour vous donner accès à ce projet,
et un compte Google pour vous donner accès au projet Google Cloud
Platform que j'ai créé pour ce séminaire. Merci de me les envoyer par
mail. Différents outils sont indispensables aujourd'hui : Docker, git
et le SDK Google Cloud. Nous les installerons le moment opportun.

## Modification de l'application Flask Hello et test local

Chacun d'entre vous va déployer sa propre application, et ça commence
par envoyer votre version sur GitHub. Il faut installer et configurer
git sur votre machine :

```
$ sudo dnf -y update
$ sudo dnf -y install git
$ git config --global user.name "sampleuser"
$ git config --global user.email "sampleuser@example.com"
```

À partir de là, vous allez pouvoir cloner ce dépôt :

```
$ git clone https://github.com/pquentin/devops-hello.git
```

Ensuite, modifiez "hello.py" pour retourner un autre message que
"Hello, World !" dans la fonction index().

Est-ce que ça a fonctionné ? Essayons en local. Il vous faut d'abord
installer pipenv, les dépendances de notre projet, lancer les tests,
et enfin lancer le serveur de test :

```
$ dnf install pipenv
$ pipenv install
$ pipenv run pytest hello.py
$ FLASK_APP=hello.py pipenv run flask run
```

Puis voir le résultat dans votre navigateur :
[http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Test dans Docker en local

Pour déployer notre application, nous allons utiliser une image
Docker, qui va contenir à elle seule un système d'exploitation,
Python, notre application et ses dépendances. Le grand avantage de
Docker ici est que le fonctionnement sera exactement le même chez vous
et dans le cloud Google.

Pour installer Docker, les [instruction pour
Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)
indiquent qu'il faut lancer ces commandes :

```
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo 
$ sudo dnf install docker-ce docker-ce-cli containerd.io
$ sudo systemctl start docker
```

Puis vérifier que l'installation a fonctionné :

```
$ sudo docker run hello-world
```

Nous pouvons ensuite construire notre image :

```
$ docker build -t hello .
```

Cette commande `docker build` exécute en fait les instructions
présentes dans le fichier Dockerfile. Apprendre à écrire un tel
fichier ne fait pas partie de ce que je veux vous montrer aujourd'hui.

On peut ensuite lancer notre image :

```
$ docker run -p 8000:8000 hello
```

Et cette fois, aller à l'adresse
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) pour admirer le
résultat.

À part le numéro du port qui change sans raison particulière (8000 vs
5000), la différence ici est que l'image Docker est prête à être
utilisée en production. Au lieu du serveur de test de Flask, nous
utilisons nginx et gunicorn qui sont conçus pour tenir la charge face
à de vrais utilisateurs.

### Intégration continue

Nous avons testé notre image Docker en local, maintenant nous
souhaitons la construire lors de chaque modification de notre projet
sur GitHub. Ce qui va se passer, c'est qu'on va envoyer notre
modification sur GitHub, et Circle CI lancer les tests puis va
construire l'image Docker pour nous, en suivant les instructions
présentes dans .circle/config.yml.

Ici, il faut me donner votre identifiant GitHub, pour que je puisse
vous rajouter au projet, et que vous ayez le droit d'envoyer votre
modification.

Sans rentrer dans les détails de git si vous ne connaissez pas, vous
allez chacun travailler dans votre propre branche qui contiendra vos
modifications :

```
$ git checkout -b votre-nom
$ git commit hello.py
$ git push origin votre-nom
```

## Kubernetes

Kubernetes est un outil d'une très grande complexité qui peut réaliser
un nombre incalculable de choses. C'est le descendant direct du
système que Google utilise depuis des années en interne, mais offert
comme logiciel libre. Aujourd'hui, c'est devenu une façon courante de
déployer son application, qui est offerte par Google, mais aussi
Amazon, Microsoft Azure ou encore Digital Ocean. Nous allons utiliser
ses fonctionnalités les plus simples, celles qui sont utiles en tant
que développeur.

Kubernetes permet d'utiliser des clusters :

 * un cluster est un ensemble d'ordinateurs appelés noeuds
 * sur chaque noeud, on peut déployer des images Docker comme celle
   que nous avons construite plus haut

La configuration se fait dans des fichiers YAML. Nous en verrons deux
aujourd'hui :

 * un déploiement est une configuration qui décrit une image Docker
   qui pourra être répliquée sur plusieurs noeuds
 * un service est une autre configuration permettant de rendre
   accessible par Internet nos images Docker

Ce sont des concepts importants, donc je vais essayer d'insister pour
en parler à l'oral.

J'ai choisi d'utiliser Google Cloud Platform, et j'ai donc besoin que
vous me communiquiez un compte Google pour que je vous donne accès au
cluster Kubernetes.

Pour utiliser le cluster que je vous ai préparé, nous devons d'abord
[installer le SDK de Google
Cloud](https://cloud.google.com/sdk/docs/downloads-interactive#linux).

Il faut ensuite initialiser l'environnement :

```
$ gcloud init
$ gcloud container clusters get-credentials c1 --zone
europe-west6-a --project devops-epitech
```

## Premier déploiement

Modifiez le fichier hello.yml pour remplacer "quentin" par votre
prénom. Il faut aussi modifier la version de l'image (après les :)
pour utiliser le sha1 de votre commit git. Vous pouvez l'obtenir avec
"git log".

Ensuite, il suffit de lancer "$ kubectl apply -f
hello.yml", ce qui va créer un déploiement, et ici mettre
en place trois répliques de votre image Docker. Comme on veut qu'elles
soient disponibles sur Internet, il y aussi un "service". Quelle est
son adresse IP ?

Vous pouvez utiliser l'interface web :

https://console.cloud.google.com/kubernetes/discovery?project=devops-epitech&service_list_tablesize=50

Ou la ligne de commande :

```
$ kubectl get services
```

Repérez le votre, et allez sur l'IP et le port 8000. Bravo, vous votre
application est en ligne. Et résiste à la charge, nous avons trois
répiliques, et à chaque fois gunicorn lance 4 instances, donc 12
serveurs répondent en même temps.

## Monitoring

Je vous ai préparé un dashboard Grafana montrant des métriques liées à
votre site web : http://34.65.175.126:3000/d/KKmr-UcZz/flask?orgId=1

C'est indispensable pour corriger un problème quand ça va mal.

## Déployer une nouvelle version

Changez à nouveau la chaîne dans hello.py. Poussez dans GitHub, et
mettez à jour votre déploiement. Durant tout ce temps là,
l'application est restée disponible !
