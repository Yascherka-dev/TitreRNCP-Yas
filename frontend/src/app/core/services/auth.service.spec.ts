import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';
import { environment } from '../../../environments/environment';

describe('AuthService (no existing session)', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('isLoggedIn() is false when no token in localStorage', () => {
    expect(service.isLoggedIn()).toBeFalse();
  });

  it('currentUser() is null when no user in localStorage', () => {
    expect(service.currentUser()).toBeNull();
  });

  it('logout() clears signals and localStorage', () => {
    service.isLoggedIn.set(true);
    service.currentUser.set({ email: 'a@b.com', nom: 'A', prenom: 'B' });
    localStorage.setItem('access_token', 'fake');
    service.logout();
    expect(service.isLoggedIn()).toBeFalse();
    expect(service.currentUser()).toBeNull();
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('current_user')).toBeNull();
  });

  it('login() sends POST to /auth/login/ then GET to /auth/me/', () => {
    service.login('user@test.com', 'password123').subscribe();

    const loginReq = httpMock.expectOne(`${environment.apiUrl}/auth/login/`);
    expect(loginReq.request.method).toBe('POST');
    expect(loginReq.request.body).toEqual({ email: 'user@test.com', password: 'password123' });
    loginReq.flush({ access: 'access-token', refresh: 'refresh-token' });

    const meReq = httpMock.expectOne(`${environment.apiUrl}/auth/me/`);
    expect(meReq.request.method).toBe('GET');
    meReq.flush({ email: 'user@test.com', nom: 'Test', prenom: 'User' });

    expect(service.isLoggedIn()).toBeTrue();
    expect(service.currentUser()?.email).toBe('user@test.com');
    expect(service.currentUser()?.prenom).toBe('User');
    expect(localStorage.getItem('access_token')).toBe('access-token');
  });

  it('login() stores tokens in localStorage', () => {
    service.login('a@b.com', 'pass').subscribe();
    httpMock.expectOne(`${environment.apiUrl}/auth/login/`).flush({ access: 'acc', refresh: 'ref' });
    httpMock.expectOne(`${environment.apiUrl}/auth/me/`).flush({ email: 'a@b.com', nom: 'A', prenom: 'B' });
    expect(localStorage.getItem('access_token')).toBe('acc');
    expect(localStorage.getItem('refresh_token')).toBe('ref');
  });

  it('register() sends POST with all user fields', () => {
    service.register('new@test.com', 'pass123', 'Dupont', 'Jean').subscribe();
    const req = httpMock.expectOne(`${environment.apiUrl}/auth/register/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ email: 'new@test.com', password: 'pass123', nom: 'Dupont', prenom: 'Jean' });
    req.flush({ id: 1 });
  });
});

describe('AuthService (existing session)', () => {
  beforeEach(() => {
    localStorage.setItem('access_token', 'existing-token');
    TestBed.configureTestingModule({ imports: [HttpClientTestingModule] });
  });

  afterEach(() => {
    TestBed.inject(HttpTestingController).verify();
    localStorage.clear();
  });

  it('constructor makes GET /auth/me/ on startup if token present', () => {
    const service  = TestBed.inject(AuthService);
    const httpMock = TestBed.inject(HttpTestingController);

    const meReq = httpMock.expectOne(`${environment.apiUrl}/auth/me/`);
    expect(meReq.request.method).toBe('GET');
    meReq.flush({ email: 'prev@test.com', nom: 'Prev', prenom: 'User' });
    expect(service.currentUser()?.email).toBe('prev@test.com');
  });

  it('constructor sets isLoggedIn true when token present', () => {
    const service  = TestBed.inject(AuthService);
    const httpMock = TestBed.inject(HttpTestingController);
    httpMock.expectOne(`${environment.apiUrl}/auth/me/`).flush({ email: 'x@y.com', nom: 'X', prenom: 'Y' });
    expect(service.isLoggedIn()).toBeTrue();
  });
});
