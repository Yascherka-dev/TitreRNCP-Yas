import { Component, OnInit, signal, DestroyRef, inject, ChangeDetectionStrategy } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, EMPTY, of } from 'rxjs';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatDialog } from '@angular/material/dialog'; // service Angular Material pour ouvrir des dialogs
import { RecipeDialogComponent } from '../../../recipes/components/recipe-dialog/recipe-dialog.component'; // le dialog qu'on va ouvrir automatiquement
import { DatePipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatchesService } from '../../../../core/services/matches.service';
import { SuggestionsService } from '../../../../core/services/suggestions.service';
import { Match } from '../../../../core/models/fixture.model';
import { MatchSuggestion } from '../../../../core/models/recipe.model';
import { RecipeCardComponent } from '../../../recipes/components/recipe-card/recipe-card.component';
import { SkeletonRecipeCardComponent } from '../../../../shared/components/skeleton-recipe-card/skeleton-recipe-card.component';

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
    RecipeCardComponent,
    SkeletonRecipeCardComponent,
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
        this.suggestion.set(s); // on stocke la suggestion (les 2 recettes) dans le signal

        if (!s) return; // si la suggestion est vide on s'arrête là, rien à ouvrir

        // On lit le param ?recipe= dans l'URL (ex: "/matches/5?recipe=42" → donne "42")
        // queryParamMap = la map de tous les params de l'URL après le ?
        // .get('recipe') = on récupère spécifiquement la valeur du param "recipe"
        const recipeId = this.route.snapshot.queryParamMap.get('recipe');

        // Si le param n'existe pas dans l'URL (lien normal sans share) → on ne fait rien
        if (!recipeId) return;

        // On cherche dans les 2 recettes de la suggestion laquelle a cet id
        // String(r.id) = on convertit l'id en texte au cas où il serait un nombre, pour comparer avec recipeId qui est toujours un string
        const recette = [s.recipeA, s.recipeB].find(r => String(r.id) === recipeId);

        // Si aucune recette ne correspond à l'id (id invalide ou recette pas dans ce match) → on s'arrête
        if (!recette) return;

        // On ouvre le dialog avec la recette trouvée, exactement comme le fait RecipeCard
        this.dialog.open(RecipeDialogComponent, {
          data: recette,       // la recette complète passée au dialog
          maxWidth: '560px',   // largeur max sur desktop
          width: '95vw',       // largeur sur mobile (95% de la fenêtre)
          panelClass: 'recipe-dialog-panel', // classe CSS custom pour le style du dialog
        });
      });
  }

  onRegenerate() {
    const m = this.match();
    if (!m) return;
    this.regenerating.set(true);
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
