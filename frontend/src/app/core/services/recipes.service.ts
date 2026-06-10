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
      country:     this.countryNames[r.pays?.toLowerCase()] ?? r.pays ?? '',
      countryCode: r.pays ?? '',
      region:      r.region ?? '',
      equipe:      r.equipe ?? '',
      typePlat:    r.type_plat ?? 'salé',
      flag:        this.flagUrl(r.pays ?? ''),
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

  private flagUrl(pays: string): string {
    const ISO: Record<string, string> = {
      france: 'fr', spain: 'es', italy: 'it', england: 'gb-eng',
      germany: 'de', portugal: 'pt', netherlands: 'nl', belgium: 'be',
      scotland: 'gb-sct', wales: 'gb-wls', switzerland: 'ch', austria: 'at',
      denmark: 'dk', sweden: 'se', norway: 'no', ireland: 'ie',
      croatia: 'hr', poland: 'pl', czechia: 'cz', 'czech republic': 'cz',
      hungary: 'hu', ukraine: 'ua', turkey: 'tr', greece: 'gr',
      russia: 'ru', romania: 'ro', serbia: 'rs', bulgaria: 'bg',
      morocco: 'ma', senegal: 'sn', nigeria: 'ng', ghana: 'gh',
      egypt: 'eg', algeria: 'dz', tunisia: 'tn', cameroon: 'cm',
      'ivory coast': 'ci', "côte d'ivoire": 'ci', 'south africa': 'za',
      brazil: 'br', argentina: 'ar', mexico: 'mx', colombia: 'co',
      chile: 'cl', uruguay: 'uy', usa: 'us', 'united states': 'us',
      canada: 'ca', japan: 'jp', 'south korea': 'kr', china: 'cn',
      australia: 'au', 'saudi arabia': 'sa', qatar: 'qa',
    };
    const code = ISO[pays.toLowerCase()] ?? pays.toLowerCase();
    return code ? `https://flagcdn.com/w40/${code}.png` : '';
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
