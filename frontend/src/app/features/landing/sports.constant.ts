/**
 * Sports proposés par le sélecteur de la landing.
 *
 * Les clés correspondent au champ `sport` renvoyé par l'API — voir LEAGUES
 * dans backend/apps/matches/sports_api.py. Toute ligue ajoutée côté backend
 * dans un sport déjà listé ici apparaît automatiquement.
 */
export const LANDING_SPORTS = [
  { key: 'football',          label: 'Football'    },
  { key: 'rugby',             label: 'Rugby'       },
  { key: 'ice_hockey',        label: 'Hockey'      },
  { key: 'american_football', label: 'Football US' },
  { key: 'basketball',        label: 'Basket'      },
] as const;

export type SportKey = (typeof LANDING_SPORTS)[number]['key'];

export const DEFAULT_SPORT: SportKey = 'football';
