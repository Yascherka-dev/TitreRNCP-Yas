import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, catchError, of, Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { switchMap } from 'rxjs/operators';

// ─────────────────────────────────────────────────────────────────────────────
// Ce service est le point central de l'authentification.
// Il gère : connexion, déconnexion, inscription, et l'état de la session.
//
// L'état est exposé via deux "signals" Angular (valeurs réactives) :
//   • isLoggedIn  → booléen : est-ce que l'utilisateur est connecté ?
//   • currentUser → objet   : email / nom / prénom de l'utilisateur connecté
//
// Ces signals sont lus directement dans les templates HTML des composants.
// Quand leur valeur change, Angular met à jour l'affichage automatiquement.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Profil de l'utilisateur connecté.
 *
 * `id` est optionnel : une session ouverte avant l'ajout de ce champ garde en
 * localStorage un profil qui n'en contient pas. Il est renseigné dès le
 * prochain appel à /api/auth/me/.
 */
export interface CurrentUser {
  id?: number;
  email: string;
  nom: string;
  prenom: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  // ── État réactif ────────────────────────────────────────────────────────────

  // true si un access_token est présent dans localStorage.
  // Vérifié dès le chargement de l'app — pas besoin d'appel réseau pour ça.
  isLoggedIn = signal<boolean>(!!localStorage.getItem('access_token'));

  // Initialisé immédiatement depuis localStorage (clé "current_user").
  // Résultat : le prénom s'affiche dès le chargement, sans attendre de requête HTTP.
  // Le constructor fait ensuite une vraie vérification côté serveur en arrière-plan.
  currentUser = signal<CurrentUser | null>(
    this.storedUser(),
  );

  // ── Helpers localStorage ────────────────────────────────────────────────────

  // Lit et désérialise les infos utilisateur depuis localStorage.
  // Retourne null si la clé n'existe pas ou si le JSON est corrompu.
  private storedUser(): CurrentUser | null {
    try {
      const raw = localStorage.getItem('current_user');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  // Sérialise et sauvegarde les infos utilisateur dans localStorage.
  // Appelé après chaque login ou réponse réussie de /api/auth/me/.
  // Appelé avec null au logout pour tout effacer.
  private saveUser(user: CurrentUser | null) {
    if (user) {
      localStorage.setItem('current_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('current_user');
    }
  }

  // ── Initialisation au démarrage ─────────────────────────────────────────────

  constructor() {
    // Si un token existe (session précédente), on vérifie qu'il est encore valide
    // en appelant /api/auth/me/ côté serveur.
    //
    // Scénarios possibles :
    //   ✅ Token valide  → on reçoit le profil → currentUser mis à jour + sauvegardé
    //   🔄 Token expiré → l'intercepteur (auth.interceptor.ts) le renouvelle
    //                      automatiquement, puis rejoue la requête → même résultat ✅
    //   ❌ Tout expiré  → l'intercepteur appelle logout() qui nettoie tout,
    //                      puis l'erreur arrive ici → on ne touche à rien (déjà nettoyé)
    if (this.isLoggedIn()) {
      this.http
        .get<CurrentUser>(
          `${this.apiUrl}/auth/me/`,
        )
        .pipe(catchError(() => of(null)))
        .subscribe((user) => {
          if (user) {
            this.currentUser.set(user);
            this.saveUser(user);
          }
          // Si user est null → erreur réseau OU session expirée (logout() déjà appelé
          // par l'intercepteur). Dans les deux cas on ne touche pas currentUser :
          // soit logout() a déjà tout vidé, soit on garde le prénom affiché le temps
          // que le réseau revienne.
        });
    }
  }

  // ── API publique ────────────────────────────────────────────────────────────

  // Appelé par l'intercepteur quand une requête reçoit un 401 (token expiré).
  // Envoie le refresh_token au serveur et récupère un nouveau access_token.
  // Le nouveau token est sauvegardé dans localStorage et retourné à l'intercepteur.
  refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    return this.http
      .post<{ access: string }>(`${this.apiUrl}/auth/token/refresh/`, { refresh })
      .pipe(tap((res) => localStorage.setItem('access_token', res.access)));
  }

  // Connexion : email + mot de passe → tokens JWT → profil utilisateur.
  // Enchaîne deux requêtes HTTP :
  //   1. POST /auth/login/ → reçoit access_token + refresh_token → les stocke
  //   2. GET  /auth/me/   → reçoit le profil → met à jour currentUser
  login(email: string, password: string) {
    return this.http
      .post<{ access: string; refresh: string }>(
        `${this.apiUrl}/auth/login/`,
        { email, password },
      )
      .pipe(
        tap((res) => {
          localStorage.setItem('access_token', res.access);
          localStorage.setItem('refresh_token', res.refresh);
          this.isLoggedIn.set(true);
        }),
        // switchMap = "annule la requête précédente et enchaîne une nouvelle"
        // Ici : dès que le login réussit, on va chercher le profil
        switchMap(() =>
          this.http.get<CurrentUser>(
            `${this.apiUrl}/auth/me/`,
          ),
        ),
        tap((user) => {
          this.currentUser.set(user);
          this.saveUser(user); // sauvegarde pour les prochains rechargements de page
        }),
      );
  }

  // Inscription : crée le compte côté serveur.
  // Ne connecte pas l'utilisateur automatiquement — c'est le composant qui
  // appelle login() juste après si besoin.
  register(email: string, password: string, nom: string, prenom: string) {
    return this.http.post(`${this.apiUrl}/auth/register/`, {
      email,
      password,
      nom,
      prenom,
    });
  }

  // Déconnexion : supprime tous les tokens et vide l'état.
  // Les signals passent à false/null → Angular retire le prénom du header instantanément.
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.saveUser(null);
    this.isLoggedIn.set(false);
    this.currentUser.set(null);
  }

  /**
   * Droit à l'effacement : supprime le compte et tout ce qui en dépend.
   *
   * Le mot de passe est redemandé côté serveur — une session laissée ouverte
   * ne doit pas suffire à effacer un compte. L'échec doit remonter : c'est ce
   * qui permet d'afficher « mot de passe incorrect » plutôt que de laisser
   * croire à une suppression.
   */
  deleteAccount(password: string): Observable<void> {
    return this.http
      .delete<void>(`${this.apiUrl}/auth/me/`, { body: { password } })
      .pipe(tap(() => this.logout()));
  }
}
