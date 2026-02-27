import { Injectable } from '@nestjs/common';
import { SupabaseService } from '../supabase/supabase.service';
import { CreateSuggestionDto } from './dto/create-suggestion.dto';

export interface Recipe {
  title: string;
  country: string;
  countryCode: string;
  description: string;
  prepTime: number;
  servings: number;
  difficulty: 'Facile' | 'Moyen' | 'Difficile';
  ingredients: string[];
  steps: string[];
  tags: string[];
  imageQuery: string;
}

export interface SuggestionResult {
  recipeA: Recipe;
  recipeB: Recipe;
}

// ── Banque de recettes mockées par code pays ──────────────────────────────────
// TODO: remplacer getMockRecipe() par callClaude() quand l'API key est disponible
const RECIPES: Record<string, Recipe> = {
  fr: {
    title: 'Bœuf Bourguignon',
    country: 'France',
    countryCode: 'fr',
    description:
      'Le grand classique de la cuisine française mijotée. Un bœuf fondant dans un vin rouge corsé, avec carottes et champignons.',
    prepTime: 40,
    servings: 4,
    difficulty: 'Moyen',
    ingredients: [
      '1 kg de bœuf à braiser (paleron)',
      '1 bouteille de vin rouge de Bourgogne',
      '200 g de lardons fumés',
      '300 g de champignons de Paris',
      '3 carottes',
      '2 oignons',
      '3 gousses d\'ail',
      '1 bouquet garni (thym, laurier, persil)',
      'Huile d\'olive, sel, poivre',
    ],
    steps: [
      'Couper le bœuf en cubes de 4 cm et les faire mariner 2h dans le vin rouge avec les légumes.',
      'Égoutter la viande, la faire revenir en cocotte avec l\'huile jusqu\'à coloration.',
      'Faire revenir les lardons et les légumes égouttés 5 min.',
      'Remettre la viande, mouiller avec la marinade filtrée, ajouter le bouquet garni.',
      'Couvrir et laisser mijoter à feu doux 2h30. Ajouter les champignons 30 min avant la fin.',
      'Ajuster l\'assaisonnement, servir avec des pommes de terre vapeur.',
    ],
    tags: ['viande', 'mijoté', 'classique', 'vin rouge'],
    imageQuery: 'beef bourguignon french stew',
  },
  de: {
    title: 'Schweinshaxe',
    country: 'Allemagne',
    countryCode: 'de',
    description:
      'La jarret de porc croustillante, star des brasseries bavaroises. Peau dorée et chair fondante, servie avec choucroute et moutarde.',
    prepTime: 30,
    servings: 2,
    difficulty: 'Facile',
    ingredients: [
      '2 jarrets de porc (1,5 kg)',
      '500 g de choucroute cuite',
      '2 oignons',
      '4 gousses d\'ail',
      '50 cl de bière blonde',
      '1 c.à.s de cumin',
      'Sel, poivre, huile',
      'Moutarde de Düsseldorf',
    ],
    steps: [
      'Préchauffer le four à 200°C. Quadriller la peau des jarrets avec un couteau.',
      'Frotter avec le sel, le poivre et le cumin. Faire dorer dans une cocotte huilée 10 min.',
      'Ajouter oignons et ail coupés en morceaux, déglacer avec la bière.',
      'Enfourner 2h en arrosant toutes les 20 min. Monter à 220°C les 15 dernières minutes pour croustiller la peau.',
      'Servir avec la choucroute réchauffée et de la moutarde.',
    ],
    tags: ['porc', 'brasserie', 'bavière', 'croustillant'],
    imageQuery: 'schweinshaxe roasted pork knuckle german',
  },
  es: {
    title: 'Paella Valenciana',
    country: 'Espagne',
    countryCode: 'es',
    description:
      'L\'emblème de la cuisine espagnole. Riz safrané, poulet, lapin et légumes cuits dans la traditionnelle poêle plate au feu de bois.',
    prepTime: 50,
    servings: 4,
    difficulty: 'Moyen',
    ingredients: [
      '400 g de riz à paella (bomba)',
      '1 poulet découpé en morceaux',
      '300 g de haricots verts plats',
      '200 g de haricots blancs cuits',
      '1 tomate mûre râpée',
      '1 pincée de safran',
      '1 c.à.c de paprika fumé',
      '1 L de bouillon de volaille',
      'Huile d\'olive, sel',
    ],
    steps: [
      'Faire chauffer l\'huile dans la paellera, faire revenir le poulet jusqu\'à dorure.',
      'Ajouter les haricots verts, faire revenir 5 min. Incorporer la tomate râpée.',
      'Ajouter le paprika, le safran infusé dans du bouillon chaud.',
      'Verser le riz, mélanger 2 min puis ajouter le bouillon chaud (2,5 fois le volume de riz).',
      'Cuire 18 min sans remuer. Laisser reposer 5 min couvert d\'aluminium avant de servir.',
    ],
    tags: ['riz', 'safran', 'traditionnel', 'sans gluten'],
    imageQuery: 'paella valenciana spanish rice',
  },
  'gb-eng': {
    title: 'Fish & Chips',
    country: 'Angleterre',
    countryCode: 'gb-eng',
    description:
      'Le plat national anglais par excellence. Filets de cabillaud en beignet doré et frites épaisses, servis avec sauce tartare et vinaigre de malt.',
    prepTime: 35,
    servings: 2,
    difficulty: 'Facile',
    ingredients: [
      '2 filets de cabillaud (200 g chacun)',
      '150 g de farine + 2 c.à.s pour paner',
      '25 cl de bière blonde bien froide',
      '1 c.à.c de levure chimique',
      '4 grosses pommes de terre à frire',
      'Huile de friture',
      'Vinaigre de malt, sel',
      'Sauce tartare (pour servir)',
    ],
    steps: [
      'Couper les pommes de terre en frites épaisses, les blanchir 5 min dans l\'eau bouillante.',
      'Préparer la pâte à beignets : mélanger la farine, la levure, la bière froide. Assaisonner.',
      'Sécher les filets, les fariner légèrement puis les tremper dans la pâte.',
      'Frire les frites à 160°C jusqu\'à cuisson, égoutter. Monter la friteuse à 180°C.',
      'Frire les poissons 4-5 min jusqu\'à dorure. Frire les frites une seconde fois pour les rendre croustillantes.',
      'Égoutter, saler immédiatement, servir avec vinaigre de malt et sauce tartare.',
    ],
    tags: ['poisson', 'friture', 'pub food', 'bière'],
    imageQuery: 'fish and chips english pub',
  },
  it: {
    title: 'Osso Buco alla Milanese',
    country: 'Italie',
    countryCode: 'it',
    description:
      'Le plat milanais par excellence. Jarret de veau braisé dans un bouillon de tomate et vin blanc, surmonté de gremolata citronnée.',
    prepTime: 35,
    servings: 4,
    difficulty: 'Moyen',
    ingredients: [
      '4 tranches de jarret de veau (4 cm d\'épaisseur)',
      '1 verre de vin blanc sec',
      '400 g de tomates concassées',
      '1 oignon, 1 carotte, 1 branche de céleri',
      '25 cl de bouillon de veau',
      'Farine, beurre, huile d\'olive',
      'Gremolata : zeste de citron, persil, 1 gousse d\'ail',
    ],
    steps: [
      'Fariner les tranches de jarret, les faire dorer au beurre et à l\'huile des deux côtés.',
      'Réserver la viande, faire revenir la brunoise d\'oignon, carotte, céleri dans la même cocotte.',
      'Déglacer au vin blanc, laisser réduire 2 min. Ajouter les tomates et le bouillon.',
      'Remettre la viande, couvrir, cuire à feu très doux 1h30 en retournant à mi-cuisson.',
      'Préparer la gremolata : mélanger zeste de citron, persil haché et ail émincé.',
      'Servir l\'osso buco avec le risotto milanais, parsemer de gremolata au moment de servir.',
    ],
    tags: ['veau', 'mijoté', 'milan', 'gremolata'],
    imageQuery: 'osso buco milanese italian veal',
  },
  pt: {
    title: 'Bacalhau à Brás',
    country: 'Portugal',
    countryCode: 'pt',
    description:
      'La recette de morue la plus célèbre du Portugal. Morue effilochée sautée avec des frites paille, des oignons et des œufs brouillés.',
    prepTime: 30,
    servings: 4,
    difficulty: 'Facile',
    ingredients: [
      '500 g de morue dessalée effilochée',
      '4 pommes de terre (frites paille)',
      '3 oignons émincés',
      '4 œufs',
      '3 gousses d\'ail',
      '50 g d\'olives noires',
      'Persil frais, huile d\'olive',
      'Sel, poivre',
    ],
    steps: [
      'Couper les pommes de terre en frites paille très fines et les frire jusqu\'à croustillant. Réserver.',
      'Dans une grande poêle, faire revenir les oignons et l\'ail dans l\'huile d\'olive jusqu\'à translucidité.',
      'Ajouter la morue effilochée, faire sauter 3 min. Incorporer les frites.',
      'Battre les œufs, les verser sur la préparation et remuer à feu doux comme des œufs brouillés.',
      'Retirer du feu avant que les œufs soient entièrement cuits (texture crémeuse).',
      'Parsemer d\'olives noires et de persil haché. Servir immédiatement.',
    ],
    tags: ['morue', 'traditionnel', 'rapide', 'œufs'],
    imageQuery: 'bacalhau bras portuguese codfish',
  },
  nl: {
    title: 'Stamppot Boerenkool',
    country: 'Pays-Bas',
    countryCode: 'nl',
    description:
      'Le plat réconfortant hollandais par excellence. Purée de pommes de terre mélangée au chou frisé, servie avec saucisse fumée.',
    prepTime: 30,
    servings: 4,
    difficulty: 'Facile',
    ingredients: [
      '1 kg de pommes de terre',
      '500 g de chou frisé (boerenkool)',
      '4 saucisses fumées (rookworst)',
      '100 ml de lait chaud',
      '50 g de beurre',
      'Moutarde, sel, poivre, noix de muscade',
    ],
    steps: [
      'Éplucher et couper les pommes de terre, les faire cuire dans l\'eau salée.',
      'Laver et couper grossièrement le chou frisé, l\'ajouter aux pommes de terre les 10 dernières minutes.',
      'Faire pocher les saucisses dans l\'eau frémissante 15 min.',
      'Égoutter pommes de terre et chou, écraser en purée avec le lait, le beurre et la noix de muscade.',
      'Servir dans les assiettes avec la saucisse fumée coupée en tranches et une touche de moutarde.',
    ],
    tags: ['légumes', 'réconfortant', 'hiver', 'végétarien-compatible'],
    imageQuery: 'stamppot boerenkool dutch kale mashed potatoes',
  },
  ar: {
    title: 'Tajine d\'Agneau aux Pruneaux',
    country: 'Argentine / Maghreb',
    countryCode: 'ar',
    description:
      'Un tajine sucré-salé parfumé aux épices chaudes. L\'agneau confit se mêle aux pruneaux moelleux et aux amandes grillées.',
    prepTime: 25,
    servings: 4,
    difficulty: 'Facile',
    ingredients: [
      '1 kg d\'épaule d\'agneau en morceaux',
      '200 g de pruneaux dénoyautés',
      '50 g d\'amandes mondées',
      '2 oignons émincés',
      '1 c.à.c de cannelle, gingembre, cumin',
      '1 c.à.s de miel',
      '25 cl de bouillon d\'agneau',
      'Huile d\'olive, sel, poivre',
    ],
    steps: [
      'Faire revenir l\'agneau dans l\'huile chaude jusqu\'à coloration, réserver.',
      'Faire revenir les oignons, ajouter les épices et mélanger 1 min.',
      'Remettre l\'agneau, ajouter le bouillon et le miel. Couvrir et mijoter 1h à feu doux.',
      'Ajouter les pruneaux, continuer la cuisson 30 min.',
      'Faire griller les amandes à sec dans une poêle.',
      'Servir dans le tajine, parsemer d\'amandes grillées. Accompagner de semoule.',
    ],
    tags: ['agneau', 'sucré-salé', 'épices', 'sans gluten'],
    imageQuery: 'moroccan lamb tagine prunes almonds',
  },
  br: {
    title: 'Feijoada',
    country: 'Brésil',
    countryCode: 'br',
    description:
      'Le plat national brésilien. Un ragoût de haricots noirs et viandes fumées servi avec du riz, farofa et orange.',
    prepTime: 30,
    servings: 6,
    difficulty: 'Moyen',
    ingredients: [
      '500 g de haricots noirs secs (trempés une nuit)',
      '300 g de saucisse chorizo / linguiça',
      '200 g de jarret de porc fumé',
      '150 g de lardons',
      '3 gousses d\'ail, 2 oignons',
      'Laurier, sel, poivre',
      'Riz blanc, oranges, farofa (pour servir)',
    ],
    steps: [
      'Faire cuire les haricots noirs trempés à la cocotte-minute 25 min.',
      'Faire revenir les lardons, ajouter oignons et ail émincés.',
      'Ajouter les viandes fumées coupées en morceaux, faire revenir 5 min.',
      'Incorporer les haricots cuits avec leur eau de cuisson, cuire encore 30 min à feu doux.',
      'Écraser quelques haricots pour épaissir la sauce.',
      'Servir avec du riz, des oranges tranchées et de la farofa.',
    ],
    tags: ['haricots', 'viandes fumées', 'national', 'consistant'],
    imageQuery: 'feijoada brazilian black beans stew',
  },
};

