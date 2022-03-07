# Logora Modération [![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)

Logora Modération est une API d'analyse de texte. Elle permet de faire différente tâche comme déterminer si un texte est du spam, déterminer la qualité du texte, et extraire des mots-clés à partir d'un corpus de textes.

En plus de l'API, ce dépôt contient des scripts pour importer des données et calculer des statistiques sur la modération (/scripts), ainsi que les modèles d'apprentissage utilisés par l'API.

[API](https://moderation.logora.fr) [Documentation](https://moderation.logora.fr/docs)

## Installation

```bash
git clone https://github.com/hboisgibault/LogoraModeration.git
```

Installer les dépendances de l'API grâce à [pip](https://pip.pypa.io/en/stable/)
```bash
pip install -r requirements.txt
```

Pour les dépendances liées aux scripts d'import et de statistiques, utiliser les commandes suivantes :
```bash
cd scripts/
pip install -r requirements.txt
```

## Utilisation


### API
- Utiliser le fichier app.py
```bash
python app/app.py
```
- Avec Docker :
```bash
docker build -t logora-moderation .
docker-compose up
```
Le serveur est disponible à l'adresse https://localhost:8000 et la documentation à l'adresse https://localhost:8000/docs

### Scripts annexes

#### Importation des données
Pour importer les dernières données, utiliser le fichier `scripts/importer.py`. Pour cela, copier le fichier `.env.example` et remplacez-le par les bonnes variables d'environnements. Ensuite lancer `python importer.py`. Cela va importer les dernières contributions dans le dossier /data.

#### Statistiques
Le script `scripts/stats.py` permet de récupérer des statistiques sur la modération et sur la pertinence.
Pour l'utiliser, lancer `python scripts/stats.py`. 

## Mise à jour du modèle
---

## Comment mettre à jour le modèle ?

- Télécharger le dernier csv avec tous les arguments Logora via le fichier importer.py

- Depuis le terminal lancer la commande **jupyter notebook** (si nécessaire **pip install notebook** au préalable)

- Ouvrir notebooks/TEST MODEL.ipynb

- Suivre les instructions (remplacer *messages_dateheureminute.csv* par le dernier csv et run les cellules pour observer les résultats *AB testing*)

- Sauvegarder puis ouvrir notebooks/CREATE MODEL.ipynb

- Suivre les instructions (remplacer le dernier csv et uncomment les cellules pour exporter le vectorizer et le modèle au format joblib)

- Tout est ok lib/model.joblib et lib/tfidf.joblib ont été mis à jour !

---

## Comment mettre à jour le modèle CamemBert ?
- Télécharger le dernier csv avec tous les arguments Logora via le fichier importer.py

- Depuis le terminal lancer la commande **jupyter notebook** (si nécessaire **pip install notebook** au préalable)

- Ouvrir logora_camembert_prod.ipynb

- Modifier le nom du fichier de données par le dernier csv puis exécuter toutes les cellules (run all)

- À la fin de l'exécution, 3 nouveaux fichiers et dossiers seront créés : un dossier model qui contient le modèle après apprentissage (tf_model.h5 et config.json) et deux fichiers DataFrame qui sont les faux positifs et les faux négatifs (il est possible de supprimer cette partie car elle n'influence pas le reste du programme)

Si tout celà ne fonctionne pas (car tout a été écrit sur Google Colab et pas Jupyter Notebook) :
- Télécharger le dernier csv avec tous les arguments Logora via le fichier importer.py et télécharger le notebook logora_camembert_prod.ipynb

- Importer les deux documents dans un dossier Google Drive

- Ouvrir le notebook via Google Colab  

- Dé-commenter la première cellule et faire en sorte que le Drive soit monté sur Colab. Puis modifier le path du fichier csv des données en fonction de son emplacement dans le drive

- Exécuter toutes les cellules (run all)

- À la fin de l'exécution, 3 nouveaux fichiers et dossiers seront créés dans le dossier Drive de départ : un dossier model qui contient le modèle après apprentissage (tf_model.h5 et config.json) et deux fichiers DataFrame qui sont les faux positifs et les faux négatifs (il est possible de supprimer cette partie car elle n'influence pas le reste du programme)

---
## Commentaires

Le dossier data est là à titre purement indicatif, il n'est pas utilisé dans le code mais dans les notebooks

**fr_dataset.csv** est un dataset de commentaires récuperé en ligne, ne pas toucher

**messages_dateheureminute.csv** est le dernier fichier des commentaires Logora



