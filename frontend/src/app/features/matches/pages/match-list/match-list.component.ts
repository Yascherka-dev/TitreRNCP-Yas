import { Component, OnInit, signal, computed, DestroyRef, inject, ChangeDetectionStrategy } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
  imports: [DatePipe, FormsModule, MatchCardComponent, SkeletonMatchCardComponent],
  templateUrl: './match-list.component.html',
  styleUrl: './match-list.component.scss',
})
export class MatchListComponent implements OnInit {
  today = new Date();
  matches = signal<Match[]>([]);
  loading = signal(true);
  skeletonItems = Array.from({ length: 8 });

  selectedLeague   = signal<number | 'all'>('all');
  selectedCountry  = signal<string | 'all'>('all');
  selectedDate     = signal<string | null>(null);  // format YYYY-MM-DD
  countrySearch    = signal('');
  countryDropdown  = signal(false);

  readonly PAGE_SIZE = 10;
  currentPage  = signal(1);
  totalPages   = computed(() => Math.ceil(this.filteredMatches().length / this.PAGE_SIZE));

  // Compétitions uniques extraites des matchs chargés
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

  // Pays uniques extraits de tous les matchs (home + away)
  countries = computed<string[]>(() => {
    const seen = new Set<string>();
    for (const m of this.matches()) {
      if (m.home.countryName) seen.add(m.home.countryName);
      if (m.away.countryName) seen.add(m.away.countryName);
    }
    return Array.from(seen).sort();
  });

  filteredCountries = computed<string[]>(() => {
    const q = this.countrySearch().toLowerCase().trim();
    return q ? this.countries().filter(c => c.toLowerCase().includes(q)) : this.countries();
  });

  paginatedMatches = computed<Match[]>(() => {
    const start = (this.currentPage() - 1) * this.PAGE_SIZE;
    return this.filteredMatches().slice(start, start + this.PAGE_SIZE);
  });

  // Applique les trois filtres en même temps
  filteredMatches = computed<Match[]>(() => {
    let result = this.matches();

    // Filtre compétition
    const league = this.selectedLeague();
    if (league !== 'all') {
      result = result.filter(m => m.league.id === league);
    }

    // Filtre pays
    const country = this.selectedCountry();
    if (country !== 'all') {
      result = result.filter(m =>
        m.home.countryName === country || m.away.countryName === country
      );
    }

    // Filtre date
    const date = this.selectedDate();
    if (date) {
      result = result.filter(m => {
        const d = m.date;
        const yyyy = d.getFullYear();
        const mm   = String(d.getMonth() + 1).padStart(2, '0');
        const dd   = String(d.getDate()).padStart(2, '0');
        return `${yyyy}-${mm}-${dd}` === date;
      });
    }

    // Live → à venir → terminés, puis par date croissante dans chaque groupe
    const order = (m: Match) => {
      const s = m.status.short;
      if (s === 'LIVE' || s === 'HT') return 0;
      if (s === 'NS') return 1;
      return 2;
    };
    return result.slice().sort((a, b) => {
      const diff = order(a) - order(b);
      return diff !== 0 ? diff : a.date.getTime() - b.date.getTime();
    });
  });

  private destroyRef = inject(DestroyRef);

  constructor(private matchesService: MatchesService) {}

  ngOnInit() {
    this.matchesService.getFixtures().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: data => { this.matches.set(data); this.loading.set(false); },
      error: ()   => { this.loading.set(false); }
    });
  }

  selectLeague(id: number | 'all')  { this.selectedLeague.set(id); this.currentPage.set(1); }
  selectCountry(c: string | 'all') {
    this.selectedCountry.set(c);
    this.countryDropdown.set(false);
    this.countrySearch.set('');
    this.currentPage.set(1);
  }
  isLeagueSelected(id: number | 'all') { return this.selectedLeague() === id; }
  isCountrySelected(c: string | 'all') { return this.selectedCountry() === c; }

  toggleCountryDropdown() { this.countryDropdown.update(v => !v); }
  closeCountryDropdown()  { this.countryDropdown.set(false); this.countrySearch.set(''); }

  countryLabel() {
    const c = this.selectedCountry();
    return c === 'all' ? 'Tous les pays' : c;
  }

  setToday() {
    const d  = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    this.selectedDate.set(`${d.getFullYear()}-${mm}-${dd}`);
    this.currentPage.set(1);
  }

  clearDate() { this.selectedDate.set(null); this.currentPage.set(1); }

  setDate(value: string | null) { this.selectedDate.set(value); this.currentPage.set(1); }

  prevPage() { this.currentPage.update(p => Math.max(1, p - 1)); }
  nextPage() { this.currentPage.update(p => Math.min(this.totalPages(), p + 1)); }
}
