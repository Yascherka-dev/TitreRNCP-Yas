import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

// Composant skeleton pour la RecipeCard.
// Reproduit la structure (image, titre, description, méta, tags, bouton)
// avec des blocs animés pendant le chargement des suggestions.
// Aucune logique — uniquement du HTML/SCSS.
@Component({
  selector: 'app-skeleton-recipe-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './skeleton-recipe-card.component.html',
  styleUrl: './skeleton-recipe-card.component.scss',
})
export class SkeletonRecipeCardComponent {}
