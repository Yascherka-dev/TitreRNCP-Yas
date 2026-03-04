import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { MatchSuggestion } from '../models/recipe.model';
import { pickRecipe } from '../../features/recipes/data/mock-recipes';

@Injectable({ providedIn: 'root' })
export class SuggestionsService {
  private cache = new Map<string, MatchSuggestion>();

  getSuggestion(matchId: number, homeCountry: string, awayCountry: string): Observable<MatchSuggestion> {
    const key = `${matchId}`;
    if (this.cache.has(key)) return of(this.cache.get(key)!);
    return of(this.build(matchId, homeCountry, awayCountry));
  }

  regenerate(matchId: number, homeCountry: string, awayCountry: string): Observable<MatchSuggestion> {
    const current = this.cache.get(`${matchId}`);
    this.cache.delete(`${matchId}`);
    return of(this.build(matchId, homeCountry, awayCountry, current?.recipeA.id, current?.recipeB.id));
  }

  private build(
    matchId: number,
    homeCountry: string,
    awayCountry: string,
    excludeA?: string,
    excludeB?: string,
  ): MatchSuggestion {
    const recipeA = pickRecipe(homeCountry, excludeA) ?? pickRecipe('fr')!;
    const recipeB = pickRecipe(awayCountry, excludeB) ?? pickRecipe('fr')!;
    const suggestion: MatchSuggestion = { matchId, recipeA, recipeB, generatedAt: new Date() };
    this.cache.set(`${matchId}`, suggestion);
    return suggestion;
  }
}
