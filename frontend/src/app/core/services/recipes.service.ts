import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Recipe } from '../models/recipe.model';
import { environment } from '../../../environments/environment';



@Injectable({ providedIn: 'root' })
export class RecipesService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  getAll(): Observable<Recipe[]> {
    return this.http
      .get<any[]>(`${this.apiUrl}/recipes/`)
      .pipe(map(items => items.map(r => this.toRecipe(r))));
  }

  private toRecipe(r: any): Recipe {
    return {
      id:          String(r.id),
      title:       r.titre ?? '',
      country: this.countryNames[r.pays?.toLowerCase()] ?? r.pays ?? '',
      countryCode: r.pays ?? '',
      flag:        '',
      description: r.description ?? '',
      prepTime:    r.temps_preparation ?? 0,
      cookTime:    r.temps_cuisson ?? 0,
      servings:    r.nb_personnes ?? 4,
      difficulty:  r.difficulte ?? 'Facile',
      imageUrl:    r.image_url ?? '',
      ingredients: r.ingredients ?? [],
      steps:       r.etapes ?? [],
      tags:        r.tags ?? [],
    };
  }

  private countryNames: Record<string, string> = {
  france: 'France',
  spain: 'Espagne',
  italy: 'Italie',
  england: 'Angleterre',
  germany: 'Allemagne',
  portugal: 'Portugal',
  netherlands: 'Pays-Bas',
  belgium: 'Belgique',
  morocco: 'Maroc',
  argentina: 'Argentine',
  brazil: 'Brésil',
};

}
