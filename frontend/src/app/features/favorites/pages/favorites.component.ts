import { Component, inject, OnInit, signal, computed, ChangeDetectionStrategy } from '@angular/core';
import { FavoritesService } from '../../../core/services/favorites.service';
import { MatchesService } from '../../../core/services/matches.service';
import { RecipesService } from '../../../core/services/recipes.service';
import { Match } from '../../../core/models/fixture.model';
import { Recipe } from '../../../core/models/recipe.model';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { RecipeDialogComponent } from '../../../features/recipes/components/recipe-dialog/recipe-dialog.component';

const SALE_IMGS  = [1,2,3,4,5,6].map(n => `/assets/images/food/sale-0${n}.webp`);
const SUCRE_IMGS = [1,2,3,4,5].map(n => `/assets/images/food/sucre-0${n}.webp`);

export function localImageFor(recipe: Recipe): string {
  const pool = recipe.typePlat === 'sucré' ? SUCRE_IMGS : SALE_IMGS;
  const seed = Math.abs(recipe.id.split('').reduce((a, c) => a + c.charCodeAt(0), 0));
  return pool[seed % pool.length];
}

function formatTime(minutes: number): string {
  if (!minutes) return '—';
  if (minutes < 60) return `${minutes}min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m ? `${h}h${m.toString().padStart(2, '0')}` : `${h}h`;
}

@Component({
  selector: 'app-favorites',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, RouterLink, FormsModule],
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

  searchQuery  = signal('');
  activeFilter = signal('all');

  localImageFor = localImageFor;
  formatTime    = formatTime;

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

  uniqueCountries = computed(() =>
    [...new Set(this.favoriteRecipes().map(r => r.country))].sort()
  );

  filteredRecipes = computed(() => {
    let list = this.favoriteRecipes();
    const q = this.searchQuery().toLowerCase().trim();
    const f = this.activeFilter();
    if (q) list = list.filter(r =>
      r.title.toLowerCase().includes(q) || r.country.toLowerCase().includes(q) || r.equipe.toLowerCase().includes(q)
    );
    if (f !== 'all') list = list.filter(r => r.country === f);
    return list;
  });

  avgCookTime = computed(() => {
    const recs = this.favoriteRecipes();
    if (!recs.length) return 0;
    return Math.round(recs.reduce((acc, r) => acc + r.prepTime + r.cookTime, 0) / recs.length);
  });

  uniqueCountryCount = computed(() =>
    new Set(this.favoriteRecipes().map(r => r.country)).size
  );

  countByCountry(country: string): number {
    return this.favoriteRecipes().filter(r => r.country === country).length;
  }

  openRecipe(recipe: Recipe) {
    this.dialog.open(RecipeDialogComponent, {
      data: recipe,
      width: '680px',
      maxHeight: '90vh',
    });
  }

  removeFavorite(type: 'match' | 'recette', refId: string, event: Event) {
    event.preventDefault();
    event.stopPropagation();
    const favId = this.favoritesService.getFavoriteId(type, refId);
    if (favId !== undefined) {
      this.favoritesService.removeFavorite(favId).subscribe();
    }
  }

  ngOnInit() {
    this.favoritesService.loadFavorites().subscribe();
    this.matchesService.getFixtures().subscribe(matches => this.allMatches.set(matches));
    this.recipesService.getAll().subscribe(recipes => this.allRecipes.set(recipes));
  }
}
