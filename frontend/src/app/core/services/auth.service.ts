import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { switchMap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // Au démarrage : vérifie si un token existe déjà (session précédente)
  isLoggedIn = signal<boolean>(!!localStorage.getItem('access_token'));
  
  refreshToken() {
  const refresh = localStorage.getItem('refresh_token');
  return this.http
    .post<{ access: string }>(`${this.apiUrl}/auth/token/refresh/`, { refresh })
    .pipe(tap(res => localStorage.setItem('access_token', res.access)));
}


  currentUser = signal<{ email: string; nom: string; prenom: string } | null>(null);

  constructor() {
    if (this.isLoggedIn()) {
      this.http.get<{ email: string; nom: string; prenom: string }>(
        `${this.apiUrl}/auth/me/`
      ).subscribe(user => this.currentUser.set(user));
    }
  }
login(email: string, password: string) {
  return this.http
    .post<{ access: string; refresh: string }>(
      `${this.apiUrl}/auth/login/`, { email, password }
    )
    .pipe(
      tap(res => {
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);
        this.isLoggedIn.set(true);
      }),
      switchMap(() =>
        this.http.get<{ email: string; nom: string; prenom: string }>(
          `${this.apiUrl}/auth/me/`
        )
      ),
      tap(user => {
        this.currentUser.set(user);
      })
    );
}

  register(email: string, password: string, nom: string, prenom: string) {
    return this.http.post(
      `${this.apiUrl}/auth/register/`,
      { email, password, nom, prenom }
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.isLoggedIn.set(false);
    this.currentUser.set(null);
  }
}
