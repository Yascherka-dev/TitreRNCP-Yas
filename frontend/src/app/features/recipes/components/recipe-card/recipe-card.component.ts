import { Component, input, inject, computed, ChangeDetectionStrategy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Recipe } from '../../../../core/models/recipe.model';
import { localRecipeImage } from '../../../../core/utils/recipe-image.util';
import { RecipeDialogComponent } from '../recipe-dialog/recipe-dialog.component';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [],
  templateUrl: './recipe-card.component.html',
  styleUrl: './recipe-card.component.scss',
})
export class RecipeCardComponent {
  recipe = input.required<Recipe>();

  localImage = computed(() => localRecipeImage(this.recipe()));

  private dialog = inject(MatDialog);

  openDetail() {
    this.dialog.open(RecipeDialogComponent, {
      data: this.recipe(),
      maxWidth: '560px',
      width: '95vw',
      panelClass: 'recipe-dialog-panel',
      backdropClass: 'mm-dialog-backdrop',
    });
  }
}
