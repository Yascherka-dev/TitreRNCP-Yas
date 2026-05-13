import { Component, input, inject, computed, ChangeDetectionStrategy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Recipe } from '../../../../core/models/recipe.model';
import { RecipeDialogComponent } from '../recipe-dialog/recipe-dialog.component';

const SALE_IMGS  = [1,2,3,4,5,6].map(n => `/assets/images/food/sale-0${n}.png`);
const SUCRE_IMGS = [1,2,3,4,5].map(n => `/assets/images/food/sucre-0${n}.png`);

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

  localImage = computed(() => {
    const r    = this.recipe();
    const pool = r.typePlat === 'sucré' ? SUCRE_IMGS : SALE_IMGS;
    const seed = Math.abs(r.id.split('').reduce((a, c) => a + c.charCodeAt(0), 0));
    return pool[seed % pool.length];
  });

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
