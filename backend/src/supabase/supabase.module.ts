import { Global, Module } from '@nestjs/common';
import { SupabaseService } from './supabase.service';

// @Global() → SupabaseService injectable dans tous les modules sans réimport
@Global()
@Module({
  providers: [SupabaseService],
  exports: [SupabaseService],
})
export class SupabaseModule {}
