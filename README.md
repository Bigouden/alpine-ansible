# ANSIBLE

Le projet **ansible** permet la génération d'un conteneur Ansible basé sur une distribution Alpine.

---

- [Informations générales](#informations-générales)
- [Liste des fichiers](#liste-des-fichiers)
- [Mise à jour](#mise-à-jour)
- [Collections](#collections)

---

## Informations générales

| Système d'exploitation / Logiciel | Version |
|-----------------------------------|---------|
| Alpine Linux                      | 3.19    |
| Ansible Core                      | 2.16.6  |
| Ansible Lint                      | 24.2.2  |

## Liste des fichiers

| Fichier / Répertoire | Description                               |
|----------------------|-------------------------------------------|
| Dockerfile           | Recette de création du conteneur          |
| .gitlab-ci.yml       | Instruction CI/CD                         |
| README.md            | Description du projet                     |
| apk_packages         | Liste des paquets APK à installer         |
| pip_packages         | Liste des paquets PIP à installer         |
| ansible_collections  | Liste des collections ANSIBLE à installer |
| .pylintrc            | Règles du linteur Python                  |

## Mise à jour

Les logiciels **Ansible Core** et **Ansible Lint** étant installés depuis les dépôts PIP, il faut régulièrement les mettre à jour.

La liste des versions est disponible ici :

- Ansible Core : <https://pypi.org/project/ansible-core/#history>
- Ansible Lint : <https://pypi.org/project/ansible-lint/#history>

Lorsqu'une nouvelle version sort, il faut mettre à jour les versions dans le fichier **pip_packages**.

## Collections

Les collections sont un ensemble de module généralement regroupées par catégorie qu'il est possible d'ajouter à Ansible.

Les collections suivantes sont installées dans le conteneur :

- ansible.posix (<https://docs.ansible.com/ansible/latest/collections/ansible/posix/index.html>)
- community.crypto (<https://docs.ansible.com/ansible/latest/collections/community/crypto/index.html>)
- community.docker (<https://docs.ansible.com/ansible/latest/collections/community/crypto/index.html>)
- community.general (<https://docs.ansible.com/ansible/latest/collections/community/general/index.html>)
- google.cloud (<https://docs.ansible.com/ansible/latest/collections/google/cloud/index.html>)
- ansible.netcommon (<https://docs.ansible.com/ansible/latest/collections/ansible/netcommon/index.html>)
- community.postgresql (<https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_db_module.html>)
- community.mongodb (<https://docs.ansible.com/ansible/latest/collections/community/mongodb/index.html>)
- community.mysql (<https://docs.ansible.com/ansible/latest/collections/community/mysql/index.html>)
- kubernetes.core (<https://docs.ansible.com/ansible/latest/collections/kubernetes/core/index.html>)

Elles sont renseignées dans le fichier **ansible_collections**.

## Exporter Prometheus

Le point d'entrée du conteneur agit maintenant comme un exporter prometheus fournissant les versions :

- ansible_core
- ansible_lint
- ansible_collection

Par défaut l'exporter est en écoute sur le port 8123 (surcharge possible à partir de la variable d'environnement : ANSIBLE_EXPORTER_PORT)

### Exemple de métriques

```bash
# HELP ansible_core Ansible Core Information
# TYPE ansible_core gauge
ansible_core{job="ansible-exporter",version="2.14.1"} 1.0
# HELP ansible_lint Ansible Lint Information
# TYPE ansible_lint gauge
ansible_lint{job="ansible-exporter",version="6.10.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="ansible.posix",version="1.4.0"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="ansible.netcommon",version="4.1.0"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="ansible.utils",version="2.8.0"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.kubernetes",version="2.0.1"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.mongodb",version="1.4.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.postgresql",version="2.3.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.docker",version="3.3.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.crypto",version="2.10.0"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="community.general",version="6.2.0"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="kubernetes.core",version="2.3.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="google.cloud",version="1.1.2"} 1.0
# HELP ansible_collection Ansible Collection Information
# TYPE ansible_collection gauge
ansible_collection{job="ansible-exporter",name="openstack.cloud",version="1.10.0"} 1.0
```
