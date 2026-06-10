import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FavoritesService, Favorite } from './favorites.service';
import { environment } from '../../../environments/environment';

describe('FavoritesService', () => {
  let service: FavoritesService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
    service = TestBed.inject(FavoritesService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('favorites() starts as empty array', () => {
    expect(service.favorites()).toEqual([]);
  });

  it('isFavorite() returns false for unknown item', () => {
    expect(service.isFavorite('recette', '99')).toBeFalse();
  });

  it('isFavorite() returns true after setting favorites signal', () => {
    service.favorites.set([{ id: 1, type: 'recette', reference_id: '42' }]);
    expect(service.isFavorite('recette', '42')).toBeTrue();
  });

  it('isFavorite() is type-sensitive', () => {
    service.favorites.set([{ id: 1, type: 'recette', reference_id: '42' }]);
    expect(service.isFavorite('match', '42')).toBeFalse();
  });

  it('getFavoriteId() returns the id for a known favorite', () => {
    service.favorites.set([{ id: 5, type: 'match', reference_id: 'abc' }]);
    expect(service.getFavoriteId('match', 'abc')).toBe(5);
  });

  it('getFavoriteId() returns undefined for unknown item', () => {
    expect(service.getFavoriteId('recette', '999')).toBeUndefined();
  });

  it('loadFavorites() calls GET /favorites/ and updates signal', () => {
    const mockData: Favorite[] = [
      { id: 1, type: 'recette', reference_id: '5' },
      { id: 2, type: 'match',   reference_id: 'xyz' },
    ];
    service.loadFavorites().subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/favorites/`);
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
    expect(service.favorites()).toEqual(mockData);
  });

  it('addFavorite() sends POST and appends result to signal', () => {
    const existing: Favorite = { id: 1, type: 'recette', reference_id: '5' };
    service.favorites.set([existing]);
    const newFav: Favorite = { id: 10, type: 'match', reference_id: 'new-id' };

    service.addFavorite('match', 'new-id').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/favorites/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ type: 'match', reference_id: 'new-id' });
    req.flush(newFav);

    expect(service.favorites().length).toBe(2);
    expect(service.favorites()[1].reference_id).toBe('new-id');
  });

  it('removeFavorite() sends DELETE and removes from signal', () => {
    service.favorites.set([
      { id: 3, type: 'recette', reference_id: '9' },
      { id: 4, type: 'match',   reference_id: 'xyz' },
    ]);
    service.removeFavorite(3).subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/favorites/3/`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
    expect(service.favorites().length).toBe(1);
    expect(service.favorites()[0].id).toBe(4);
  });
});
