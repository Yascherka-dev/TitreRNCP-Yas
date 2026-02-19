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
