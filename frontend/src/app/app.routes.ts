import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/matches/pages/match-list/match-list.component').then(
        m => m.MatchListComponent
      ),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
