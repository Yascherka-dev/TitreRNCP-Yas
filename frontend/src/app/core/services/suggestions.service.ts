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

  getSuggestion(matchId: number | string, paysA: string, paysB: string, equipeA = '', equipeB = ''): Observable<MatchSuggestion> {
    const key = `${matchId}`;
    if (this.cache.has(key)) return of(this.cache.get(key)!);
    return this.fetch(matchId, paysA, paysB, equipeA, equipeB);
  }

  regenerate(matchId: number | string, paysA: string, paysB: string, equipeA = '', equipeB = ''): Observable<MatchSuggestion> {
    this.cache.delete(`${matchId}`);
    return this.fetch(matchId, paysA, paysB, equipeA, equipeB);
  }

  private fetch(matchId: number | string, paysA: string, paysB: string, equipeA: string, equipeB: string): Observable<MatchSuggestion> {
    return this.http
      .post<{ recettes: any[] }>(`${this.apiUrl}/suggestions/`, { paysA, paysB, equipeA, equipeB })
      .pipe(
        map(res => ({
          matchId: String(matchId),
          recipeA: this.toRecipe(res.recettes[0]),
          recipeB: this.toRecipe(res.recettes[1]),
          generatedAt: new Date(),
        })),
        tap(s => this.cache.set(`${matchId}`, s))
      );
  }

  private flagUrl(pays: string): string {
    const map: Record<string, string> = {
      // Europe occidentale
      'france':                   'fr',
      'england':                  'gb-eng',
      'scotland':                 'gb-sct',
      'wales':                    'gb-wls',
      'northern ireland':         'gb-nir',
      'germany':                  'de',
      'spain':                    'es',
      'italy':                    'it',
      'portugal':                 'pt',
      'netherlands':              'nl',
      'belgium':                  'be',
      'austria':                  'at',
      'switzerland':              'ch',
      'denmark':                  'dk',
      'sweden':                   'se',
      'norway':                   'no',
      'finland':                  'fi',
      'ireland':                  'ie',
      'luxembourg':               'lu',
      'monaco':                   'mc',
      'liechtenstein':            'li',
      'malta':                    'mt',
      'san marino':               'sm',
      'andorra':                  'ad',
      'iceland':                  'is',
      // Europe centrale et orientale
      'czechia':                  'cz',
      'czech republic':           'cz',
      'slovakia':                 'sk',
      'poland':                   'pl',
      'hungary':                  'hu',
      'romania':                  'ro',
      'bulgaria':                 'bg',
      'slovenia':                 'si',
      'croatia':                  'hr',
      'serbia':                   'rs',
      'bosnia and herzegovina':   'ba',
      'bosnia & herzegovina':     'ba',
      'north macedonia':          'mk',
      'macedonia':                'mk',
      'montenegro':               'me',
      'albania':                  'al',
      'kosovo':                   'xk',
      'moldova':                  'md',
      'ukraine':                  'ua',
      'belarus':                  'by',
      'russia':                   'ru',
      'latvia':                   'lv',
      'lithuania':                'lt',
      'estonia':                  'ee',
      'cyprus':                   'cy',
      'greece':                   'gr',
      'israel':                   'il',
      'turkey':                   'tr',
      'azerbaijan':               'az',
      'armenia':                  'am',
      'georgia':                  'ge',
      // Amérique
      'brazil':                   'br',
      'argentina':                'ar',
      'colombia':                 'co',
      'chile':                    'cl',
      'uruguay':                  'uy',
      'mexico':                   'mx',
      'usa':                      'us',
      'united states':            'us',
      'canada':                   'ca',
      // Afrique
      'morocco':                  'ma',
      'senegal':                  'sn',
      'nigeria':                  'ng',
      'ghana':                    'gh',
      'egypt':                    'eg',
      'ivory coast':              'ci',
      "côte d'ivoire":            'ci',
      'cameroon':                 'cm',
      'south africa':             'za',
      'algeria':                  'dz',
      'tunisia':                  'tn',
      // Asie / Océanie
      'japan':                    'jp',
      'south korea':              'kr',
      'korea republic':           'kr',
      'china':                    'cn',
      'australia':                'au',
      'saudi arabia':             'sa',
      'iran':                     'ir',
      'qatar':                    'qa',
    };
    const code = map[pays.toLowerCase()] ?? pays.toLowerCase();
    return `https://flagcdn.com/w40/${code}.png`;
  }

  private toRecipe(r: any): Recipe {
    return {
      id: String(r.id ?? ''),
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
