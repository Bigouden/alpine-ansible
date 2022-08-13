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
| ------ | ------ |
| Alpine Linux | 3.16 |
| Ansible Core | 2.13.2 |
| Ansible Lint | 6.4.0 |

## Liste des fichiers

| Fichier / Répertoire | Description |
| ------ | ------ |
| Dockerfile | Recette de création du conteneur |
| .gitlab-ci.yml | Instruction CI/CD |
| README.md | Description du projet |
| apk_packages | Liste des paquets APK à installer |
| pip_packages | Liste des paquets PIP à installer |
| ansible_collections | Liste des collections ANSIBLE à installer |
| .pylintrc | Règles du linteur Python |

## Mise à jour

Les logiciels **Ansible Core** et **Ansible Lint** étant installés depuis les dépôts PIP, il faut régulièrement les mettre à jour.

La liste des versions est disponible ici :

- Ansible Core : https://pypi.org/project/ansible-core/#history
- Ansible Lint : https://pypi.org/project/ansible-lint/#history

Lorsqu'une nouvelle version sort, il faut mettre à jour les versions dans le fichier **pip_packages**.

## Collections

Les collections sont un ensemble de module généralement regroupées par catégorie qu'il est possible d'ajouter à Ansible.

Les collections suivantes sont installées dans le conteneur :

- ansible.posix (https://docs.ansible.com/ansible/latest/collections/ansible/posix/index.html)
- community.crypto (https://docs.ansible.com/ansible/latest/collections/community/crypto/index.html)
- community.docker (https://docs.ansible.com/ansible/latest/collections/community/crypto/index.html)
- community.kubernetes (https://docs.ansible.com/ansible/latest/collections/community/kubernetes/index.html)
- community.general (https://docs.ansible.com/ansible/latest/collections/community/general/index.html)
- google.cloud (https://docs.ansible.com/ansible/latest/collections/google/cloud/index.html)
- ansible.netcommon (https://docs.ansible.com/ansible/latest/collections/ansible/netcommon/index.html)
- community.postgresql (https://docs.ansible.com/ansible/latest/collections/community/postgresql/postgresql_db_module.html)
- community.mongodb (https://docs.ansible.com/ansible/latest/collections/community/mongodb/index.html)

Elles sont renseignées dans le fichier **ansible_collections**.
