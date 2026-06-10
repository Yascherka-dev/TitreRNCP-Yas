import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { MatchesService } from './matches.service';
import { environment } from '../../../environments/environment';

const RAW_MATCH = {
  id: 1,
  date_heure: '2026-06-15T20:00:00Z',
  sport: 'football',
  statut: 'NS',
  competition: 'Ligue 1',
  league_id: 4334,
  equipe_a: 'PSG',
  equipe_b: 'Marseille',
  pays_a: 'france',
  pays_b: 'france',
  logo_a: '',
  logo_b: '',
  score_a: null,
  score_b: null,
  venue: 'Parc des Princes',
  thumb_url: '',
};

describe('MatchesService', () => {
  let service: MatchesService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
    service = TestBed.inject(MatchesService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('getFixtures() maps raw API response to Match objects', () => {
    let matches: any[] = [];
    service.getFixtures().subscribe(m => (matches = m));
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
    expect(matches.length).toBe(1);
    expect(matches[0].id).toBe('1');
    expect(matches[0].home.name).toBe('PSG');
    expect(matches[0].away.name).toBe('Marseille');
    expect(matches[0].sport).toBe('football');
  });

  it('getFixtures() translates pays_a to French country name', () => {
    let matches: any[] = [];
    service.getFixtures().subscribe(m => (matches = m));
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
    expect(matches[0].home.countryName).toBe('France');
  });

  it('getFixtures() maps status correctly', () => {
    let matches: any[] = [];
    service.getFixtures().subscribe(m => (matches = m));
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
    expect(matches[0].status.short).toBe('NS');
  });

  it('getFixtures() sets score to null for unplayed match', () => {
    let matches: any[] = [];
    service.getFixtures().subscribe(m => (matches = m));
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
    expect(matches[0].home.goals).toBeNull();
    expect(matches[0].away.goals).toBeNull();
  });

  it('getFixtureById() finds match by id', (done) => {
    service.getFixtureById('1').subscribe(match => {
      expect(match).toBeDefined();
      expect(match?.id).toBe('1');
      expect(match?.home.name).toBe('PSG');
      done();
    });
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
  });

  it('getFixtureById() returns undefined for unknown id', (done) => {
    service.getFixtureById('999').subscribe(match => {
      expect(match).toBeUndefined();
      done();
    });
    httpMock.expectOne(`${environment.apiUrl}/matches/`).flush([RAW_MATCH]);
  });

  it('getFixturesByDate() sends GET with date param', () => {
    let matches: any[] = [];
    service.getFixturesByDate('2026-06-15').subscribe(m => (matches = m));
    const req = httpMock.expectOne(`${environment.apiUrl}/matches/?date=2026-06-15`);
    expect(req.request.method).toBe('GET');
    req.flush([RAW_MATCH]);
    expect(matches.length).toBe(1);
  });

  it('getFixturesBySport() sends GET with sport param', () => {
    service.getFixturesBySport('basketball').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/matches/?sport=basketball`);
    expect(req.request.method).toBe('GET');
    req.flush([]);
  });
});
