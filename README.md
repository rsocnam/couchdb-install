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

```
ansible/files/
```
