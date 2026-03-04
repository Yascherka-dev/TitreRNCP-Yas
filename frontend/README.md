# Match & Munch

Plateforme web qui répond à la question : **« On mange quoi devant le match de ce soir ? »**

Pour chaque match sélectionné, Match & Munch suggère deux recettes inspirées des spécialités culinaires des pays des équipes qui s'affrontent.

## Stack technique

- **Frontend** : Angular 19 + Angular Material
- **Backend** : Django REST Framework *(à venir)*
- **Base de données** : PostgreSQL

## Lancer le projet

```bash
npm install
ng serve
```

L'application sera disponible sur `http://localhost:4200`.

## Fonctionnalités

- Liste des matchs du jour avec filtres par compétition
- Fiche match avec deux recettes associées (une par pays)
- Régénération des suggestions de recettes
- Notation et avis sur les recettes
- Design responsive, adapté mobile et desktop
