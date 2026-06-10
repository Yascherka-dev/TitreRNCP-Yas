import { Component, computed, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { DatePipe, Location } from '@angular/common';
import { Router } from '@angular/router';
import { Recipe } from '../../../../core/models/recipe.model';
import { RecipeReviewsService } from '../../../../core/services/recipe-reviews.service';
import { FavoritesService } from '../../../../core/services/favorites.service';
import { AuthService } from '../../../../core/services/auth.service';
import { StarRatingComponent } from '../star-rating/star-rating.component';

@Component({
  selector: 'app-recipe-dialog',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    MatDialogModule,
    MatIconModule,
    MatChipsModule,
    MatDividerModule,
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
  private location         = inject(Location);

  constructor() {
    const urlAvantOuverture = this.location.path();
    const urlAvecRecette = urlAvantOuverture.includes('?')
      ? `${urlAvantOuverture}&recipe=${this.recipe.id}`
      : `${urlAvantOuverture}?recipe=${this.recipe.id}`;
    this.location.go(urlAvecRecette);
    this.dialogRef.afterClosed().subscribe(() => {
      this.location.go(urlAvantOuverture);
    });
    this.reviewsService.loadReviews(this.recipe.id);
  }

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

  print() {
    const content     = document.querySelector('mat-dialog-content') as HTMLElement;
    const innerScroll = document.querySelector('.mat-mdc-dialog-inner-scroll-container') as HTMLElement;
    [content, innerScroll].forEach(el => {
      if (!el) return;
      el.scrollTop = 0;
      el.style.setProperty('max-height', 'none',    'important');
      el.style.setProperty('overflow',   'visible', 'important');
    });
    window.addEventListener('afterprint', () => {
      [content, innerScroll].forEach(el => {
        if (!el) return;
        el.style.removeProperty('max-height');
        el.style.removeProperty('overflow');
      });
    }, { once: true });
    window.print();
  }

  share() {
    const urlPartage = `${window.location.origin}${window.location.pathname}?recipe=${this.recipe.id}`;
    if (navigator.share) {
      navigator.share({ title: this.recipe.title, url: urlPartage });
    } else {
      navigator.clipboard.writeText(urlPartage);
    }
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
    const rating  = this.pendingRating();
    const content = this.commentText();
    this.reviewsService.setRating(this.recipe.id, rating).subscribe();
    this.reviewsService.addComment(this.recipe.id, content, rating).subscribe();
    this.pendingRating.set(0);
    this.commentText.set('');
    this.submitError.set('');
  }
}
