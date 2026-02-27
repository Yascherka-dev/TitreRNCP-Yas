import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Anthropic from '@anthropic-ai/sdk';
import { SupabaseService } from '../supabase/supabase.service';
import { CreateSuggestionDto } from './dto/create-suggestion.dto';

export interface Recipe {
  title: string;
  country: string;
  countryCode: string;
  description: string;
  prepTime: number;   // en minutes
  servings: number;
  difficulty: 'Facile' | 'Moyen' | 'Difficile';
  ingredients: string[];
  steps: string[];
  tags: string[];
  imageQuery: string; // mot-clé pour Unsplash/image de recherche
}

export interface SuggestionResult {
  recipeA: Recipe;
  recipeB: Recipe;
}

@Injectable()
export class SuggestionsService {
  private anthropic: Anthropic;

  constructor(
    private config: ConfigService,
    private supabase: SupabaseService,
  ) {
    this.anthropic = new Anthropic({
      apiKey: this.config.getOrThrow<string>('ANTHROPIC_API_KEY'),
    });
  }

  async generateSuggestion(dto: CreateSuggestionDto): Promise<SuggestionResult> {
    // 1. Vérifier le cache Supabase si matchId fourni
    if (dto.matchId) {
      const cached = await this.getCached(dto.matchId);
      if (cached) return cached;
    }

    // 2. Appeler Claude pour générer les recettes
    const result = await this.callClaude(dto);

    // 3. Sauvegarder en base
    if (dto.matchId) {
      await this.saveSuggestion(dto, result);
    }

    return result;
  }

  private async getCached(matchId: number): Promise<SuggestionResult | null> {
    const { data } = await this.supabase.db
      .from('suggestions')
      .select('recipe_a, recipe_b')
      .eq('match_id', matchId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (!data) return null;
    return { recipeA: data.recipe_a as Recipe, recipeB: data.recipe_b as Recipe };
  }

  private async saveSuggestion(dto: CreateSuggestionDto, result: SuggestionResult) {
    await this.supabase.db.from('suggestions').insert({
      match_id: dto.matchId,
      home_country: dto.homeCountry,
      away_country: dto.awayCountry,
      recipe_a: result.recipeA,
      recipe_b: result.recipeB,
    });
  }

  private async callClaude(dto: CreateSuggestionDto): Promise<SuggestionResult> {
    const prompt = `Tu es un chef cuisinier expert en cuisine internationale et un passionné de football.

Pour le match ${dto.homeName} vs ${dto.awayName}, génère exactement 2 recettes :
- Recette A : inspirée de la cuisine du pays de ${dto.homeName} (code pays : ${dto.homeCountry})
- Recette B : inspirée de la cuisine du pays de ${dto.awayName} (code pays : ${dto.awayCountry})

Chaque recette doit être :
- Réalisable par un cuisinier amateur en soirée (pas trop complexe)
- Authentique et représentative de la cuisine du pays
- Adaptée pour 2-4 personnes

Réponds UNIQUEMENT avec un JSON valide, sans texte avant ou après, au format exact suivant :
{
  "recipeA": {
    "title": "Nom de la recette en français",
    "country": "Nom du pays en français",
    "countryCode": "${dto.homeCountry}",
    "description": "Description courte et appétissante (2 phrases max)",
    "prepTime": 45,
    "servings": 4,
    "difficulty": "Facile",
    "ingredients": ["200g de ...", "2 cuillères de ...", "..."],
    "steps": ["Étape 1 : ...", "Étape 2 : ...", "..."],
    "tags": ["viande", "traditionnel", "..."],
    "imageQuery": "mot-clé anglais pour recherche image du plat"
  },
  "recipeB": {
    "title": "...",
    "country": "...",
    "countryCode": "${dto.awayCountry}",
    "description": "...",
    "prepTime": 30,
    "servings": 4,
    "difficulty": "Moyen",
    "ingredients": ["..."],
    "steps": ["..."],
    "tags": ["..."],
    "imageQuery": "..."
  }
}`;

    const message = await this.anthropic.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 2048,
      messages: [{ role: 'user', content: prompt }],
    });

    const content = message.content[0];
    if (content.type !== 'text') {
      throw new InternalServerErrorException('Réponse Claude invalide');
    }

    try {
      // Extraire le JSON de la réponse (au cas où Claude ajoute du texte)
      const jsonMatch = content.text.match(/\{[\s\S]*\}/);
      if (!jsonMatch) throw new Error('Pas de JSON dans la réponse');
      return JSON.parse(jsonMatch[0]) as SuggestionResult;
    } catch {
      throw new InternalServerErrorException('Impossible de parser la réponse Claude');
    }
  }
}
