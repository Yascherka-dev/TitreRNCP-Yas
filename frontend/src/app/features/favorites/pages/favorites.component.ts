import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { FavoritesService, Favorite } from '../../../core/services/favorites.service';
import { MatchesService } from '../../../core/services/matches.service';
import { Match } from '../../../core/models/fixture.model';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

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

  allMatches = signal<Match[]>([]);

  favoriteMatches = computed(() => {
    const favIds = this.favoritesService.favorites()
      .filter(f => f.type === 'match')
      .map(f => f.reference_id);
    return this.allMatches().filter(m =>
      favIds.includes(m.id)
    );
  });

  ngOnInit() {
    this.favoritesService.loadFavorites().subscribe();
    this.matchesService.getFixtures().subscribe(matches => {
      this.allMatches.set(matches);
    });
  }
}
