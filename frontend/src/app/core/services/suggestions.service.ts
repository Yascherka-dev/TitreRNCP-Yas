import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { MatchSuggestion, Recipe } from '../models/recipe.model';
import { pickRecipe } from '../../features/recipes/data/mock-recipes';

@Injectable({ providedIn: 'root' })
export class SuggestionsService {

  // Cache en mémoire — évite de re-générer à chaque visite
  private cache = new Map<string, MatchSuggestion>();

  getSuggestion(matchId: number, countryA: string, countryB: string): Observable<MatchSuggestion> {
    const key = `${matchId}`;

    if (this.cache.has(key)) {
      return of(this.cache.get(key)!);
    }

    return of(this.generate(matchId, countryA, countryB));
  }

  regenerate(matchId: number, countryA: string, countryB: string): Observable<MatchSuggestion> {
    this.cache.delete(`${matchId}`);
    return of(this.generate(matchId, countryA, countryB));
  }

  private generate(matchId: number, countryA: string, countryB: string): MatchSuggestion {
    const recipeA = pickRecipe(countryA);
    const recipeB = pickRecipe(countryB);

    const suggestion: MatchSuggestion = {
      matchId,
      recipeA: recipeA ?? this.fallback(countryA),
      recipeB: recipeB ?? this.fallback(countryB),
      generatedAt: new Date(),
    };

    this.cache.set(`${matchId}`, suggestion);
    return suggestion;
  }

  private fallback(countryCode: string): Recipe {
    return {
      id: `fallback-${countryCode}`,
      title: 'Recette locale',
      country: countryCode,
      countryCode,
      flag: `https://media.api-sports.io/flags/${countryCode}.svg`,
      description: 'Une recette typique de ce pays.',
      prepTime: 20,
      cookTime: 30,
      servings: 2,
      difficulty: 'Facile',
      imageUrl: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600',
      ingredients: [],
      steps: [],
      tags: [],
    };
  }
}
