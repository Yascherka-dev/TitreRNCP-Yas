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
    DatePipe,            // Pipe Angular pour formater les dates ({{ date | date:'dd/MM/yyyy' }})
    StarRatingComponent, // Composant étoiles custom (notation + lecture seule)
  ],
  templateUrl: './recipe-dialog.component.html',
  styleUrl: './recipe-dialog.component.scss',
})
export class RecipeDialogComponent {

  // ── Données de la recette injectées par MatDialog.open({ data: recipe }) ──
  recipe: Recipe = inject(MAT_DIALOG_DATA);
  dialogRef = inject(MatDialogRef<RecipeDialogComponent>);

  // ── Service de gestion des avis ───────────────────────────────────────────
  private reviewsService = inject(RecipeReviewsService);

  // ── Données réactives ─────────────────────────────────────────────────────
  // computed() recalcule automatiquement quand le service est mis à jour

  // Liste des commentaires pour cette recette spécifique
  comments = computed(() => this.reviewsService.commentsFor(this.recipe.id));

  // Note enregistrée pour cette recette (0 si pas encore notée)
  currentRating = computed(() => this.reviewsService.ratingFor(this.recipe.id));

  // ── État du formulaire ────────────────────────────────────────────────────

  // Note sélectionnée dans le formulaire (0 = aucune étoile cliquée)
  pendingRating = signal(0);

  // Texte tapé dans la zone de commentaire
  commentText = signal('');

  // Message d'erreur affiché si la validation échoue
  submitError = signal('');

  // ── Soumission de l'avis ──────────────────────────────────────────────────
  submitReview(): void {
    // Validation : une note est obligatoire
    if (this.pendingRating() === 0) {
      this.submitError.set('Veuillez sélectionner une note avant de soumettre.');
      return;
    }
    // Validation : minimum 10 caractères dans le commentaire
    if (this.commentText().trim().length < 10) {
      this.submitError.set('Votre avis doit contenir au moins 10 caractères.');
      return;
    }

    // Enregistrement dans le service (stockage local pour l'instant)
    this.reviewsService.setRating(this.recipe.id, this.pendingRating());
    this.reviewsService.addComment(this.recipe.id, this.commentText(), this.pendingRating());

    // Réinitialisation du formulaire après soumission réussie
    this.pendingRating.set(0);
    this.commentText.set('');
    this.submitError.set('');
  }
}
