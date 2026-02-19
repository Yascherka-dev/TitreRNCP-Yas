import { Component, input, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { Recipe } from '../../../../core/models/recipe.model';
import { RecipeDialogComponent } from '../recipe-dialog/recipe-dialog.component';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  imports: [MatCardModule, MatIconModule, MatChipsModule, MatButtonModule],
  templateUrl: './recipe-card.component.html',
  styleUrl: './recipe-card.component.scss',
})
export class RecipeCardComponent {
  recipe = input.required<Recipe>();
  private dialog = inject(MatDialog);

  openDetail() {
    this.dialog.open(RecipeDialogComponent, {
      data: this.recipe(),
      maxWidth: '560px',
      width: '95vw',
      panelClass: 'recipe-dialog-panel',
    });
  }
}
