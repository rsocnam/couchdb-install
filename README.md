# Projet NFE204

## Installation via Ansible

L'inventaire, à modifier selon ses besoins, se trouve dans `ansible/hosts.ini`

### Installation de HAProxy

```shell
ansible-playbook -i ansible/hosts.ini ansible/couchdb/install-couchdb.yml
```

### Installation de HAProxy

```shell
ansible-playbook -i ansible/hosts.ini ansible/couchdb/install-haproxy.yml
```

### Fichiers de configuration

Ils se trouvent dans le répertoire `ansible/files/`

## Import des données

Lancer, avec python 3, le script `geonames.py`. Par défaut, le script cherche le fichier `allCountries.txt`