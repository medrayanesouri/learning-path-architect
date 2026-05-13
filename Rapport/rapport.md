# Rapport — Architecte de "Learning Paths" et stratégies d'apprentissage

## 1. Introduction

Ce projet vise à concevoir un agent IA local capable de construire un parcours d'apprentissage personnalisé, en fonction du profil, du temps disponible et de l'objectif de l'utilisateur. L'application est développée avec Streamlit et ne nécessite aucune API payante.

## 2. Objectifs

- Poser des questions à l'utilisateur de manière conversationnelle.
- Proposer automatiquement la durée du parcours et les domaines adaptés.
- Générer un plan d'apprentissage jour par jour avec des ressources gratuites.
- Fournir un contrôle hebdomadaire pour évaluer la progression.

## 3. Méthodologie (Version 1)

L'agent utilise une logique de recommandation par heuristiques :

- Si l'utilisateur est débutant ou dispose de peu d'heures, la durée du parcours augmente.
- Si l'objectif est un portfolio, la durée est plus longue.
- Chaque semaine contient un module thématique, un plan quotidien (5 jours d'apprentissage, 1 révision, 1 contrôle) et un quiz.

### Architecture de l'application (v1)

- Interface Streamlit (web local, formulaire statique).
- Moteur de recommandation basé sur des règles.
- Génération automatique des modules, tâches quotidiennes et quiz.
- Export Markdown pour télécharger le parcours.

### Ressources intégrées (v1)

Le système propose des ressources gratuites officielles selon le domaine choisi (ML, Data Science, Python, Web, Cybersécurité, Prompt Engineering, Français, Anglais).

## 4. Améliorations — Version 2

La Version 2 apporte plusieurs évolutions majeures à l'application.

### 4.1 UX conversationnelle

Le formulaire statique est remplacé par un flux de questions posées une à une : identifiant utilisateur, prénom, âge, genre, niveau, objectif, heures disponibles par semaine, centres d'intérêt. L'agent suggère ensuite automatiquement 2 à 3 domaines basés sur les mots-clés détectés dans les intérêts (ex. : « python » → Python / Data Science / ML ; « web » → Développement Web ; « prompt » ou « chatgpt » → Prompt Engineering) et laisse l'utilisateur confirmer ou corriger la sélection.

### 4.2 Persistance locale (JSON)

Les profils utilisateurs (données personnelles, domaines choisis, tâches complétées, date de début) sont sauvegardés automatiquement sous forme de fichiers JSON dans un répertoire local `data/`. À chaque nouvelle session, l'utilisateur entre son identifiant et son profil est rechargé instantanément, lui permettant de reprendre exactement là où il en était.

### 4.3 Suivi de progression

Des cases à cocher (checkboxes) sont associées aux tâches quotidiennes. Une barre de progression globale affiche en permanence le ratio de tâches accomplies sur le total du parcours (semaines × 7 jours). L'onglet *Progression* détaille les statistiques semaine par semaine.

### 4.4 Interface à onglets

L'interface est organisée en trois onglets :

- **Aujourd'hui** : tâche du jour (avec checkbox), articles dynamiques Dev.to et ressources officielles.
- **Roadmap** : plan complet de la semaine en cours uniquement + quiz de fin de semaine.
- **Progression** : métriques globales, détail par semaine, récapitulatif du profil.

### 4.5 Ressources dynamiques via l'API Dev.to

Pour enrichir les ressources sans recourir à une API payante, l'application interroge l'API publique et gratuite de Dev.to (`GET https://dev.to/api/articles?tag={tag}&per_page=10`) en fonction du domaine sélectionné. Les résultats sont mis en cache pendant une heure dans la session Streamlit afin de limiter les appels réseau.

## 5. Limites & perspectives

- La persistance est locale (pas de base de données distante) : les profils ne sont pas partagés entre machines.
- Améliorations futures possibles : export PDF, authentification, scoring de niveau, version bilingue de l'interface.

## 6. Conclusion

L'agent IA local permet d'architecturer un parcours d'apprentissage réaliste et personnalisé, tout en restant entièrement gratuit et sans API payante. La Version 2 améliore significativement l'expérience utilisateur grâce à l'UX conversationnelle, la persistance JSON, les indicateurs de progression et l'intégration de contenu dynamique via Dev.to.
