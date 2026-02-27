import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

// Composant skeleton pour la MatchCard.
// Reproduit la structure visuelle de la carte (ligue, équipes, actions)
// avec des blocs animés (effet shimmer) pendant le chargement.
// Aucune logique — uniquement du HTML/SCSS.
@Component({
  selector: 'app-skeleton-match-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './skeleton-match-card.component.html',
  styleUrl: './skeleton-match-card.component.scss',
})
export class SkeletonMatchCardComponent {}
