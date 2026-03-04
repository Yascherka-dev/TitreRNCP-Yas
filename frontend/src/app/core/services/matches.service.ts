import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Match } from '../models/fixture.model';
import { MOCK_MATCHES } from '../../features/matches/data/mock-matches';

@Injectable({ providedIn: 'root' })
export class MatchesService {
  getFixtures(): Observable<Match[]> {
    return of(MOCK_MATCHES);
  }

  getFixtureById(id: number): Observable<Match | undefined> {
    return of(MOCK_MATCHES.find(m => m.id === id));
  }
}
