import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { Recipe } from '../../../../core/models/recipe.model';

@Component({
  selector: 'app-recipe-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule, MatIconModule, MatDividerModule, MatChipsModule],
  templateUrl: './recipe-dialog.component.html',
  styleUrl: './recipe-dialog.component.scss',
})
export class RecipeDialogComponent {
  recipe: Recipe = inject(MAT_DIALOG_DATA);
  dialogRef = inject(MatDialogRef<RecipeDialogComponent>);
}
