import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

@Injectable()
export class SupabaseService {
  private client: SupabaseClient;

  constructor(private config: ConfigService) {
    this.client = createClient(
      this.config.getOrThrow<string>('SUPABASE_URL'),
      // service_role key côté backend — accès complet, contourne les RLS
      this.config.getOrThrow<string>('SUPABASE_SERVICE_KEY'),
    );
  }

  get db(): SupabaseClient {
    return this.client;
  }
}
