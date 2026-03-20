import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { BehaviorSubject, catchError, filter, switchMap, take, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

// Partagé entre toutes les invocations de l'intercepteur (singleton de facto)
let isRefreshing = false;
const refreshDone$ = new BehaviorSubject<string | null>(null);

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = localStorage.getItem('access_token');

  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status !== 401) {
        return throwError(() => err);
      }

      // Évite les refreshs parallèles : si un refresh est en cours, on attend
      if (isRefreshing) {
        return refreshDone$.pipe(
          filter((t) => t !== null),
          take(1),
          switchMap((newToken) => {
            const retryReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` },
            });
            return next(retryReq);
          }),
        );
      }

      isRefreshing = true;
      refreshDone$.next(null);

      return auth.refreshToken().pipe(
        switchMap((res) => {
          isRefreshing = false;
          refreshDone$.next(res.access);
          const retryReq = req.clone({
            setHeaders: { Authorization: `Bearer ${res.access}` },
          });
          return next(retryReq);
        }),
        catchError((refreshErr) => {
          isRefreshing = false;
          refreshDone$.next(null);
          auth.logout();
          return throwError(() => refreshErr);
        }),
      );
    }),
  );
};
