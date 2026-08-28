import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, map, catchError, of, switchMap } from 'rxjs';
import { RecipeComment } from '../models/recipe.model';
import { environment } from '../../../environments/environment';
import { AuthService } from './auth.service';

interface ApiComment {
  id: number;
  user: number;
  auteur: string;
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
  private auth   = inject(AuthService);
  private apiUrl = environment.apiUrl;

  private allComments = signal<RecipeComment[]>([]);
  // Toutes les notes de chaque recette, indexées par auteur : c'est ce qui
  // permet d'afficher la note de l'auteur sous son commentaire, et de retrouver
  // la sienne parmi celles des autres.
  private allRatings = signal<Record<string, ApiRating[]>>({});

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
        this.allRatings.update(ratings => ({ ...ratings, [recipeId]: items }));
        this.rafraichirNotesDesCommentaires(recipeId);
      });
  }

  commentsFor(recipeId: string): RecipeComment[] {
    return this.allComments()
      .filter(c => c.recipeId === recipeId)
      .sort((a, b) => b.date.getTime() - a.date.getTime());
  }

  /** La note de l'utilisateur connecté sur cette recette, 0 s'il n'en a pas mis. */
  ratingFor(recipeId: string): number {
    return this.maNote(recipeId)?.valeur ?? 0;
  }

  private maNote(recipeId: string): ApiRating | undefined {
    const moi = this.auth.currentUser()?.id;
    if (moi === undefined) return undefined;
    return (this.allRatings()[recipeId] ?? []).find(r => r.user === moi);
  }

  private noteDe(recipeId: string, userId: number): number {
    return (this.allRatings()[recipeId] ?? []).find(r => r.user === userId)?.valeur ?? 0;
  }

  /**
   * Commentaires et notes arrivent par deux requêtes parallèles : celle des
   * notes peut répondre en second. Les commentaires déjà affichés doivent
   * alors récupérer l'étoilage de leur auteur.
   */
  private rafraichirNotesDesCommentaires(recipeId: string): void {
    this.allComments.update(list =>
      list.map(c => c.recipeId === recipeId
        ? { ...c, rating: this.noteDe(recipeId, c.authorId) }
        : c));
  }

  setRating(recipeId: string, value: number): Observable<void> {
    const ancienne = this.maNote(recipeId);
    if (!ancienne) return this.postRating(recipeId, value);

    // Une seule note par utilisateur et par recette : la base le garantit.
    // Modifier revient donc à supprimer puis réécrire.
    return this.http
      .delete<void>(`${this.apiUrl}/ratings/${ancienne.id}/`)
      .pipe(
        tap(() => this.allRatings.update(ratings => ({
          ...ratings,
          [recipeId]: (ratings[recipeId] ?? []).filter(r => r.id !== ancienne.id),
        }))),
        switchMap(() => this.postRating(recipeId, value)),
        // Pas de catchError : un echec d'ecriture doit remonter au composant.
      );
  }

  private postRating(recipeId: string, value: number): Observable<void> {
    return this.http
      .post<ApiRating>(`${this.apiUrl}/ratings/`, {
        type: 'recette',
        reference_id: recipeId,
        valeur: value,
      })
      .pipe(
        tap(r => {
          this.allRatings.update(ratings => ({
            ...ratings,
            [recipeId]: [...(ratings[recipeId] ?? []).filter(x => x.user !== r.user), r],
          }));
          this.rafraichirNotesDesCommentaires(recipeId);
        }),
        map(() => undefined),
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
      );
  }

  deleteComment(commentId: string): Observable<void> {
    return this.http
      .delete<void>(`${this.apiUrl}/comments/${commentId}/`)
      .pipe(
        tap(() => this.allComments.update(list => list.filter(c => c.id !== commentId))),
        map(() => undefined),
      );
  }

  private toComment(c: ApiComment): RecipeComment {
    return {
      id:       String(c.id),
      recipeId: c.reference_id,
      authorId: c.user,
      author:   c.user === this.auth.currentUser()?.id ? 'Vous' : (c.auteur || 'Anonyme'),
      content:  c.contenu,
      rating:   this.noteDe(c.reference_id, c.user),
      date:     new Date(c.date_soumission),
    };
  }
}
