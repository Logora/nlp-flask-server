# Logora NLP [![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)

Logora Modération est une API d'analyse de texte. Elle permet de faire différente tâche comme déterminer si un texte est du spam, déterminer la qualité du texte, et extraire des mots-clés à partir d'un corpus de textes.

En plus de l'API, ce dépôt contient des scripts pour importer des données et calculer des statistiques sur la modération (/scripts), ainsi que les modèles d'apprentissage utilisés par l'API.

[API](https://moderation.logora.fr) [Documentation](https://moderation.logora.fr/docs)

## Installation

```bash
git clone https://github.com/hboisgibault/LogoraNLP.git
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
- Créer un fichier .env avec les bonnes variables d'environnement. Prendre pour exemple .env.example

- Lancer la migration initiale : 
```bash
flask db upgrade
```

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
