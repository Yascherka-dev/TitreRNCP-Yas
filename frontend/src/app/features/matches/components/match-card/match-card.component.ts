import { Component, input, computed, inject } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Match } from '../../../../core/models/fixture.model';
import { FavoritesService } from '../../../../core/services/favorites.service';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-match-card',
  standalone: true,
  imports: [DatePipe, RouterLink, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './match-card.component.html',
  styleUrl: './match-card.component.scss',
})
export class MatchCardComponent {
  match = input.required<Match>();

  private favoritesService = inject(FavoritesService);
  private authService      = inject(AuthService);
  private router           = inject(Router);

  isFavorite = computed(() =>
    this.favoritesService.isFavorite('match', parseInt(String(this.match().id).replace('football_', ''), 10))
  );

  toggleFavorite(event: Event) {
    event.stopPropagation();
    event.preventDefault();

    //console.log('match id:', this.match().id, typeof this.match().id);

    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }

    if (this.isFavorite()) {
      const favId = this.favoritesService.getFavoriteId('match', parseInt(String(this.match().id).replace('football_', ''), 10));
      if (favId) this.favoritesService.removeFavorite(favId).subscribe();
    } else {
      this.favoritesService.addFavorite('match', parseInt(String(this.match().id).replace('football_', ''), 10)).subscribe();
    }
  }

  statusConfig = computed(() => {
    const s = this.match().status.short;
    if (['1H', '2H', 'ET', 'BT', 'P', 'LIVE', 'HT'].includes(s)) {
      return { label: s === 'HT' ? 'Mi-temps' : `${this.match().status.elapsed}'`, cssClass: 'live' };
    }
    if (s === 'FT' || s === 'AET' || s === 'PEN') {
      return { label: 'Terminé', cssClass: 'finished' };
    }
    return { label: 'À venir', cssClass: 'upcoming' };
  });

  isStarted = computed(() => {
    const s = this.match().status.short;
    return !['NS', 'TBD', 'PST', 'CANC', 'ABD'].includes(s);
  });
}