// Recette générique si le pays n'est pas dans la banque
const DEFAULT_RECIPE = (countryCode: string, countryName: string): Recipe => ({
  title: `Spécialité de ${countryName}`,
  country: countryName,
  countryCode,
  description: `Un plat traditionnel représentatif de la cuisine de ${countryName}, riche en saveurs locales et en histoire culinaire.`,
  prepTime: 45,
  servings: 4,
  difficulty: 'Moyen',
  ingredients: [
    'Ingrédients locaux de saison',
    'Épices et aromates typiques',
    'Huile ou matière grasse locale',
    'Protéine principale du pays',
    'Légumes de la région',
  ],
  steps: [
    'Préparer et couper tous les ingrédients.',
    'Faire revenir les aromates dans la matière grasse.',
    'Ajouter la protéine et faire dorer.',
    'Incorporer les légumes et épices, cuire à feu moyen.',
    'Ajuster l\'assaisonnement et servir chaud.',
  ],
  tags: ['traditionnel', 'local', 'découverte'],
  imageQuery: `traditional ${countryName} food dish`,
});

@Injectable()
export class SuggestionsService {
  constructor(private supabase: SupabaseService) {}

  async generateSuggestion(dto: CreateSuggestionDto): Promise<SuggestionResult> {
    // 1. Vérifier le cache Supabase si matchId fourni
    if (dto.matchId) {
      const cached = await this.getCached(dto.matchId);
      if (cached) return cached;
    }

    // 2. Récupérer les recettes mockées (→ Claude quand l'API key est disponible)
    const result = this.getMockSuggestion(dto);

    // 3. Sauvegarder en base pour le cache
    if (dto.matchId) {
      await this.saveSuggestion(dto, result);
    }

    return result;
  }

  private getMockSuggestion(dto: CreateSuggestionDto): SuggestionResult {
    const recipeA = RECIPES[dto.homeCountry] ?? DEFAULT_RECIPE(dto.homeCountry, dto.homeName);
    const recipeB = RECIPES[dto.awayCountry] ?? DEFAULT_RECIPE(dto.awayCountry, dto.awayName);
    return { recipeA, recipeB };
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

  // TODO: décommenter et utiliser cette méthode quand ANTHROPIC_API_KEY est disponible
  // private async callClaude(dto: CreateSuggestionDto): Promise<SuggestionResult> {
  //   const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  //   const message = await anthropic.messages.create({ ... });
  //   ...
  // }
}
