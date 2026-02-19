import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { Recipe } from '../../../../core/models/recipe.model';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  imports: [MatCardModule, MatIconModule, MatChipsModule],
  templateUrl: './recipe-card.component.html',
  styleUrl: './recipe-card.component.scss',
})
export class RecipeCardComponent {
  recipe = input.required<Recipe>();
}
