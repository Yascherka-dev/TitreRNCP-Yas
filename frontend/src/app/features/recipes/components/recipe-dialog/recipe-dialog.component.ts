import { Component, computed, inject, signal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { DatePipe } from '@angular/common';
import { Recipe } from '../../../../core/models/recipe.model';
import { RecipeReviewsService } from '../../../../core/services/recipe-reviews.service';
import { StarRatingComponent } from '../star-rating/star-rating.component';

@Component({
  selector: 'app-recipe-dialog',
  standalone: true,
  imports: [
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatChipsModule,
    DatePipe,
    StarRatingComponent,
  ],
  templateUrl: './recipe-dialog.component.html',
  styleUrl: './recipe-dialog.component.scss',
})
export class RecipeDialogComponent {

  recipe: Recipe = inject(MAT_DIALOG_DATA);
  dialogRef = inject(MatDialogRef<RecipeDialogComponent>);

  private reviewsService = inject(RecipeReviewsService);

  comments = computed(() => this.reviewsService.commentsFor(this.recipe.id));

  currentRating = computed(() => this.reviewsService.ratingFor(this.recipe.id));

  pendingRating = signal(0);

  commentText = signal('');

  submitError = signal('');

  submitReview(): void {
    if (this.pendingRating() === 0) {
      this.submitError.set('Veuillez sélectionner une note avant de soumettre.');
      return;
    }
    if (this.commentText().trim().length < 10) {
      this.submitError.set('Votre avis doit contenir au moins 10 caractères.');
      return;
    }

    this.reviewsService.setRating(this.recipe.id, this.pendingRating());
    this.reviewsService.addComment(this.recipe.id, this.commentText(), this.pendingRating());

    this.pendingRating.set(0);
    this.commentText.set('');
    this.submitError.set('');
  }
}
