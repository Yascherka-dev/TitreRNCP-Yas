import { Component, computed, inject, signal } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { DatePipe, Location } from '@angular/common'; // Location = service qui lit/modifie l'URL du navigateur
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
    // Le problème : mat-dialog-content a max-height: 62vh + overflow: auto
    // Le navigateur imprime uniquement la portion visible du scroll — pas tout le contenu
    // Solution : on enlève ces contraintes AVANT d'imprimer, on restaure APRÈS

    // document.querySelector cherche le premier élément mat-dialog-content dans la page
    // "as HTMLElement" dit à TypeScript "traite ce résultat comme un élément HTML"
    const content = document.querySelector('mat-dialog-content') as HTMLElement;

    if (content) {
      // scrollTop = position verticale du scroll (0 = tout en haut)
      // On remonte en haut pour être sûr que le contenu part depuis le début
      content.scrollTop = 0;

      // setProperty avec 'important' écrase tous les autres styles (même Material)
      content.style.setProperty('max-height', 'none', 'important');
      content.style.setProperty('overflow', 'visible', 'important');
    }

    // window.addEventListener écoute l'événement 'afterprint'
    // afterprint se déclenche quand l'utilisateur ferme la fenêtre d'impression
    // { once: true } = l'écouteur se supprime automatiquement après un seul déclenchement
    window.addEventListener('afterprint', () => {
      if (content) {
        // removeProperty enlève les styles inline qu'on avait ajoutés
        // → mat-dialog-content retrouve ses styles SCSS d'origine (62vh + scroll)
        content.style.removeProperty('max-height');
        content.style.removeProperty('overflow');
      }
    }, { once: true });

    // On ouvre la fenêtre d'impression du navigateur
    window.print();
  }

  share() {
    // On construit l'URL de partage propre avec le ?recipe=<id>
    // window.location.origin = le domaine (ex: "https://matchmuunch.com" ou "http://localhost:4200")
    // window.location.pathname = le chemin (ex: "/matches/5")
    // On n'utilise PAS window.location.href car il peut déjà contenir un ?recipe= qu'on a mis nous-mêmes
    // On repart de zéro pour avoir une URL propre et sans doublon
    const urlPartage = `${window.location.origin}${window.location.pathname}?recipe=${this.recipe.id}`;

    // navigator.share = l'API native du téléphone/navigateur pour partager (SMS, WhatsApp, etc.)
    // Elle n'existe PAS sur tous les navigateurs (souvent absente sur desktop)
    if (navigator.share) {
      navigator.share({
        title: this.recipe.title,
        url: urlPartage,
      });
    } else {
      // Fallback : si le navigateur ne supporte pas navigator.share (ex: Chrome desktop)
      // On copie l'URL dans le presse-papier de l'utilisateur
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

    this.reviewsService.setRating(this.recipe.id, this.pendingRating());
    this.reviewsService.addComment(this.recipe.id, this.commentText(), this.pendingRating());

    this.pendingRating.set(0);
    this.commentText.set('');
    this.submitError.set('');
  }
}
