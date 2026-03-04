import { Routes } from '@angular/router';

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
    path: '**',
    loadComponent: () =>
      import('./features/not-found/not-found.component').then(
        m => m.NotFoundComponent
      ),
  },
];
