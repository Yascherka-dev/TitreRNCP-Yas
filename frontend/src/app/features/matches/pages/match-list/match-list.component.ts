import { Component, OnInit, signal, computed, DestroyRef, inject, ChangeDetectionStrategy } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { interval } from 'rxjs';
import { startWith, switchMap } from 'rxjs/operators';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatchCardComponent } from '../../components/match-card/match-card.component';
import { SkeletonMatchCardComponent } from '../../../../shared/components/skeleton-match-card/skeleton-match-card.component';
import { MatchesService } from '../../../../core/services/matches.service';
import { Match } from '../../../../core/models/fixture.model';

interface LeagueFilter { id: number | 'all'; name: string; }

const LIVE_STATUSES = new Set(['1H', '2H', 'HT', 'ET', 'P', 'BT']);

const SPORT_LABELS: Record<string, string> = {
  football:          '⚽ Football',
  basketball:        '🏀 Basket',
  ice_hockey:        '🏒 Hockey',
  american_football: '🏈 NFL',
  rugby:             '🏉 Rugby',
  tennis:            '🎾 Tennis',
  baseball:          '⚾ Baseball',
};

@Component({
  selector: 'app-match-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [DatePipe, FormsModule, MatchCardComponent, SkeletonMatchCardComponent],
  templateUrl: './match-list.component.html',
  styleUrl: './match-list.component.scss',
})
export class MatchListComponent implements OnInit {
  today = new Date();
  matches  = signal<Match[]>([]);
  loading  = signal(true);
  liveCount = signal(0);
  skeletonItems = Array.from({ length: 8 });

  selectedSport    = signal<string | 'all'>('all');
  selectedLeague   = signal<number | 'all'>('all');
  selectedCountry  = signal<string | 'all'>('all');
  selectedDate     = signal<string | null>(null);
  countrySearch    = signal('');
  countryDropdown  = signal(false);

  readonly PAGE_SIZE = 10;
  currentPage = signal(1);
  totalPages  = computed(() => Math.ceil(this.filteredMatches().length / this.PAGE_SIZE));

  sports = computed<string[]>(() => {
    const seen = new Set<string>();
    for (const m of this.matches()) if (m.sport) seen.add(m.sport);
    return Array.from(seen).sort();
  });

  sportLabel(sport: string): string {
    return SPORT_LABELS[sport] ?? sport;
  }

  leagues = computed<LeagueFilter[]>(() => {
    const seen = new Set<number>();
    const result: LeagueFilter[] = [];
    const sport = this.selectedSport();
    const src = sport === 'all' ? this.matches() : this.matches().filter(m => m.sport === sport);
    for (const m of src) {
      if (!seen.has(m.league.id)) {
        seen.add(m.league.id);
        result.push({ id: m.league.id, name: m.league.name });
      }
    }
    return result;
  });

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

  filteredMatches = computed<Match[]>(() => {
    let result = this.matches();

    const sport = this.selectedSport();
    if (sport !== 'all') result = result.filter(m => m.sport === sport);

    const league = this.selectedLeague();
    if (league !== 'all') result = result.filter(m => m.league.id === league);

    const country = this.selectedCountry();
    if (country !== 'all') result = result.filter(m =>
      m.home.countryName === country || m.away.countryName === country
    );

    const date = this.selectedDate();
    if (date) {
      result = result.filter(m => {
        const d  = m.date;
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const dd = String(d.getDate()).padStart(2, '0');
        return `${d.getFullYear()}-${mm}-${dd}` === date;
      });
    }

    return result.slice().sort((a, b) => {
      const order = (m: Match) => LIVE_STATUSES.has(m.status.short) ? 0 : m.status.short === 'NS' ? 1 : 2;
      const diff = order(a) - order(b);
      return diff !== 0 ? diff : a.date.getTime() - b.date.getTime();
    });
  });

  paginatedMatches = computed<Match[]>(() => {
    const start = (this.currentPage() - 1) * this.PAGE_SIZE;
    return this.filteredMatches().slice(start, start + this.PAGE_SIZE);
  });

  private destroyRef = inject(DestroyRef);

  constructor(private matchesService: MatchesService) {}

  ngOnInit() {
    // Chargement initial
    this.matchesService.getFixtures()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next:  data => { this.matches.set(data); this.loading.set(false); this._updateLiveCount(); },
        error: ()   => this.loading.set(false),
      });

    // Polling livescores toutes les 60 secondes
    interval(60_000).pipe(
      startWith(0),
      switchMap(() => this.matchesService.getLivescores()),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe(liveMatches => {
      if (liveMatches.length === 0) return;
      const liveMap = new Map(liveMatches.map(m => [m.id, m]));
      this.matches.update(all => all.map(m => liveMap.get(m.id) ?? m));
      this._updateLiveCount();
    });
  }

  private _updateLiveCount() {
    this.liveCount.set(this.matches().filter(m => LIVE_STATUSES.has(m.status.short)).length);
  }

  selectSport(sport: string | 'all') {
    this.selectedSport.set(sport);
    this.selectedLeague.set('all');
    this.currentPage.set(1);
  }
  selectLeague(id: number | 'all')   { this.selectedLeague.set(id);  this.currentPage.set(1); }
  selectCountry(c: string | 'all') {
    this.selectedCountry.set(c);
    this.countryDropdown.set(false);
    this.countrySearch.set('');
    this.currentPage.set(1);
  }

  isSportSelected(s: string | 'all')   { return this.selectedSport()   === s; }
  isLeagueSelected(id: number | 'all') { return this.selectedLeague()  === id; }
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
  clearDate()             { this.selectedDate.set(null); this.currentPage.set(1); }
  setDate(v: string|null) { this.selectedDate.set(v);   this.currentPage.set(1); }

  prevPage() { this.currentPage.update(p => Math.max(1, p - 1)); }
  nextPage() { this.currentPage.update(p => Math.min(this.totalPages(), p + 1)); }
}
