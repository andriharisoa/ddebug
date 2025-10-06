# ddebug

**ddebug** est un outil Python pour déboguer rapidement des conteneurs Docker. Il permet d'ouvrir un conteneur de debug attaché à un conteneur cible, avec accès aux namespaces PID, réseau et aux volumes du conteneur. Il inclut des outils système et réseau avancés, ainsi que le shell **fish** pour une expérience interactive améliorée.

---

## Fonctionnalités

* Débogue un conteneur Docker en partageant ses namespaces PID et réseau.
* Monte les volumes du conteneur cible pour accéder à ses fichiers.
* Lancement automatique du shell **fish** dans le conteneur de debug.
* Conteneur éphémère : tout est supprimé à la fermeture.
* Basé sur l’image **nicolaka/netshoot**, avec de nombreux outils réseau et système.

---

## Prérequis

* Python 3
* Docker installé et accessible
* Conteneur cible en cours d’exécution
* Permissions suffisantes pour utiliser `--privileged` et accéder aux namespaces

---

## Installation

Clonez le dépôt et rendez le script exécutable :

```bash
git clone https://github.com/andriharisoa/ddebug.git
cd ddebug
chmod +x ddebug.py
```

---

## Utilisation

### Déboguer un conteneur

```bash
./ddebug.py debug <nom_ou_id_du_conteneur>
```

Exemple :

```bash
./ddebug.py debug mybackend
```

Le script lance un conteneur `ddebug_mybackend` attaché à `mybackend`.
Le shell **fish** sera automatiquement installé et lancé.

### Options

* `--shell SHELL` : Choisir un shell différent (par défaut `fish`).

Exemple :

```bash
./ddebug.py debug mybackend --shell /bin/sh
```

---

## Fonctionnement

1. Vérifie que Docker est installé et que le conteneur cible existe et est en cours d’exécution.
2. Supprime tout conteneur debug existant avec le même nom.
3. Lance un nouveau conteneur avec les options suivantes :

* `--privileged`
* `--pid=container:<target>`
* `--net=container:<target>`
* `--volumes-from <target>`

4. Le conteneur de debug contient tous les outils de **nicolaka/netshoot** et le shell **fish**.

---

## Outils disponibles dans le conteneur de debug

* `ps`, `top`
* `netstat`, `ip`, `ping`
* `curl`, `wget`, `tcpdump`
* `nc`, `telnet`
* `fish`
* `vim` ou autres éditeurs installés

---

## Contribution

Les contributions sont les bienvenues.
Proposez des améliorations pour ajouter des outils, des shells alternatifs ou des options avancées.

---

## Licence

MIT License
