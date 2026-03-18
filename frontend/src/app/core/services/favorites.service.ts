import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Favorite {
  id: number;
  type: 'match' | 'recette' | 'equipe';
  reference_id: string;
}

@Injectable({ providedIn: 'root' })
export class FavoritesService {
  private http   = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  favorites = signal<Favorite[]>([]);

  loadFavorites() {
    return this.http.get<Favorite[]>(`${this.apiUrl}/favorites/`).pipe(
      tap(data => this.favorites.set(data))
    );
  }

  addFavorite(type: Favorite['type'], referenceId: string) {
    return this.http.post<Favorite>(`${this.apiUrl}/favorites/`, {
      type,
      reference_id: referenceId
    }).pipe(
      tap(newFav => this.favorites.update(list => [...list, newFav]))
    );
  }

  removeFavorite(id: number) {
    return this.http.delete(`${this.apiUrl}/favorites/${id}/`).pipe(
      tap(() => this.favorites.update(list => list.filter(f => f.id !== id)))
    );
  }

  isFavorite(type: Favorite['type'], referenceId: string): boolean {
    return this.favorites().some(f => f.type === type && f.reference_id === referenceId);
  }

  getFavoriteId(type: Favorite['type'], referenceId: string): number | undefined {
    return this.favorites().find(f => f.type === type && f.reference_id === referenceId)?.id;
  }
}
