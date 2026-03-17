import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Match } from '../models/fixture.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MatchesService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  getFixtures(): Observable<Match[]> {
    return this.http
      .get<any[]>(`${this.apiUrl}/matches/`)
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
      'france':         'fr',
      'england':        'gb-eng',
      'germany':        'de',
      'spain':          'es',
      'italy':          'it',
      'portugal':       'pt',
      'netherlands':    'nl',
      'belgium':        'be',
      'norway':         'no',
      'scotland':       'gb-sct',
      'austria':        'at',
      'switzerland':    'ch',
      'denmark':        'dk',
      'sweden':         'se',
      'czechia':        'cz',
      'czech republic': 'cz',
      'slovakia':       'sk',
      'poland':         'pl',
      'ukraine':        'ua',
      'turkey':         'tr',
      'greece':         'gr',
      'croatia':        'hr',
      'serbia':         'rs',
      'romania':        'ro',
      'hungary':        'hu',
      'russia':         'ru',
      'israel':         'il',
      'monaco':         'mc',
      'azerbaijan':     'az',
      'europe':         'eu',
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
