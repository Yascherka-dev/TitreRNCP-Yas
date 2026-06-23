import { Match } from '../models/fixture.model';

const LIVE_CODES     = new Set(['1H', '2H', 'HT', 'ET', 'P', 'BT', 'LIVE']);
const FINISHED_CODES = new Set(['FT', 'AET', 'PEN']);

/**
 * Retourne le statut effectif d'un match.
 * Si le backend renvoie NS mais que le match a commencé depuis moins de 130 min,
 * on infère qu'il est en cours (l'API de livescore n'est pas toujours temps réel).
 */
export function inferStatus(match: Match): string {
  const s = match.status.short;

  if (LIVE_CODES.has(s) || FINISHED_CODES.has(s)) return s;
  if (s !== 'NS') return s; // PST, CANC, ABD…

  const elapsedMs = Date.now() - match.date.getTime();
  if (elapsedMs <= 0)                      return 'NS';   // pas encore commencé
  if (elapsedMs >= 130 * 60 * 1000)        return 'FT';   // > 2h10 → probablement terminé
  return 'LIVE';                                           // dans la fenêtre → en cours
}

export function isEffectivelyLive(match: Match): boolean {
  return LIVE_CODES.has(inferStatus(match));
}
