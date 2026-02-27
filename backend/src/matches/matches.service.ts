import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { SupabaseService } from '../supabase/supabase.service';

const CACHE_TTL_HOURS = 23; // On garde le cache 23h (API-Football = 7 req/jour)

@Injectable()
export class MatchesService {
  private readonly logger = new Logger(MatchesService.name);

  constructor(
    private config: ConfigService,
    private supabase: SupabaseService,
  ) {}

  async getFixtures(date: string) {
    // 1. Vérifier le cache Supabase
    const cached = await this.getFromCache(date);
    if (cached) {
      this.logger.log(`Cache hit pour ${date}`);
      return cached;
    }

    // 2. Appeler API-Football
    this.logger.log(`Cache miss — appel API-Football pour ${date}`);
    const data = await this.fetchFromApiFootball(date);

    // 3. Stocker en cache
    await this.saveToCache(date, data);

    return data;
  }

  private async getFromCache(date: string) {
    const { data } = await this.supabase.db
      .from('matches_cache')
      .select('data, fetched_at')
      .eq('date', date)
      .single();

    if (!data) return null;

    const fetchedAt = new Date(data.fetched_at as string);
    const ageHours = (Date.now() - fetchedAt.getTime()) / (1000 * 60 * 60);

    // Cache expiré → retourner null pour forcer un nouvel appel
    if (ageHours > CACHE_TTL_HOURS) return null;

    return data.data;
  }

  private async saveToCache(date: string, data: unknown) {
    await this.supabase.db
      .from('matches_cache')
      .upsert({ date, data, fetched_at: new Date().toISOString() }, { onConflict: 'date' });
  }

  private async fetchFromApiFootball(date: string) {
    const apiKey = this.config.getOrThrow<string>('API_FOOTBALL_KEY');

    const response = await fetch(
      `https://v3.football.api-sports.io/fixtures?date=${date}`,
      {
        headers: {
          'x-rapidapi-host': 'v3.football.api-sports.io',
          'x-rapidapi-key': apiKey,
        },
      },
    );

    if (!response.ok) {
      throw new Error(`API-Football erreur : ${response.status}`);
    }

    const json = await response.json() as { response: unknown[] };
    // Retourner les fixtures brutes — le frontend les transforme déjà
    return json.response ?? [];
  }
}
