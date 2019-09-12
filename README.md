# Séminaire DevOps - Epitech Saint-André

Nous avons quatre heures pour vous donner une idée des pratiques
DevOps. Ce qu'on va faire, c'est vous donner une idée des tâches qui
vous attendent en tant que développeurs dans un tel système.

Nous allons partir sur un exemple concret, une bête application Flask
qui va servir à introduire les concepts que j'ai jugé les plus
importants dans une introduction, parce qu'utiles au jour le jour.

Cette application Flask sera la plus basique possible : elle
n'affichera qu'un simple message dans votre navigateur. Ce qui va nous
intéresser ici, c'est tout le reste :

 * l'empaquetage de l'application dans Docker
 * l'intégration continue pour tester l'application
 * le déploiement dans Kubernetes
 * la surveillance de l'application
 * la haute disponiblité, et les mises à jour de cette application

Une manière simple de voir le mouvement DevOps est que vous ne faites
plus que développer une application, vous gérez tout son cycle de vie,
ce qui demande de nouvelles compétences dont on va parler aujourd'hui.

## Pré-requis

J'ai choisi d'utiliser GitHub pour stocker le code source, Circle CI
pour l'intégration continue, et Google Cloud Platform pour le
déploiement dans Kubernetes. Rien n'oblige à utiliser ces outils là en
particulier, et ils ont tous des concurrents tout aussi performants,
mais j'ai préféré utiliser des outils que je connais déjà pour pouvoir
vous aider au mieux si vous rencontrez un problème.

Du coup, il faut un compte GitHub, pour vous donner accès à ce projet,
et un compte Google pour vous donner accès au projet Google Cloud
Platform que j'ai créé pour ce séminaire. Merci de me les envoyer par
mail. Différents outils sont indispensables aujourd'hui : Docker, git
et le SDK Google Cloud. Nous les installerons le moment opportun.

## Modification de l'application Flask Hello

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
$ FLASK_APP=hello.py pipenv run flask
```

Puis voir le résultat dans votre navigateur :
[http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Test dans Docker en local

Pour déployer notre application, nous allons utiliser une image
Docker, qui va contenir à elle seule un système d'exploitation,
Python, notre application et ces dépendances. Le grand avantage de
Docker ici est que le fonctionnement sera exactement le même chez vous
et déployé dans le cloud.

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

Cette commande suite les instructions présentes dans le fichier
Dockerfile. Apprendre à écrire un tel fichier ne fait pas partie de ce
que je veux vous montrer aujourd'hui.

Et l'éxecuter :

```
$ docker run -p 8000:8000 hello
```

Et cette fois, aller à l'adresse
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) pour admirer le
résultat.

À part le numéro du port, la différence ici est que l'image Docker est
prête à être utilisée en production. Au lieu du serveur de test de
Flask, nous utilisons nginx et gunicorn qui sont conçus pour tenir la
charge face à de vrais utilisateurs.

### Intégration continue

Nous avons testé notre image Docker en local, maintenant nous
souhaitons la construire lors de chaque modification de notre projet
sur GitHub. Ce qui va se passer, c'est qu'on va envoyer notre
modification sur GitHub, et Circle CI va construire l'image Docker pour
nous, en suivant les instructions présentes dans .circle/config.yml.

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

J'ai choisi d'utiliser Google Cloud Platform, et j'ai donc besoin que
vous me communiquiez un compte Google pour que je vous donne accès au
cluster Kubernetes.

Pour utiliser le cluster que je vous ai préparé, nous devons d'abord
[installer le SDK de Google
Cloud](https://cloud.google.com/sdk/docs/downloads-interactive#linux).

Il faut ensuite initialiser l'environnement :

```
$ gcloud init
$ gcloud container clusters get-credentials your-first-cluster-1 --zone
europe-west6-a --project devops-epitech
```

Il y a quelques concepts Kubernetes à définir :

 * un cluster est un ensemble de noeuds, autrement dit un ensemble
   d'ordinateurs
 * sur chaque noeud, on peut avoir des pods, qui sont des ensembles de
   conteneurs Docker, même si souvent chaque pod ne contient qu'un
   conteneur Docker
 * un déploiement est un ensemble de pods, chaque pod tournant en
   général sur un noeud différent
 * un service est un moyen de faire des requêtes sur les pods d'un
   déploiement

Ce sont des concepts importants, donc je vais essayer d'insister pour
en parler à l'oral.

## Premier déploiement

Modifiez le fichier hello-deployment.yml pour remplaer "votrenom" par
"votrenom" (moi j'ai mis "quentin"). Il faut aussi modifier
"votresha1" pour utiliser le sha1 de votre commit. Vous pouvez
l'obtenir avec "git log".

Ensuite, il suffit de lancer "$ kubectl apply -f
hello-deployment.yml", ce qui va créer un déploiement, et ici mettre
en place trois répliques de votre image Docker. Comme on veut qu'elles
soient disponibles sur Internet, il y aussi un "service". Quelle est
son adresse IP ?

```
$ kubectl get services
```

Repérez le votre, et allez sur l'IP et le port 8000. Bravo, vous votre
application est en ligne. Et résiste à la charge, nous avons trois
répiliques, et à chaque fois gunicorn lance 4 instances, donc 12
serveurs répondent en même temps.

## Monitoring

TODO Métriques Prometheus.

## Déployer une nouvelle version

Changez à nouveau la chaîne dans hello.py. Poussez dans GitHub, et
mettez à jour votre déploiement. Durant tout ce temps là,
l'application est restée disponible !
