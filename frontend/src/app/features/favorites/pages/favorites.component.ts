import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { FavoritesService } from '../../../core/services/favorites.service';
import { MatchesService } from '../../../core/services/matches.service';
import { RecipesService } from '../../../core/services/recipes.service';
import { Match } from '../../../core/models/fixture.model';
import { Recipe } from '../../../core/models/recipe.model';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { RecipeDialogComponent } from '../../../features/recipes/components/recipe-dialog/recipe-dialog.component';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [CommonModule, RouterLink, MatIconModule, MatButtonModule],
  templateUrl: './favorites.component.html',
  styleUrl: './favorites.component.scss'
})
export class FavoritesComponent implements OnInit {
  private favoritesService = inject(FavoritesService);
  private matchesService   = inject(MatchesService);
  private recipesService   = inject(RecipesService);
  private dialog = inject(MatDialog);

  allMatches = signal<Match[]>([]);
  allRecipes = signal<Recipe[]>([]);

  openRecipe(recipe: Recipe) {
  this.dialog.open(RecipeDialogComponent, {
    data: recipe,
    width: '680px',
    maxHeight: '90vh',
  });
}


  favoriteMatches = computed(() => {
    const favIds = this.favoritesService.favorites()
      .filter(f => f.type === 'match')
      .map(f => f.reference_id);
    return this.allMatches().filter(m => favIds.includes(m.id));
  });

  favoriteRecipes = computed(() => {
    const favIds = this.favoritesService.favorites()
      .filter(f => f.type === 'recette')
      .map(f => f.reference_id);
    return this.allRecipes().filter(r => favIds.includes(String(r.id)));
  });

  ngOnInit() {
    this.favoritesService.loadFavorites().subscribe();
    this.matchesService.getFixtures().subscribe(matches => {
      this.allMatches.set(matches);
    });
    this.recipesService.getAll().subscribe(recipes => {
      this.allRecipes.set(recipes);
    });
  }
}
