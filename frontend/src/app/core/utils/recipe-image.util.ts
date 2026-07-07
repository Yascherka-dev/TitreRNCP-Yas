import { Recipe } from '../models/recipe.model';

const SALE_IMGS  = [1, 2, 3, 4, 5, 6].map(n => `/assets/images/food/sale-0${n}.png`);
const SUCRE_IMGS = [1, 2, 3, 4, 5].map(n => `/assets/images/food/sucre-0${n}.png`);

/**
 * Image locale déterministe d'une recette (même id → même image).
 * Utilisée par la carte ET la modale pour garantir une image identique.
 */
export function localRecipeImage(recipe: Recipe): string {
  const pool = recipe.typePlat === 'sucré' ? SUCRE_IMGS : SALE_IMGS;
  const seed = Math.abs(recipe.id.split('').reduce((a, c) => a + c.charCodeAt(0), 0));
  return pool[seed % pool.length];
}
