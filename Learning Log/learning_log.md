# Learning Log — Projet "Learning Path Architect"

## 2026-05-13 — Version 1

- Compréhension des livrables attendus.
- Décision : agent IA local sans API + application Streamlit.
- Choix des domaines proposés (ML, Python, Data Science, Prompt Engineering, Langues, etc.).
- Implémentation de la génération de roadmap avec plan jour-par-jour.
- Ajout d'un contrôle hebdomadaire basé sur le contenu appris.
- Intégration de ressources gratuites officielles (liens réels).
- Export Markdown du parcours généré.

## 2026-05-13 — Version 2

- Remplacement du formulaire statique par un **flux de conversation étape par étape** (identifiant, prénom, âge, genre, niveau, objectif, heures/semaine, intérêts).
- Ajout d'une **suggestion automatique de domaines** basée sur les mots-clés des intérêts (python → Python / Data Science / ML ; web → Développement Web ; security → Cybersécurité ; prompt/chatgpt → Prompt Engineering ; anglais/français → langue correspondante) avec possibilité de confirmer ou corriger la sélection.
- **Persistance locale JSON** : les profils utilisateurs sont sauvegardés dans un répertoire `data/` et rechargés automatiquement à la prochaine session via l'identifiant.
- Ajout de **cases à cocher** (checkboxes) sur les tâches quotidiennes et d'une **barre de progression globale** (tâches complétées / semaines × 7).
- Réorganisation de l'interface en **3 onglets** :
  - *Aujourd'hui* : tâche du jour avec checkbox + articles Dev.to + ressources officielles.
  - *Roadmap* : semaine en cours uniquement + quiz de fin de semaine.
  - *Progression* : métriques, détail par semaine, récapitulatif du profil.
- Intégration de **ressources dynamiques** via l'API gratuite Dev.to (`GET /api/articles?tag={tag}&per_page=10`) avec cache de 1 heure en session Streamlit.
