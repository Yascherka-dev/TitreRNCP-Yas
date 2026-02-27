import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    // Landing page — point d'entrée de l'application
    path: '',
    loadComponent: () =>
      import('./features/landing/landing.component').then(
        m => m.LandingComponent
      ),
  },
  {
    // Dashboard — liste des matchs du soir
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
    // Toute URL inconnue → page 404 dédiée (lazy-loaded comme les autres pages)
    path: '**',
    loadComponent: () =>
      import('./features/not-found/not-found.component').then(
        m => m.NotFoundComponent
      ),
  },
];
