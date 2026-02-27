export interface Recipe {
  id: string;
  title: string;
  country: string;
  countryCode: string;
  flag: string;
  description: string;
  prepTime: number;   // minutes
  cookTime: number;   // minutes
  servings: number;
  difficulty: 'Facile' | 'Moyen' | 'Difficile';
  imageUrl: string;
  ingredients: string[];
  steps: string[];
  tags: string[];
}

export interface MatchSuggestion {
  matchId: number;
  recipeA: Recipe;
  recipeB: Recipe;
  generatedAt: Date;
}

// Représente un avis laissé par un utilisateur sur une recette.
// Pour l'instant, l'auteur est toujours "Vous" (pas d'auth).
// À l'étape 11 MVP, ces données seront persistées dans Supabase.
export interface RecipeComment {
  id: string;          // UUID généré côté client
  recipeId: string;    // ID de la recette concernée
  author: string;      // Nom de l'auteur — "Vous" tant que l'auth n'est pas branchée
  content: string;     // Texte de l'avis
  rating: number;      // Note de 1 à 5 étoiles
  date: Date;          // Date de soumission
}
