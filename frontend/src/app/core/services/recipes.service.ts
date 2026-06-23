import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Recipe } from '../models/recipe.model';
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

@Injectable({ providedIn: 'root' })
export class RecipesService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  getAll(): Observable<Recipe[]> {
    return this.http
      .get<RawRecipe[]>(`${this.apiUrl}/recipes/`)
      .pipe(map(items => items.map(r => this.toRecipe(r))));
  }

  private toRecipe(r: RawRecipe): Recipe {
    return {
      id:          String(r.id),
      title:       r.titre ?? '',
      country:     this.countryNames[r.pays?.toLowerCase()] ?? r.pays ?? '',
      countryCode: r.pays ?? '',
      region:      r.region ?? '',
      equipe:      r.equipe ?? '',
      typePlat:    (r.type_plat ?? 'salé') as 'salé' | 'sucré',
      flag:        flagUrl(r.pays ?? ''),
      description: r.description ?? '',
      prepTime:    r.temps_preparation ?? 0,
      cookTime:    r.temps_cuisson ?? 0,
      servings:    r.nb_personnes ?? 4,
      difficulty:  (r.difficulte ?? 'Facile') as 'Facile' | 'Moyen' | 'Difficile',
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
