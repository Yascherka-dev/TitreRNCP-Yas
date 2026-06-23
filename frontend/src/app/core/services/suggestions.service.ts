import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, tap, map } from 'rxjs';
import { Beer, MatchSuggestion, Recipe } from '../models/recipe.model';
import { environment } from '../../../environments/environment';
import { flagUrl } from '../utils/flag.utils';

interface RawRecipe {
  id: number;
  titre: string;
  pays: string;
  region: string;
  equipe: string;
  type_plat: string;
  description: string;
  temps_preparation: number;
  temps_cuisson: number;
  nb_personnes: number;
  difficulte: string;
  image_url: string;
  ingredients: string[];
  etapes: string[];
  tags: string[];
}

interface RawBeer {
  id: number;
  nom: string;
  brasserie: string;
  pays: string;
  region: string;
  equipe: string;
  style: string;
  description: string;
  degre_alcool: string | null;
  image_url: string;
}

interface RawSuggestionResponse {
  recette_a: RawRecipe | null;
  recette_b: RawRecipe | null;
  peche_mignon_a: RawRecipe | null;
  peche_mignon_b: RawRecipe | null;
  biere_a: RawBeer | null;
  biere_b: RawBeer | null;
}

@Injectable({ providedIn: 'root' })
export class SuggestionsService {
  private http    = inject(HttpClient);
  private apiUrl  = environment.apiUrl;
  private cache   = new Map<string, MatchSuggestion>();

  getSuggestion(
    matchId: number | string,
    paysA: string, paysB: string,
    equipeA = '', equipeB = '',
  ): Observable<MatchSuggestion> {
    const key = `${matchId}`;
    if (this.cache.has(key)) return of(this.cache.get(key)!);
    return this.fetch(matchId, paysA, paysB, equipeA, equipeB);
  }

  regenerate(
    matchId: number | string,
    paysA: string, paysB: string,
    equipeA = '', equipeB = '',
  ): Observable<MatchSuggestion> {
    this.cache.delete(`${matchId}`);
    return this.fetch(matchId, paysA, paysB, equipeA, equipeB);
  }

  private fetch(
    matchId: number | string,
    paysA: string, paysB: string,
    equipeA: string, equipeB: string,
  ): Observable<MatchSuggestion> {
    return this.http
      .post<RawSuggestionResponse>(`${this.apiUrl}/suggestions/`, { paysA, paysB, equipeA, equipeB })
      .pipe(
        map(res => ({
          matchId:      String(matchId),
          recetteA:     res.recette_a     ? this.toRecipe(res.recette_a)     : null,
          recetteB:     res.recette_b     ? this.toRecipe(res.recette_b)     : null,
          pecheMignonA: res.peche_mignon_a ? this.toRecipe(res.peche_mignon_a) : null,
          pecheMignonB: res.peche_mignon_b ? this.toRecipe(res.peche_mignon_b) : null,
          biereA:       res.biere_a       ? this.toBeer(res.biere_a)         : null,
          biereB:       res.biere_b       ? this.toBeer(res.biere_b)         : null,
          generatedAt:  new Date(),
        } satisfies MatchSuggestion)),
        tap(s => this.cache.set(`${matchId}`, s)),
      );
  }

  private toRecipe(r: RawRecipe): Recipe {
    return {
      id:          String(r.id ?? ''),
      title:       r.titre ?? '',
      country:     r.pays ?? '',
      countryCode: r.pays ?? '',
      region:      r.region ?? '',
      equipe:      r.equipe ?? '',
      typePlat:    (r.type_plat ?? 'salé') as 'salé' | 'sucré',
      flag:        flagUrl(r.pays ?? ''),
      description: r.description ?? '',
      prepTime:    r.temps_preparation ?? 30,
      cookTime:    r.temps_cuisson ?? 0,
      servings:    r.nb_personnes ?? 4,
      difficulty:  (r.difficulte ?? 'Facile') as 'Facile' | 'Moyen' | 'Difficile',
      imageUrl:    r.image_url ?? '',
      ingredients: r.ingredients ?? [],
      steps:       r.etapes ?? [],
      tags:        r.tags ?? [],
    };
  }

  private toBeer(b: RawBeer): Beer {
    return {
      id:          String(b.id ?? ''),
      nom:         b.nom ?? '',
      brasserie:   b.brasserie ?? '',
      pays:        b.pays ?? '',
      region:      b.region ?? '',
      equipe:      b.equipe ?? '',
      style:       b.style ?? '',
      description: b.description ?? '',
      degreAlcool: b.degre_alcool ?? null,
      imageUrl:    b.image_url ?? '',
    };
  }
}
