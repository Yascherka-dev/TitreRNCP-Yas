import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/landing/landing.component').then(
        m => m.LandingComponent
      ),
  },
  {
    path: 'matches',
    loadComponent: () =>
      import('./features/matches/pages/match-list/match-list.component').then(
        m => m.MatchListComponent
      ),
  },
  {
    path: 'matches/:id',
    loadComponent: () =>
      import('./features/matches/pages/match-detail/match-detail.component').then(
        m => m.MatchDetailComponent
      ),
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/pages/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./features/auth/pages/register/register.component').then(m => m.RegisterComponent),
  },
{
  path: 'favorites',
  canActivate: [authGuard],
  loadComponent: () =>
    import('./features/favorites/pages/favorites.component').then(
      m => m.FavoritesComponent
    ),
},
  {
    path: 'parametres',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/settings/settings.component').then(
        m => m.SettingsComponent
      ),
  },
  {
    path: 'mentions-legales',
    loadComponent: () =>
      import('./features/legal/legal-notice.component').then(
        m => m.LegalNoticeComponent
      ),
  },
  {
    path: 'partenaires/:slug',
    loadComponent: () =>
      import('./features/partners/partner-bridge.component').then(
        m => m.PartnerBridgeComponent
      ),
  },
  {
    path: '**',
    loadComponent: () =>
      import('./features/not-found/not-found.component').then(
        m => m.NotFoundComponent
      ),
  },
];
