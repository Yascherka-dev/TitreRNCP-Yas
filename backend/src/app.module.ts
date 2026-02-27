import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { SupabaseModule } from './supabase/supabase.module';
import { MatchesModule } from './matches/matches.module';
import { SuggestionsModule } from './suggestions/suggestions.module';
import { AuthModule } from './auth/auth.module';
import { FavoritesModule } from './favorites/favorites.module';

@Module({
  imports: [
    // ConfigModule global → process.env accessible partout via ConfigService
    ConfigModule.forRoot({ isGlobal: true }),
    // SupabaseModule global → SupabaseService injectable dans tous les modules
    SupabaseModule,
    MatchesModule,
    SuggestionsModule,
    AuthModule,
    FavoritesModule,
  ],
})
export class AppModule {}
