import { Component, input, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { Match } from '../../../../core/models/fixture.model';
import { FavoritesService } from '../../../../core/services/favorites.service';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-match-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [DatePipe, RouterLink],
  templateUrl: './match-card.component.html',
  styleUrl: './match-card.component.scss',
  host: {
    '(mouseenter)': 'hovering.set(true)',
    '(mouseleave)': 'hovering.set(false)',
  },
})
export class MatchCardComponent {
  match   = input.required<Match>();
  hovering = signal(false);

  private favoritesService = inject(FavoritesService);
  private authService      = inject(AuthService);
  private router           = inject(Router);

  isFavorite = computed(() =>
    this.favoritesService.isFavorite('match', this.match().id)
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
      const favId = this.favoritesService.getFavoriteId('match', this.match().id);
      if (favId) this.favoritesService.removeFavorite(favId).subscribe();
    } else {
      this.favoritesService.addFavorite('match', this.match().id).subscribe();
    }
  }

  statusConfig = computed(() => {
    const s = this.match().status.short;
    if (['1H', '2H', 'ET', 'BT', 'P', 'LIVE', 'HT'].includes(s)) {
      if (s === 'HT') return { label: 'Mi-temps', cssClass: 'live' };
      const elapsed = this.match().status.elapsed;
      return { label: elapsed != null ? `${elapsed}'` : 'En cours', cssClass: 'live' };
    }
    if (['FT', 'AET', 'PEN'].includes(s)) {
      return { label: 'Terminé', cssClass: 'finished' };
    }
    if (['PST', 'CANC', 'ABD', 'SUSP'].includes(s)) {
      return { label: 'Annulé', cssClass: 'cancelled' };
    }
    return { label: 'À venir', cssClass: 'upcoming' };
  });

  isStarted = computed(() => {
    const s = this.match().status.short;
    return !['NS', 'TBD', 'PST', 'CANC', 'ABD'].includes(s);
  });
}
