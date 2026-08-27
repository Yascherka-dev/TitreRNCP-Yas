/**
 * Partenaires affichés sur la fiche match.
 *
 * Aucun de ces partenariats n'existe : ce sont des marques réelles, mises en
 * scène pour illustrer le parcours complet « je choisis mon match, je regarde,
 * je cuisine ». Chaque lien mène à une page-relais interne qui le dit
 * explicitement — jamais vers une imitation du site du partenaire.
 */

export type PartnerKind = 'streaming' | 'food';

export interface Partner {
  slug: string;
  name: string;
  kind: PartnerKind;
  /** Accroche affichée dans la liste de la fiche match. */
  tagline: string;
  ctaLabel: string;
  color: string;
  emoji: string;
  badge?: string;
  /** Ce que le bouton ferait dans une version réelle, à la 3e personne. */
  action: string;
  /** Domaine réel du partenaire, cité sans lien. Vide si l'enseigne est inventée. */
  site: string;
  /**
   * Enseigne inventée pour illustrer un modèle économique, par opposition aux
   * marques réelles simplement mises en scène. Ces partenaires ne figurent pas
   * dans les listes de la fiche match : ils ont leur propre emplacement.
   */
  fictional?: boolean;
}

export const PARTNERS: readonly Partner[] = [
  // ── Diffuseurs ────────────────────────────────────────────────────────────
  {
    slug: 'canal-plus',
    name: 'Canal+',
    kind: 'streaming',
    tagline: 'Champions League, Ligue 1 — en direct et en exclusivité.',
    ctaLabel: 'Regarder le match',
    color: '#000000',
    emoji: '📺',
    badge: 'Exclusif',
    action: 'ouvrirait la page de diffusion du match',
    site: 'canalplus.com',
  },
  {
    slug: 'bein-sports',
    name: 'beIN Sports',
    kind: 'streaming',
    tagline: 'La Liga, Serie A et bien plus — live & replay.',
    ctaLabel: 'Accéder au direct',
    color: '#D4002D',
    emoji: '⚽',
    action: 'lancerait le direct de la rencontre',
    site: 'beinsports.com',
  },
  {
    slug: 'dazn',
    name: 'DAZN',
    kind: 'streaming',
    tagline: 'Le sport en streaming, sans engagement.',
    ctaLabel: 'Voir le match',
    color: '#F8E220',
    emoji: '▶️',
    action: 'ouvrirait le flux du match',
    site: 'dazn.com',
  },

  // ── Livraison et courses ──────────────────────────────────────────────────
  {
    slug: 'hellofresh',
    name: 'HelloFresh',
    kind: 'food',
    tagline: 'Kit repas personnalisé pour ce match : ingrédients frais, recette étape par étape.',
    ctaLabel: 'Commander le kit',
    color: '#6DB33F',
    emoji: '📦',
    badge: 'Kit repas',
    action: 'composerait un kit avec les ingrédients des deux recettes',
    site: 'hellofresh.fr',
  },
  {
    slug: 'uber-eats',
    name: 'Uber Eats',
    kind: 'food',
    tagline: 'Le plat déjà préparé, livré en moins de 30 min.',
    ctaLabel: 'Commander maintenant',
    color: '#06C167',
    emoji: '🛵',
    action: 'chercherait des restaurants servant ces plats près de chez vous',
    site: 'ubereats.com',
  },
  {
    slug: 'carrefour-drive',
    name: 'Carrefour Drive',
    kind: 'food',
    tagline: 'Tous les ingrédients en un clic, retrait en 2h.',
    ctaLabel: 'Faire mes courses',
    color: '#004E9F',
    emoji: '🛒',
    action: 'remplirait un panier avec la liste de courses des deux recettes',
    site: 'carrefour.fr',
  },
  // ── Enseigne inventée, mise en avant sur la page de connexion ─────────────
  {
    slug: 'la-maison-du-canard',
    name: 'La Maison du Canard',
    kind: 'food',
    tagline: 'Kit match du soir livré en 2h : ingrédients frais pré-dosés.',
    ctaLabel: "Découvrir l'offre",
    color: '#8B4A2B',
    emoji: '🦆',
    action: 'livrerait les ingrédients pré-dosés avant le coup d\'envoi',
    site: '',
    fictional: true,
  },
] as const;

// Les enseignes inventées sont exclues : elles ont leur propre emplacement.
export const STREAMING_PARTNERS = PARTNERS.filter(p => p.kind === 'streaming' && !p.fictional);
export const FOOD_PARTNERS      = PARTNERS.filter(p => p.kind === 'food' && !p.fictional);

export function findPartner(slug: string | null): Partner | undefined {
  return PARTNERS.find(p => p.slug === slug);
}
