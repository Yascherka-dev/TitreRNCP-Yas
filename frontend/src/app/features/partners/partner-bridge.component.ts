import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { Partner, findPartner } from '../../core/data/partners.constant';
import { Match } from '../../core/models/fixture.model';
import { MatchSuggestion } from '../../core/models/recipe.model';
import { MatchesService } from '../../core/services/matches.service';
import { SuggestionsService } from '../../core/services/suggestions.service';

/**
 * Page-relais vers un partenaire.
 *
 * Les partenariats sont fictifs. Cette page le dit explicitement plutôt que
 * d'imiter le site du partenaire : elle reste dans l'identité Match & Munch et
 * rappelle le match concerné, pour que le parcours ne s'arrête pas dans le vide.
 */
@Component({
  selector: 'app-partner-bridge',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink, DatePipe],
  templateUrl: './partner-bridge.component.html',
  styleUrl: './partner-bridge.component.scss',
})
export class PartnerBridgeComponent {
  private readonly route       = inject(ActivatedRoute);
  private readonly matches     = inject(MatchesService);
  private readonly suggestions = inject(SuggestionsService);
  private readonly destroyRef  = inject(DestroyRef);

  readonly partner = signal<Partner | undefined>(undefined);
  readonly match   = signal<Match | null>(null);
  readonly menu    = signal<MatchSuggestion | null>(null);

  /** Les deux plats du soir, pour les partenaires livraison. */
  readonly dishes = computed<string[]>(() => {
    const m = this.menu();
    if (!m) return [];
    return [m.recetteA?.title, m.recetteB?.title].filter((t): t is string => !!t);
  });

  constructor() {
    this.partner.set(findPartner(this.route.snapshot.paramMap.get('slug')));

    const matchId = this.route.snapshot.queryParamMap.get('match');
    if (!matchId) return;

    this.matches.getFixtureById(matchId)
      .pipe(catchError(() => of(undefined)), takeUntilDestroyed(this.destroyRef))
      .subscribe(match => {
        if (!match) return;
        this.match.set(match);
        this.loadMenu(match);
      });
  }

  /** Le menu n'est utile qu'aux partenaires livraison : on l'évite ailleurs. */
  private loadMenu(match: Match): void {
    if (this.partner()?.kind !== 'food') return;

    this.suggestions
      .getSuggestion(match.id, match.home.countryCode, match.away.countryCode, match.home.name, match.away.name)
      .pipe(catchError(() => of(null)), takeUntilDestroyed(this.destroyRef))
      .subscribe(menu => this.menu.set(menu));
  }
}
