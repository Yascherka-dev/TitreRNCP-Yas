import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, shareReplay } from 'rxjs';
import { Match } from '../models/fixture.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MatchesService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  private fixtures$ = this.http
    .get<any[]>(`${this.apiUrl}/matches/`)
    .pipe(map(items => items.map(this.toMatch)), shareReplay(1));

  getFixtures(): Observable<Match[]> {
    return this.fixtures$;
  }

  getFixturesByDate(date: string): Observable<Match[]> {
    return this.http
      .get<any[]>(`${this.apiUrl}/matches/?date=${date}`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  getFixtureById(id: string | number): Observable<Match | undefined> {
    return this.getFixtures().pipe(
      map(matches => matches.find(m => String(m.id) === String(id)))
    );
  }

  private hashString(s: string): number {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (Math.imul(31, h) + s.charCodeAt(i)) | 0;
    return Math.abs(h);
  }

  // Traduit les statuts de football-data.org vers les codes attendus par le composant
  private mapStatus(statut: string): string {
    const map: Record<string, string> = {
      'FINISHED':  'FT',
      'IN_PLAY':   'LIVE',
      'PAUSED':    'HT',
      'HALFTIME':  'HT',
      'SCHEDULED': 'NS',
      'TIMED':     'NS',
      'POSTPONED': 'PST',
      'CANCELLED': 'CANC',
    };
    return map[statut] ?? 'NS';
  }

  // Retourne le logo de la compétition depuis football-data.org
  private competitionLogo(name: string): string {
    const map: Record<string, string> = {
      'Ligue 1':        'https://crests.football-data.org/FL1.png',
      'Premier League': 'https://crests.football-data.org/PL.png',
      'La Liga':        'https://crests.football-data.org/PD.png',
      'Bundesliga':     'https://crests.football-data.org/BL1.png',
      'Serie A':        'https://crests.football-data.org/SA.png',
      'UEFA Champions League': 'https://crests.football-data.org/CL.png',
    };
    return map[name] ?? '';
  }

  // Génère une URL de drapeau à partir du nom de pays (ex: "france" → drapeau FR)
  private flagUrl(countryName: string): string {
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
      // Moyen-Orient / Asie occidentale
      'turkey':                   'tr',
      'israel':                   'il',
      'palestine':                'ps',
      'azerbaijan':               'az',
      'armenia':                  'am',
      'georgia':                  'ge',
      'kazakhstan':               'kz',
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
      'united arab emirates':     'ae',
      // Divers
      'europe':                   'eu',
      'world':                    'un',
    };
    const code = map[countryName.toLowerCase()] ?? countryName.toLowerCase();
    return `https://flagcdn.com/w40/${code}.png`;
  }

  private toMatch = (item: any): Match => {
    return {
      id: item.id,
      date: new Date(item.date_heure),
      sport: item.sport ?? 'football',
      status: { short: this.mapStatus(item.statut ?? 'NS'), long: item.statut ?? 'Not Started', elapsed: null },
      league: { id: this.hashString(item.competition ?? ''), name: item.competition ?? '', country: '', logo: this.competitionLogo(item.competition ?? ''), round: '' },
      home: {
        id: 0,
        name: item.equipe_a ?? '',
        logo: item.logo_a ?? '',
        countryCode: item.pays_a ?? '',
        countryName: item.pays_a ?? '',
        flag: this.flagUrl(item.pays_a ?? ''),
        goals: item.score_a ?? null,
        winner: null,
      },
      away: {
        id: 0,
        name: item.equipe_b ?? '',
        logo: item.logo_b ?? '',
        countryCode: item.pays_b ?? '',
        countryName: item.pays_b ?? '',
        flag: this.flagUrl(item.pays_b ?? ''),
        goals: item.score_b ?? null,
        winner: null,
      },
    };
  };
}
