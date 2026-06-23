import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, shareReplay } from 'rxjs';
import { Match } from '../models/fixture.model';
import { environment } from '../../../environments/environment';
import { flagUrl } from '../utils/flag.utils';

interface RawMatch {
  id: number;
  date_heure: string;
  sport: string;
  statut: string;
  competition: string;
  league_id: number;
  equipe_a: string;
  equipe_b: string;
  pays_a: string;
  pays_b: string;
  logo_a: string;
  logo_b: string;
  score_a: number | null;
  score_b: number | null;
  venue: string;
  thumb_url: string;
}

// TheSportsDB league badge URLs (keyed by league ID)
const LEAGUE_BADGES: Record<number, string> = {
  4334: 'https://r2.thesportsdb.com/images/media/league/badge/9f7z9d1742983155.png',  // Ligue 1
  4480: 'https://r2.thesportsdb.com/images/media/league/badge/facv1u1742998896.png',  // UCL
  4429: 'https://r2.thesportsdb.com/images/media/league/badge/e7er5g1696521789.png',  // WC 2026
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
    .get<RawMatch[]>(`${this.apiUrl}/matches/`)
    .pipe(map(items => items.map(this.toMatch)), shareReplay(1));

  getFixtures(): Observable<Match[]> {
    return this.fixtures$;
  }

  getFixturesByDate(date: string): Observable<Match[]> {
    return this.http
      .get<RawMatch[]>(`${this.apiUrl}/matches/?date=${date}`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  getFixturesBySport(sport: string): Observable<Match[]> {
    return this.http
      .get<RawMatch[]>(`${this.apiUrl}/matches/?sport=${sport}`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  getFixtureById(id: string | number): Observable<Match | undefined> {
    return this.getFixtures().pipe(
      map(matches => matches.find(m => String(m.id) === String(id)))
    );
  }

  getLivescores(): Observable<Match[]> {
    return this.http
      .get<RawMatch[]>(`${this.apiUrl}/matches/livescores/`)
      .pipe(map(items => items.map(this.toMatch)));
  }

  private leagueBadge(leagueId: number): string {
    return LEAGUE_BADGES[leagueId] ?? '';
  }

  private readonly COUNTRY_LABELS: Record<string, string> = {
    // Europe ouest
    france: 'France', england: 'Angleterre', spain: 'Espagne',
    germany: 'Allemagne', italy: 'Italie', portugal: 'Portugal',
    netherlands: 'Pays-Bas', belgium: 'Belgique', scotland: 'Écosse',
    wales: 'Pays de Galles', austria: 'Autriche', switzerland: 'Suisse',
    denmark: 'Danemark', sweden: 'Suède', norway: 'Norvège', finland: 'Finlande',
    ireland: 'Irlande', luxembourg: 'Luxembourg', iceland: 'Islande',
    andorra: 'Andorre', 'san marino': 'Saint-Marin', malta: 'Malte',
    gibraltar: 'Gibraltar', 'faroe islands': 'Îles Féroé',
    // Europe centre/est
    croatia: 'Croatie', serbia: 'Serbie', poland: 'Pologne',
    ukraine: 'Ukraine', hungary: 'Hongrie', romania: 'Roumanie',
    'czech republic': 'Tchéquie', czechia: 'Tchéquie', slovakia: 'Slovaquie',
    slovenia: 'Slovénie', bulgaria: 'Bulgarie', greece: 'Grèce',
    albania: 'Albanie', georgia: 'Géorgie', turkey: 'Turquie',
    'bosnia and herzegovina': 'Bosnie', 'north macedonia': 'Macédoine du Nord',
    macedonia: 'Macédoine', kosovo: 'Kosovo',
    montenegro: 'Monténégro', moldova: 'Moldavie', belarus: 'Biélorussie',
    russia: 'Russie', latvia: 'Lettonie', lithuania: 'Lituanie', estonia: 'Estonie',
    // Amériques
    usa: 'USA', 'united states': 'USA', canada: 'Canada',
    brazil: 'Brésil', argentina: 'Argentine', mexico: 'Mexique',
    colombia: 'Colombie', chile: 'Chili', uruguay: 'Uruguay',
    ecuador: 'Équateur', venezuela: 'Venezuela', peru: 'Pérou',
    panama: 'Panama', 'costa rica': 'Costa Rica', honduras: 'Honduras',
    jamaica: 'Jamaïque', 'el salvador': 'El Salvador', paraguay: 'Paraguay',
    bolivia: 'Bolivie', 'trinidad and tobago': 'Trinidad',
    // Afrique
    morocco: 'Maroc', senegal: 'Sénégal', nigeria: 'Nigéria',
    ghana: 'Ghana', egypt: 'Égypte', 'ivory coast': "Côte d'Ivoire",
    cameroon: 'Cameroun', 'south africa': 'Afrique du Sud',
    algeria: 'Algérie', tunisia: 'Tunisie', mali: 'Mali',
    'dr congo': 'RD Congo', congo: 'Congo', ethiopia: 'Éthiopie',
    // Asie / Océanie
    japan: 'Japon', 'south korea': 'Corée du Sud', 'korea republic': 'Corée du Sud',
    china: 'Chine', australia: 'Australie', 'saudi arabia': 'Arabie Saoudite',
    iran: 'Iran', 'ir iran': 'Iran', qatar: 'Qatar',
    uzbekistan: 'Ouzbékistan', jordan: 'Jordanie', indonesia: 'Indonésie',
    'new zealand': 'Nouvelle-Zélande', iraq: 'Irak', syria: 'Syrie',
  };

  private countryLabel(pays: string): string {
    return this.COUNTRY_LABELS[pays.toLowerCase()]
      ?? pays.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  private teamName(equipe: string): string {
    return this.COUNTRY_LABELS[equipe.toLowerCase()] ?? equipe;
  }

  private toMatch = (item: RawMatch): Match => {
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
        name:        this.teamName(item.equipe_a ?? ''),
        logo:        item.logo_a ?? '',
        countryCode: item.pays_a ?? '',
        countryName: this.countryLabel(item.pays_a ?? ''),
        flag:        flagUrl(item.pays_a ?? ''),
        goals:       item.score_a ?? null,
        winner:      null,
      },
      away: {
        id:          0,
        name:        this.teamName(item.equipe_b ?? ''),
        logo:        item.logo_b ?? '',
        countryCode: item.pays_b ?? '',
        countryName: this.countryLabel(item.pays_b ?? ''),
        flag:        flagUrl(item.pays_b ?? ''),
        goals:       item.score_b ?? null,
        winner:      null,
      },
      venue:    item.venue ?? '',
      thumbUrl: item.thumb_url ?? '',
    };
  };
}
