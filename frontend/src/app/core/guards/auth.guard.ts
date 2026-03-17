// auth.guard.ts
// Un guard Angular est une fonction qui décide si on peut accéder à une route.
// Ici : si l'utilisateur n'est pas connecté → on le redirige vers /login.

import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router      = inject(Router);

  if (authService.isLoggedIn()) {
    // Connecté → accès autorisé
    return true;
  }

  // Pas connecté → redirige vers /login
  return router.createUrlTree(['/login']);
};
