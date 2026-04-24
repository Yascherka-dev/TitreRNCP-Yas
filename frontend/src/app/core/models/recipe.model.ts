export interface Recipe {
  id: string;
  title: string;
  country: string;
  countryCode: string;
  region: string;
  equipe: string;
  typePlat: 'salé' | 'sucré';
  flag: string;
  description: string;
  prepTime: number;
  cookTime: number;
  servings: number;
  difficulty: 'Facile' | 'Moyen' | 'Difficile';
  imageUrl: string;
  ingredients: string[];
  steps: string[];
  tags: string[];
}

export interface Beer {
  id: string;
  nom: string;
  brasserie: string;
  pays: string;
  region: string;
  equipe: string;
  style: string;
  description: string;
  degreAlcool: string | null;
  ibu?: number;
  volume?: string;
  imageUrl: string;
}

export interface MatchSuggestion {
  matchId: string;
  recetteA: Recipe | null;
  recetteB: Recipe | null;
  pecheMignonA: Recipe | null;
  pecheMignonB: Recipe | null;
  biereA: Beer | null;
  biereB: Beer | null;
  generatedAt: Date;
}

export interface RecipeComment {
  id: string;
  recipeId: string;
  author: string;
  content: string;
  rating: number;
  date: Date;
}
