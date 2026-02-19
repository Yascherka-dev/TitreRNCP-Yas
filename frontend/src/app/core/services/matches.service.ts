import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Match } from '../models/fixture.model';
import { MOCK_MATCHES } from '../../features/matches/data/mock-matches';

@Injectable({ providedIn: 'root' })
export class MatchesService {

  getFixtures(): Observable<Match[]> {
    // Données mockées — à remplacer par l'appel API via le backend NestJS
    return of(MOCK_MATCHES);
  }

  getFixtureById(id: number): Observable<Match | undefined> {
    const match = MOCK_MATCHES.find(m => m.id === id);
    return of(match);
  }
}
