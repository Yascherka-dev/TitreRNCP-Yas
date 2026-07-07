import { Component, OnInit, signal, computed, DestroyRef, inject, ChangeDetectionStrategy } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, EMPTY } from 'rxjs';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { RecipeDialogComponent } from '../../../recipes/components/recipe-dialog/recipe-dialog.component';
import { DatePipe } from '@angular/common';
import { MatchesService } from '../../../../core/services/matches.service';
import { SuggestionsService } from '../../../../core/services/suggestions.service';
import { Match } from '../../../../core/models/fixture.model';
import { MatchSuggestion } from '../../../../core/models/recipe.model';
import { RecipeCardComponent } from '../../../recipes/components/recipe-card/recipe-card.component';
import { BeerCardComponent } from '../../../beers/components/beer-card/beer-card.component';
import { MarcoLoaderComponent, ChefScript } from '../../../../shared/components/marco-loader/marco-loader.component';

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
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    DatePipe,
    RouterLink,
    RecipeCardComponent,
    BeerCardComponent,
    MarcoLoaderComponent,
  ],
  templateUrl: './match-detail.component.html',
  styleUrl: './match-detail.component.scss',
})
export class MatchDetailComponent implements OnInit {
  match           = signal<Match | null>(null);
  suggestion      = signal<MatchSuggestion | null>(null);
  suggestionError = signal(false);
  regenerating    = signal(false);
  loadingMsg      = signal('');

  recipeTab     = signal<'sale' | 'sucre'>('sale');
  beerTab       = signal<'a' | 'b'>('a');
  marcoFinished = signal(false);

  marcoLoadingScript = computed<ChefScript | null>(() => {
    const m = this.match();
    if (!m) return null;
    const domestic = m.home.countryName.toLowerCase() === m.away.countryName.toLowerCase();
    const labelA = domestic ? m.home.name : m.home.countryName;
    const labelB = domestic ? m.away.name : m.away.countryName;
    return {
      chef: 'marco',
      matchLabel: `${m.home.name} vs ${m.away.name}`,
      tokens: [
        '🍳 Marco explore les cuisines du monde… ',
        { italic: `${labelA} × ${labelB}` },
        ', ça sent bon par ici. Sélection des meilleures recettes en cours…',
      ],
      steps: ['Match reçu', 'Saveurs par pays', 'Recettes rédigées', 'À table'],
    };
  });

  marcoScript = computed<ChefScript | null>(() => {
    const m = this.match();
    const s = this.suggestion();
    if (!m || !s) return null;
    const domestic = m.home.countryName.toLowerCase() === m.away.countryName.toLowerCase();
    const labelA = domestic ? m.home.name : m.home.countryName;
    const labelB = domestic ? m.away.name : m.away.countryName;
    return {
      chef: 'marco',
      matchLabel: `${m.home.name} vs ${m.away.name}`,
      tokens: [
        'Allez, on allume le feu. ',
        { italic: `${labelA} × ${labelB}` },
        ', ça appelle du goût et des couleurs. Côté ',
        { italic: labelA }, ' : ',
        { italic: s.recetteA?.title ?? '…' },
        ' et en sucré, ',
        { italic: s.pecheMignonA?.title ?? '…' },
        '. Côté ',
        { italic: labelB }, ' : ',
        { italic: s.recetteB?.title ?? '…' },
        ' et ',
        { italic: s.pecheMignonB?.title ?? '…' },
        '. Je dresse les assiettes — ',
        { italic: 'bonne soirée.' },
      ],
      steps: ['Match reçu', 'Saveurs par pays', 'Recettes rédigées', 'À table'],
    };
  });

  private readonly LOADING_MSGS = [
    '🧑‍🍳 Marco est aux fourneaux...',
    '🌍 On explore les cuisines du monde...',
    '🔪 Sélection des meilleures recettes...',
    '🍷 Accord mets et match en cours...',
    '📖 Consultation du livre de recettes...',
  ];
  private msgTimer?: ReturnType<typeof setInterval>;

  foodPartners = FOOD_PARTNERS;
  streamingPartners = STREAMING_PARTNERS;

  private destroyRef = inject(DestroyRef);

  constructor(
    private route: ActivatedRoute,
    private matchesService: MatchesService,
    private suggestionsService: SuggestionsService,
    private dialog: MatDialog,
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id') ?? '';
    this.matchesService.getFixtureById(id).pipe(takeUntilDestroyed(this.destroyRef)).subscribe(m => {
      if (!m) return;
      this.match.set(m);
      this.loadSuggestion(m);
    });
  }

  private startLoadingMsgs() {
    this.loadingMsg.set(this.LOADING_MSGS[0]);
    let i = 1;
    this.msgTimer = setInterval(() => {
      this.loadingMsg.set(this.LOADING_MSGS[i % this.LOADING_MSGS.length]);
      i++;
    }, 2000);
  }

  private stopLoadingMsgs() {
    clearInterval(this.msgTimer);
  }

  loadSuggestion(m: Match) {
    this.suggestionError.set(false);
    this.startLoadingMsgs();
    this.suggestionsService
      .getSuggestion(m.id, m.home.countryCode, m.away.countryCode, m.home.name, m.away.name)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        catchError(() => {
          this.stopLoadingMsgs();
          this.suggestionError.set(true);
          return EMPTY;
        }),
      )
      .subscribe(s => {
        this.stopLoadingMsgs();
        this.suggestion.set(s);

        if (!s) return;

        // ?recipe= permet d'ouvrir directement une recette depuis un lien partagé
        const recipeId = this.route.snapshot.queryParamMap.get('recipe');
        if (!recipeId) return;

        const recette = [s.recetteA, s.recetteB, s.pecheMignonA, s.pecheMignonB]
          .filter(Boolean)
          .find(r => String(r!.id) === recipeId);

        if (!recette) return;

        this.dialog.open(RecipeDialogComponent, {
          data: recette,
          maxWidth: '560px',
          width: '95vw',
          panelClass: 'recipe-dialog-panel',
          backdropClass: 'mm-dialog-backdrop',
        });
      });
  }

  onRegenerate() {
    const m = this.match();
    if (!m) return;
    this.regenerating.set(true);
    this.marcoFinished.set(false);
    this.suggestion.set(null);

    this.suggestionError.set(false);
    this.startLoadingMsgs();
    this.suggestionsService
      .regenerate(m.id, m.home.countryCode, m.away.countryCode, m.home.name, m.away.name)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        catchError(() => {
          this.stopLoadingMsgs();
          this.regenerating.set(false);
          this.suggestionError.set(true);
          return EMPTY;
        }),
      )
      .subscribe(s => {
        this.stopLoadingMsgs();
        this.suggestion.set(s);
        this.regenerating.set(false);
      });
  }
}
