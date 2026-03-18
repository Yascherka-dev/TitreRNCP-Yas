import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, tap, map } from 'rxjs';
import { MatchSuggestion, Recipe } from '../models/recipe.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class SuggestionsService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;
  private cache = new Map<string, MatchSuggestion>();

  getSuggestion(matchId: number | string, paysA: string, paysB: string): Observable<MatchSuggestion> {
    const key = `${matchId}`;
    if (this.cache.has(key)) return of(this.cache.get(key)!);
    return this.fetch(matchId, paysA, paysB);
  }

  regenerate(matchId: number | string, paysA: string, paysB: string): Observable<MatchSuggestion> {
    this.cache.delete(`${matchId}`);
    return this.fetch(matchId, paysA, paysB);
  }

  private fetch(matchId: number | string, paysA: string, paysB: string): Observable<MatchSuggestion> {
    return this.http
      .post<{ recettes: any[] }>(`${this.apiUrl}/suggestions/`, { paysA, paysB })
      .pipe(
        map(res => ({
          matchId: Number(matchId),
          recipeA: this.toRecipe(res.recettes[0]),
          recipeB: this.toRecipe(res.recettes[1]),
          generatedAt: new Date(),
        })),
        tap(s => this.cache.set(`${matchId}`, s))
      );
  }

  private flagUrl(pays: string): string {
    const map: Record<string, string> = {
      'france': 'fr', 'england': 'gb-eng', 'germany': 'de', 'spain': 'es',
      'italy': 'it', 'portugal': 'pt', 'netherlands': 'nl', 'belgium': 'be',
      'brazil': 'br', 'argentina': 'ar', 'japan': 'jp', 'morocco': 'ma',
      'senegal': 'sn', 'nigeria': 'ng', 'usa': 'us', 'mexico': 'mx',
    };
    const code = map[pays.toLowerCase()] ?? pays.toLowerCase();
    return `https://flagcdn.com/w40/${code}.png`;
  }

  private toRecipe(r: any): Recipe {
    return {
      id: String(r.id ?? Math.random().toString(36).slice(2)),
      title: r.titre ?? '',
      country: r.pays ?? '',
      countryCode: r.pays ?? '',
      flag: this.flagUrl(r.pays ?? ''),
      description: r.description ?? '',
      prepTime: r.temps_preparation ?? 30,
      cookTime: r.temps_cuisson ?? 0,
      servings: r.nb_personnes ?? 4,
      difficulty: r.difficulte ?? 'Facile',
      imageUrl: r.image_url ?? '',
      ingredients: r.ingredients ?? [],
      steps: r.etapes ?? [],
      tags: r.tags ?? [],
    };
  }
}
