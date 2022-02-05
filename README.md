# ANSIBLE

Le projet **ansible** permet la génération d'un conteneur Ansible basé sur une distribution Alpine.

---

- [Informations générales](#informations-générales)
- [Utilisation](#utilisation)
- [Liste des fichiers](#liste-des-fichiers)
- [Mise à jour](#mise-à-jour)
- [Collections](#collections)
- [Entrypoint](#entrypoint)

---

## Informations générales

| Système d'exploitation / Logiciel | Version |
| ------ | ------ |
| Alpine Linux | 3.15 |
| Ansible Base | 2.10.16 |
| Ansible Lint | 5.3.1 |


## Utilisation  

Sur admintools, PAS en root  

```
dransible
```

## Liste des fichiers

| Fichier / Répertoire | Description |
| ------ | ------ |
| Dockerfile | Recette de création du conteneur |
| .gitlab-ci.yml | Instruction CI/CD |
| README.md | Description du projet |
| entrypoint.py | Script exécuté au lancement du conteneur |
| internal.crt | Autorité de certification |
| apk_packages | Liste des paquets APK à installer |
| pip_packages | Liste des paquets PIP à installer |
| ansible_collections | Liste des collections ANSIBLE à installer |
| ansible.cfg | Fichier de configuration ANSIBLE |
| .pylintrc | Règles du linteur Python |

## Mise à jour

Les logiciels **Ansible Base** et **Ansible Lint** étant installés depuis les dépôts PIP, il faut régulièrement les mettre à jour.

La liste des versions est disponible ici :

- Ansible Base : https://pypi.org/project/ansible-base/#history
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

## Entrypoint

```bash
usage: entrypoint.py [-h] [--url URL] [--username USERNAME]
                     [--password PASSWORD] [--directory DIRECTORY]
                     [--shell SHELL] [--branch BRANCH]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Git HTTP(S) Repository URL
  --username USERNAME   Git Username
  --password PASSWORD   Git Password
  --directory DIRECTORY Git Repository Directory
  --shell SHELL         Unix Shell
  --branch BRANCH       Git Clone Branch
``` 
