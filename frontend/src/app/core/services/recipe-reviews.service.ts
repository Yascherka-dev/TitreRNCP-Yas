import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, map, catchError, of, switchMap } from 'rxjs';
import { RecipeComment } from '../models/recipe.model';
import { environment } from '../../../environments/environment';

interface ApiComment {
  id: number;
  user: number;
  type: string;
  reference_id: string;
  contenu: string;
  date_soumission: string;
}

interface ApiRating {
  id: number;
  user: number;
  type: string;
  reference_id: string;
  valeur: number;
}

@Injectable({ providedIn: 'root' })
export class RecipeReviewsService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  private allComments = signal<RecipeComment[]>([]);
  private allRatings  = signal<Record<string, { value: number; apiId: number | null }>>({});

  loadReviews(recipeId: string): void {
    this.http
      .get<ApiComment[]>(`${this.apiUrl}/comments/?type=recette&reference_id=${recipeId}`)
      .pipe(catchError(() => of([])))
      .subscribe(items => {
        const mapped = items.map(c => this.toComment(c));
        this.allComments.update(existing => {
          const others = existing.filter(c => c.recipeId !== recipeId);
          return [...others, ...mapped];
        });
      });

    this.http
      .get<ApiRating[]>(`${this.apiUrl}/ratings/?type=recette&reference_id=${recipeId}`)
      .pipe(catchError(() => of([])))
      .subscribe(items => {
        if (items.length > 0) {
          const r = items[0];
          this.allRatings.update(ratings => ({
            ...ratings,
            [recipeId]: { value: r.valeur, apiId: r.id },
          }));
        }
      });
  }

  commentsFor(recipeId: string): RecipeComment[] {
    return this.allComments()
      .filter(c => c.recipeId === recipeId)
      .sort((a, b) => b.date.getTime() - a.date.getTime());
  }

  ratingFor(recipeId: string): number {
    return this.allRatings()[recipeId]?.value ?? 0;
  }

  setRating(recipeId: string, value: number): Observable<void> {
    const existing = this.allRatings()[recipeId];
    if (existing?.apiId) {
      return this.http
        .delete<void>(`${this.apiUrl}/ratings/${existing.apiId}/`)
        .pipe(
          tap(() => this.allRatings.update(r => ({ ...r, [recipeId]: { value: 0, apiId: null } }))),
          switchMap(() => this.postRating(recipeId, value)),
          catchError(() => of(undefined)),
        );
    }
    return this.postRating(recipeId, value);
  }

  private postRating(recipeId: string, value: number): Observable<void> {
    return this.http
      .post<ApiRating>(`${this.apiUrl}/ratings/`, {
        type: 'recette',
        reference_id: recipeId,
        valeur: value,
      })
      .pipe(
        tap(r => this.allRatings.update(ratings => ({
          ...ratings,
          [recipeId]: { value: r.valeur, apiId: r.id },
        }))),
        map(() => undefined),
        catchError(() => of(undefined)),
      );
  }

  addComment(recipeId: string, content: string): Observable<void> {
    return this.http
      .post<ApiComment>(`${this.apiUrl}/comments/`, {
        type: 'recette',
        reference_id: recipeId,
        contenu: content.trim(),
      })
      .pipe(
        tap(c => {
          const comment = this.toComment(c);
          this.allComments.update(list => [comment, ...list]);
        }),
        map(() => undefined),
        catchError(() => of(undefined)),
      );
  }

  deleteComment(commentId: string): Observable<void> {
    return this.http
      .delete<void>(`${this.apiUrl}/comments/${commentId}/`)
      .pipe(
        tap(() => this.allComments.update(list => list.filter(c => c.id !== commentId))),
        map(() => undefined),
        catchError(() => of(undefined)),
      );
  }

  private toComment(c: ApiComment): RecipeComment {
    return {
      id:       String(c.id),
      recipeId: c.reference_id,
      author:   'Vous',
      content:  c.contenu,
      rating:   0,
      date:     new Date(c.date_soumission),
    };
  }
}
