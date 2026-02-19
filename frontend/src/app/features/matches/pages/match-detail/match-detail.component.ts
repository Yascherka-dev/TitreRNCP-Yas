import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatchesService } from '../../../../core/services/matches.service';
import { SuggestionsService } from '../../../../core/services/suggestions.service';
import { Match } from '../../../../core/models/fixture.model';
import { MatchSuggestion } from '../../../../core/models/recipe.model';
import { RecipeCardComponent } from '../../../recipes/components/recipe-card/recipe-card.component';

interface PartnerLink {
  name: string;
  tagline: string;
  ctaLabel: string;
  url: string;
  color: string;
  emoji: string;
  badge?: string;
}

const FOOD_PARTNERS: PartnerLink[] = [
  {
    name: 'HelloFresh',
    tagline: 'Kit repas livré : ingrédients frais + recette étape par étape.',
    ctaLabel: 'Commander le kit',
    url: '#',
    color: '#6DB33F',
    emoji: '📦',
    badge: 'Partenaire',
  },
  {
    name: 'Uber Eats',
    tagline: 'Le plat déjà préparé, livré en moins de 30 min.',
    ctaLabel: 'Commander maintenant',
    url: '#',
    color: '#06C167',
    emoji: '🛵',
  },
  {
    name: 'Carrefour Drive',
    tagline: 'Tous les ingrédients en un clic, retrait en 2h.',
    ctaLabel: 'Faire mes courses',
    url: '#',
    color: '#004E9F',
    emoji: '🛒',
  },
];

const STREAMING_PARTNERS: PartnerLink[] = [
  {
    name: 'Canal+',
    tagline: 'Champions League, Ligue 1 — en direct et en exclusivité.',
    ctaLabel: 'Regarder le match',
    url: '#',
    color: '#000000',
    emoji: '📺',
    badge: 'Exclusif',
  },
  {
    name: 'beIN Sports',
    tagline: 'La Liga, Serie A et bien plus — live & replay.',
    ctaLabel: 'Accéder au direct',
    url: '#',
    color: '#D4002D',
    emoji: '⚽',
  },
  {
    name: 'DAZN',
    tagline: 'Le sport en streaming, sans engagement.',
    ctaLabel: 'Voir le match',
    url: '#',
    color: '#F8E220',
    emoji: '▶️',
  },
];

@Component({
  selector: 'app-match-detail',
  standalone: true,
  imports: [
    DatePipe,
    RouterLink,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    RecipeCardComponent,
  ],
  templateUrl: './match-detail.component.html',
  styleUrl: './match-detail.component.scss',
})
export class MatchDetailComponent implements OnInit {
  match = signal<Match | null>(null);
  suggestion = signal<MatchSuggestion | null>(null);
  regenerating = signal(false);

  foodPartners = FOOD_PARTNERS;
  streamingPartners = STREAMING_PARTNERS;

  constructor(
    private route: ActivatedRoute,
    private matchesService: MatchesService,
    private suggestionsService: SuggestionsService,
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.matchesService.getFixtureById(id).subscribe(m => {
      if (!m) return;
      this.match.set(m);
      this.loadSuggestion(m);
    });
  }

  loadSuggestion(m: Match) {
    this.suggestionsService
      .getSuggestion(m.id, m.home.countryCode, m.away.countryCode)
      .subscribe(s => this.suggestion.set(s));
  }

  onRegenerate() {
    const m = this.match();
    if (!m) return;
    this.regenerating.set(true);
    this.suggestion.set(null);

    // Simule un délai réseau (sera remplacé par l'appel réel à l'API Claude)
    setTimeout(() => {
      this.suggestionsService
        .regenerate(m.id, m.home.countryCode, m.away.countryCode)
        .subscribe(s => {
          this.suggestion.set(s);
          this.regenerating.set(false);
        });
    }, 800);
  }
}
