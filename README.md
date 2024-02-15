# Logora NLP [![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)

Logora NLP est une API d'analyse de texte et d'extraction de mots clés. Elle permet de résumer les idées principales et d'extraire des mots-clés à partir d'un corpus de textes.

[API](https://nlp.logora.fr) [Documentation](https://nlp.logora.fr/docs)

## Installation
```bash
git clone https://github.com/hboisgibault/LogoraNLP.git
```

Installer les dépendances de l'API grâce à [pip](https://pip.pypa.io/en/stable/)
```bash
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
docker build -t logora-nlp .
docker-compose up
```
Le serveur est disponible à l'adresse https://localhost:8000 et la documentation à l'adresse https://localhost:8000/docs
