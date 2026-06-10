import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, shareReplay } from 'rxjs';
import { Match } from '../models/fixture.model';
import { environment } from '../../../environments/environment';

// TheSportsDB league badge URLs (keyed by league ID)
const LEAGUE_BADGES: Record<number, string> = {
  4334: 'https://r2.thesportsdb.com/images/media/league/badge/9f7z9d1742983155.png',  // Ligue 1
  4480: 'https://r2.thesportsdb.com/images/media/league/badge/facv1u1742998896.png',  // UCL
  4387: 'https://r2.thesportsdb.com/images/media/league/badge/frdjqy1536585083.png',  // NBA
  4391: 'https://r2.thesportsdb.com/images/media/league/badge/g85fqz1662057187.png',  // NFL
  4380: 'https://r2.thesportsdb.com/images/media/league/badge/4cem2k1619616539.png',  // NHL
  4430: 'https://r2.thesportsdb.com/images/media/league/badge/xrsqtw1452903237.png',  // Top 14
  4714: 'https://r2.thesportsdb.com/images/media/league/badge/7h1wr91738670253.png',  // Six Nations
};

@Injectable({ providedIn: 'root' })
export class MatchesService {
  private http    = inject(HttpClient);
  private apiUrl  = environment.apiUrl;

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

  getFixturesBySport(sport: string): Observable<Match[]> {
    return this.http
      .get<any[]>(`${this.apiUrl}/matches/?sport=${sport}`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  getFixtureById(id: string | number): Observable<Match | undefined> {
    return this.getFixtures().pipe(
      map(matches => matches.find(m => String(m.id) === String(id)))
    );
  }

  getLivescores(): Observable<Match[]> {
    return this.http
      .get<any[]>(`${this.apiUrl}/matches/livescores/`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  private leagueBadge(leagueId: number): string {
    return LEAGUE_BADGES[leagueId] ?? '';
  }

  private countryLabel(pays: string): string {
    const labels: Record<string, string> = {
      france: 'France', england: 'Angleterre', spain: 'Espagne',
      germany: 'Allemagne', italy: 'Italie', portugal: 'Portugal',
      netherlands: 'Pays-Bas', belgium: 'Belgique', scotland: 'Écosse',
      usa: 'USA', 'united states': 'USA', canada: 'Canada',
      brazil: 'Brésil', argentina: 'Argentine', mexico: 'Mexique',
      japan: 'Japon', 'south korea': 'Corée du Sud', australia: 'Australie',
      morocco: 'Maroc', senegal: 'Sénégal', 'ivory coast': "Côte d'Ivoire",
      turkey: 'Turquie', switzerland: 'Suisse', denmark: 'Danemark',
      sweden: 'Suède', croatia: 'Croatie', ukraine: 'Ukraine',
      poland: 'Pologne', 'czech republic': 'Tchéquie', czechia: 'Tchéquie',
    };
    return labels[pays.toLowerCase()] ?? pays.charAt(0).toUpperCase() + pays.slice(1);
  }

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
      'the netherlands':          'nl',
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
      'north macedonia':          'mk',
      'montenegro':               'me',
      'albania':                  'al',
      'ukraine':                  'ua',
      'russia':                   'ru',
      'latvia':                   'lv',
      'lithuania':                'lt',
      'estonia':                  'ee',
      'cyprus':                   'cy',
      'greece':                   'gr',
      'turkey':                   'tr',
      'israel':                   'il',
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
      'china':                    'cn',
      'australia':                'au',
      'saudi arabia':             'sa',
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
    const leagueId: number = item.league_id ?? 0;
    return {
      id:      String(item.id),
      date:    new Date(item.date_heure),
      sport:   item.sport ?? 'football',
      status: {
        short:   item.statut ?? 'NS',
        long:    item.statut ?? 'NS',
        elapsed: null,
      },
      league: {
        id:       leagueId,
        leagueId: leagueId,
        name:     item.competition ?? '',
        country:  '',
        logo:     this.leagueBadge(leagueId),
        round:    '',
      },
      home: {
        id:          0,
        name:        item.equipe_a ?? '',
        logo:        item.logo_a ?? '',
        countryCode: item.pays_a ?? '',
        countryName: this.countryLabel(item.pays_a ?? ''),
        flag:        this.flagUrl(item.pays_a ?? ''),
        goals:       item.score_a ?? null,
        winner:      null,
      },
      away: {
        id:          0,
        name:        item.equipe_b ?? '',
        logo:        item.logo_b ?? '',
        countryCode: item.pays_b ?? '',
        countryName: this.countryLabel(item.pays_b ?? ''),
        flag:        this.flagUrl(item.pays_b ?? ''),
        goals:       item.score_b ?? null,
        winner:      null,
      },
      venue:    item.venue ?? '',
      thumbUrl: item.thumb_url ?? '',
    };
  };
}
