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

  if (FINISHED_CODES.has(s)) return s;

  const elapsedMs = Date.now() - match.date.getTime();

  // Statut live retourné par l'API : fiable seulement si < 130 min depuis le coup d'envoi
  if (LIVE_CODES.has(s)) {
    return elapsedMs >= 130 * 60 * 1000 ? 'FT' : s;
  }

  if (s !== 'NS') return s; // PST, CANC, ABD…

  if (elapsedMs <= 0)                return 'NS';
  if (elapsedMs >= 130 * 60 * 1000) return 'FT';
  return 'LIVE';
}

export function isEffectivelyLive(match: Match): boolean {
  return LIVE_CODES.has(inferStatus(match));
}
