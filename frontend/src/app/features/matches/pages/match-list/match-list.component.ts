import { Component, OnInit, signal, computed } from '@angular/core';
import { DatePipe } from '@angular/common';
import { MatchCardComponent } from '../../components/match-card/match-card.component';
import { SkeletonMatchCardComponent } from '../../../../shared/components/skeleton-match-card/skeleton-match-card.component';
import { MatchesService } from '../../../../core/services/matches.service';
import { Match } from '../../../../core/models/fixture.model';

interface LeagueFilter {
  id: number | 'all';
  name: string;
}

@Component({
  selector: 'app-match-list',
  standalone: true,
  imports: [DatePipe, MatchCardComponent, SkeletonMatchCardComponent],
  templateUrl: './match-list.component.html',
  styleUrl: './match-list.component.scss',
})
export class MatchListComponent implements OnInit {
  today = new Date();
  matches = signal<Match[]>([]);
  selectedLeague = signal<number | 'all'>('all');

  loading = signal(true);

  skeletonItems = Array(8);

  leagues = computed<LeagueFilter[]>(() => {
    const seen = new Set<number>();
    const result: LeagueFilter[] = [];
    for (const m of this.matches()) {
      if (!seen.has(m.league.id)) {
        seen.add(m.league.id);
        result.push({ id: m.league.id, name: m.league.name });
      }
    }
    return result;
  });

  filteredMatches = computed<Match[]>(() => {
    const sel = this.selectedLeague();
    if (sel === 'all') return this.matches();
    return this.matches().filter(m => m.league.id === sel);
  });

  constructor(private matchesService: MatchesService) {}

  ngOnInit() {
    this.matchesService.getFixtures().subscribe(data => {
      this.matches.set(data);
      this.loading.set(false);
    });
  }

  selectLeague(id: number | 'all') {
    this.selectedLeague.set(id);
  }

  isSelected(id: number | 'all') {
    return this.selectedLeague() === id;
  }
}
