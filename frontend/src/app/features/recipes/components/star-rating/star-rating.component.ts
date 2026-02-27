import { Component, input, output, signal } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

// Composant d'affichage et de sélection d'une note de 1 à 5 étoiles.
// Utilisable en mode interactif (formulaire) ou en lecture seule (affichage des avis).
@Component({
  selector: 'app-star-rating',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './star-rating.component.html',
  styleUrl: './star-rating.component.scss',
})
export class StarRatingComponent {

  // ── Inputs ────────────────────────────────────────────────────────────────

  // Valeur actuelle de la note (0 = pas encore noté)
  value = input<number>(0);

  // Si true, les étoiles sont affichées sans interaction (pour les commentaires)
  readonly = input<boolean>(false);

  // ── Output ────────────────────────────────────────────────────────────────

  // Émis quand l'utilisateur clique sur une étoile — valeur = étoile sélectionnée (1-5)
  ratingChange = output<number>();

  // ── État interne ──────────────────────────────────────────────────────────

  // Étoile survolée au hover (0 = aucun hover actif)
  hovered = signal(0);

  // Tableau des 5 étoiles pour le @for dans le template
  stars = [1, 2, 3, 4, 5];

  // ── Actions ───────────────────────────────────────────────────────────────

  select(star: number): void {
    if (!this.readonly()) {
      this.ratingChange.emit(star);
    }
  }

  onMouseEnter(star: number): void {
    if (!this.readonly()) {
      this.hovered.set(star);
    }
  }

  onMouseLeave(): void {
    if (!this.readonly()) {
      this.hovered.set(0);
    }
  }

  // Détermine si une étoile doit être affichée pleine ou vide.
  // Priorité au hover (pendant le survol), sinon la valeur actuelle.
  isFilled(star: number): boolean {
    return star <= (this.hovered() || this.value());
  }
}
