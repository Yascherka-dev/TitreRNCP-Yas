import { Component, input, computed } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Match } from '../../../../core/models/fixture.model';

@Component({
  selector: 'app-match-card',
  standalone: true,
  imports: [DatePipe, RouterLink, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './match-card.component.html',
  styleUrl: './match-card.component.scss',
})
export class MatchCardComponent {
  match = input.required<Match>();

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
