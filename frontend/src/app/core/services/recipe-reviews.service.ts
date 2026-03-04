import { Injectable, signal } from '@angular/core';
import { RecipeComment } from '../models/recipe.model';

@Injectable({ providedIn: 'root' })
export class RecipeReviewsService {

  private allComments = signal<RecipeComment[]>([]);

  private allRatings = signal<Record<string, number>>({});

  commentsFor(recipeId: string): RecipeComment[] {
    return this.allComments()
      .filter(c => c.recipeId === recipeId)
      .sort((a, b) => b.date.getTime() - a.date.getTime());
  }

  ratingFor(recipeId: string): number {
    return this.allRatings()[recipeId] ?? 0;
  }

  setRating(recipeId: string, value: number): void {
    this.allRatings.update(ratings => ({ ...ratings, [recipeId]: value }));
  }

  addComment(recipeId: string, content: string, rating: number): void {
    const comment: RecipeComment = {
      id: crypto.randomUUID(),
      recipeId,
      author: 'Vous',
      content: content.trim(),
      rating,
      date: new Date(),
    };
    this.allComments.update(list => [comment, ...list]);
  }
}
