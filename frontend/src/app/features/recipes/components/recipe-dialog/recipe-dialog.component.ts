import { Component, computed, inject, signal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { Recipe } from '../../../../core/models/recipe.model';
import { RecipeReviewsService } from '../../../../core/services/recipe-reviews.service';
import { FavoritesService } from '../../../../core/services/favorites.service';
import { AuthService } from '../../../../core/services/auth.service';
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

  recipe: Recipe           = inject(MAT_DIALOG_DATA);
  dialogRef                = inject(MatDialogRef<RecipeDialogComponent>);
  private reviewsService   = inject(RecipeReviewsService);
  private favoritesService = inject(FavoritesService);
  private authService      = inject(AuthService);
  private router           = inject(Router);

  comments      = computed(() => this.reviewsService.commentsFor(this.recipe.id));
  currentRating = computed(() => this.reviewsService.ratingFor(this.recipe.id));
  pendingRating = signal(0);
  commentText   = signal('');
  submitError   = signal('');

  isFavorite = computed(() =>
    this.favoritesService.isFavorite('recette', this.recipe.id)
  );

  toggleFavorite() {
    if (!this.authService.isLoggedIn()) {
      this.dialogRef.close();
      this.router.navigate(['/login']);
      return;
    }

    if (this.isFavorite()) {
      const favId = this.favoritesService.getFavoriteId('recette', this.recipe.id);
      if (favId) this.favoritesService.removeFavorite(favId).subscribe();
    } else {
      this.favoritesService.addFavorite('recette', this.recipe.id).subscribe();
    }
  }

  share() {
  if (navigator.share) {
    navigator.share({
      title: this.recipe.title,
      text: `Découvrez cette recette : ${this.recipe.title}`,
      url: window.location.href,
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
  }
}

print() {
  window.print();
}


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
