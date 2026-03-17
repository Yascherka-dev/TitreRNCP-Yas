import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // Au démarrage : vérifie si un token existe déjà (session précédente)
  isLoggedIn = signal<boolean>(!!localStorage.getItem('access_token'));

  currentUser = signal<{ email: string; nom: string; prenom: string } | null>(null);

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
