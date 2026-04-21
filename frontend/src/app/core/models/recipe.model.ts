export interface Recipe {
  id: string;
  title: string;
  country: string;
  countryCode: string;
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

export interface MatchSuggestion {
  matchId: string;
  recipeA: Recipe;
  recipeB: Recipe;
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
