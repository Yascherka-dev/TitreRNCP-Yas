import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-skeleton-recipe-card',
  standalone: true,
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './skeleton-recipe-card.component.html',
  styleUrl: './skeleton-recipe-card.component.scss',
})
export class SkeletonRecipeCardComponent {}
