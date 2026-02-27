import { Injectable, signal } from '@angular/core';
import { RecipeComment } from '../models/recipe.model';

// Service de gestion des avis et notes sur les recettes.
// Stockage local via Signals Angular 19 — sans persistance pour l'instant.
// À l'étape 11 MVP : remplacer par des appels HTTP vers le backend NestJS / Supabase.
@Injectable({ providedIn: 'root' })
export class RecipeReviewsService {

  // ── Stockage central ──────────────────────────────────────────────────────

  // Signal contenant tous les commentaires de toutes les recettes
  private allComments = signal<RecipeComment[]>([]);

  // Signal contenant les notes par recette — clé = recipeId, valeur = note 1-5
  private allRatings = signal<Record<string, number>>({});

  // ── Lecture ───────────────────────────────────────────────────────────────

  // Retourne les commentaires d'une recette donnée, triés du plus récent au plus ancien.
  // Conçu pour être appelé dans un `computed()` du composant → réactivité automatique.
  commentsFor(recipeId: string): RecipeComment[] {
    return this.allComments()
      .filter(c => c.recipeId === recipeId)
      .sort((a, b) => b.date.getTime() - a.date.getTime());
  }

  // Retourne la note enregistrée pour une recette (0 si jamais notée).
  ratingFor(recipeId: string): number {
    return this.allRatings()[recipeId] ?? 0;
  }

  // ── Écriture ──────────────────────────────────────────────────────────────

  // Enregistre ou met à jour la note d'une recette.
  setRating(recipeId: string, value: number): void {
    // `update` crée une nouvelle référence d'objet → Angular détecte le changement
    this.allRatings.update(ratings => ({ ...ratings, [recipeId]: value }));
  }

  // Ajoute un nouvel avis pour une recette.
  addComment(recipeId: string, content: string, rating: number): void {
    const comment: RecipeComment = {
      id: crypto.randomUUID(), // ID unique généré dans le navigateur
      recipeId,
      author: 'Vous',          // Remplacé par le vrai nom une fois l'auth branchée
      content: content.trim(),
      rating,
      date: new Date(),
    };
    this.allComments.update(list => [comment, ...list]);
  }
}
