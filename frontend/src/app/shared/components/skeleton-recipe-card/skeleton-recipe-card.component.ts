import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-skeleton-recipe-card',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './skeleton-recipe-card.component.html',
  styleUrl: './skeleton-recipe-card.component.scss',
})
export class SkeletonRecipeCardComponent {}
