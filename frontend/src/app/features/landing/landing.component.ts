import { DatePipe } from '@angular/common';
import {
  AfterViewInit, ChangeDetectionStrategy, Component, DestroyRef,
  OnDestroy, computed, inject, signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { Match } from '../../core/models/fixture.model';
import { MatchSuggestion } from '../../core/models/recipe.model';
import { MatchesService } from '../../core/services/matches.service';
import { SuggestionsService } from '../../core/services/suggestions.service';
import { DEFAULT_SPORT, LANDING_SPORTS, SportKey } from './sports.constant';

@Component({
  selector: 'app-landing',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink, DatePipe],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss',
})
export class LandingComponent implements AfterViewInit, OnDestroy {
  private readonly matches     = inject(MatchesService);
  private readonly suggestions = inject(SuggestionsService);
  private readonly destroyRef  = inject(DestroyRef);

  private observer?: IntersectionObserver;

  readonly sports = LANDING_SPORTS;

  private readonly allMatches = signal<readonly Match[]>([]);

  readonly selectedSport     = signal<SportKey>(DEFAULT_SPORT);
  readonly loadingMatches    = signal(true);
  readonly loadingSuggestion = signal(false);
  readonly suggestion        = signal<MatchSuggestion | null>(null);

  /** Prochaine rencontre à venir dans le sport sélectionné. */
  readonly featured = computed<Match | null>(() => {
    const sport = this.selectedSport();
    const now   = Date.now();

    return this.allMatches()
      .filter(m => m.sport === sport && m.date.getTime() >= now)
      .sort((a, b) => a.date.getTime() - b.date.getTime())[0] ?? null;
  });

  /** « Confit de canard × Knödel », ou null si Marco n'a rien à proposer. */
  readonly menuLabel = computed<string | null>(() => {
    const menu = this.suggestion();
    if (!menu) return null;

    const titles = [menu.recetteA?.title, menu.recetteB?.title].filter(Boolean);
    return titles.length ? titles.join(' × ') : null;
  });

  constructor() {
    this.matches.getFixtures()
      .pipe(catchError(() => of([] as Match[])), takeUntilDestroyed(this.destroyRef))
      .subscribe(matches => {
        this.allMatches.set(matches);
        this.loadingMatches.set(false);
        this.loadSuggestion();
      });
  }

  ngAfterViewInit(): void {
    this.initReveal();
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }

  selectSport(key: SportKey): void {
    if (key === this.selectedSport()) return;
    this.selectedSport.set(key);
    this.loadSuggestion();
  }

  /**
   * Recettes de l'affiche mise en avant. SuggestionsService met déjà en cache
   * par match : revenir sur un sport déjà consulté ne relance aucune requête.
   */
  private loadSuggestion(): void {
    const match = this.featured();
    this.suggestion.set(null);

    if (!match) {
      this.loadingSuggestion.set(false);
      return;
    }

    this.loadingSuggestion.set(true);
    this.suggestions
      .getSuggestion(match.id, match.home.countryCode, match.away.countryCode, match.home.name, match.away.name)
      .pipe(catchError(() => of(null)), takeUntilDestroyed(this.destroyRef))
      .subscribe(suggestion => {
        this.suggestion.set(suggestion);
        this.loadingSuggestion.set(false);
      });
  }

  /** Révélation au scroll des sections « Comment ça marche » et bannière. */
  private initReveal(): void {
    this.observer = new IntersectionObserver(
      entries => entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          this.observer?.unobserve(e.target);
        }
      }),
      { threshold: 0.15 },
    );
    document.querySelectorAll('.reveal').forEach(el => this.observer!.observe(el));
  }
}
