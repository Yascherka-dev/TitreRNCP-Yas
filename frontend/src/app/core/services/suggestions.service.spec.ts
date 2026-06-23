import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SuggestionsService } from './suggestions.service';
import { flagUrl } from '../utils/flag.utils';
import { environment } from '../../../environments/environment';

const RAW_RECIPE = {
  id: 1, titre: 'Boeuf bourguignon', pays: 'france', region: '', equipe: '',
  type_plat: 'salé', description: 'Un classique.', temps_preparation: 30,
  temps_cuisson: 120, nb_personnes: 4, difficulte: 'Moyen',
  image_url: '', ingredients: ['boeuf', 'vin'], etapes: ['Cuire', 'Servir'], tags: ['boeuf'],
};
const RAW_BEER = {
  id: 1, nom: 'Kronenbourg', brasserie: 'SAS', pays: 'france', region: '', equipe: '',
  style: 'Lager', description: 'Bière française.', degre_alcool: '5.0', image_url: '',
};
const MOCK_RESPONSE = {
  recette_a:      RAW_RECIPE,
  recette_b:      { ...RAW_RECIPE, id: 2, titre: 'Paella', pays: 'spain' },
  peche_mignon_a: null,
  peche_mignon_b: null,
  biere_a:        RAW_BEER,
  biere_b:        null,
};

describe('SuggestionsService', () => {
  let service: SuggestionsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
    service = TestBed.inject(SuggestionsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('getSuggestion() sends POST to /suggestions/', () => {
    service.getSuggestion('1', 'france', 'spain').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/suggestions/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ paysA: 'france', paysB: 'spain', equipeA: '', equipeB: '' });
    req.flush(MOCK_RESPONSE);
  });

  it('getSuggestion() maps recetteA title correctly', () => {
    let result: any;
    service.getSuggestion('1', 'france', 'spain').subscribe(s => (result = s));
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);
    expect(result.recetteA?.title).toBe('Boeuf bourguignon');
    expect(result.recetteB?.title).toBe('Paella');
  });

  it('getSuggestion() maps biereA correctly', () => {
    let result: any;
    service.getSuggestion('1', 'france', 'spain').subscribe(s => (result = s));
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);
    expect(result.biereA?.nom).toBe('Kronenbourg');
    expect(result.biereB).toBeNull();
  });

  it('getSuggestion() null peche_mignon becomes null pecheMignonA', () => {
    let result: any;
    service.getSuggestion('1', 'france', 'spain').subscribe(s => (result = s));
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);
    expect(result.pecheMignonA).toBeNull();
    expect(result.pecheMignonB).toBeNull();
  });

  it('getSuggestion() uses in-memory cache on second call with same matchId', () => {
    service.getSuggestion('2', 'france', 'spain').subscribe();
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);

    let cached: any;
    service.getSuggestion('2', 'france', 'spain').subscribe(s => (cached = s));
    httpMock.expectNone(`${environment.apiUrl}/suggestions/`);
    expect(cached).toBeDefined();
    expect(cached.matchId).toBe('2');
  });

  it('getSuggestion() does NOT use cache for different matchId', () => {
    service.getSuggestion('3', 'france', 'spain').subscribe();
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);

    service.getSuggestion('4', 'france', 'spain').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/suggestions/`);
    expect(req.request.method).toBe('POST');
    req.flush(MOCK_RESPONSE);
  });

  it('regenerate() bypasses cache and sends fresh POST', () => {
    service.getSuggestion('5', 'france', 'spain').subscribe();
    httpMock.expectOne(`${environment.apiUrl}/suggestions/`).flush(MOCK_RESPONSE);
    service.regenerate('5', 'france', 'spain').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/suggestions/`);
    expect(req.request.method).toBe('POST');
    req.flush(MOCK_RESPONSE);
  });

  it('flagUrl() returns a flagcdn URL for known countries', () => {
    expect(flagUrl('france')).toContain('fr');
    expect(flagUrl('spain')).toContain('es');
  });
});
