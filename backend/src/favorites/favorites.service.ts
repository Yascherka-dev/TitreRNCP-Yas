import { Injectable, NotFoundException } from '@nestjs/common';
import { SupabaseService } from '../supabase/supabase.service';
import { CreateFavoriteDto } from './dto/favorite.dto';

@Injectable()
export class FavoritesService {
  constructor(private supabase: SupabaseService) {}

  async findAll(userId: string) {
    const { data, error } = await this.supabase.db
      .from('favorites')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (error) throw new Error(error.message);
    return data ?? [];
  }

  async create(userId: string, dto: CreateFavoriteDto) {
    const { data, error } = await this.supabase.db
      .from('favorites')
      .insert({ user_id: userId, type: dto.type, reference_id: dto.referenceId })
      .select()
      .single();

    if (error) throw new Error(error.message);
    return data;
  }

  async remove(userId: string, favoriteId: string) {
    const { error } = await this.supabase.db
      .from('favorites')
      .delete()
      .eq('id', favoriteId)
      .eq('user_id', userId); // Sécurité : on ne supprime que ses propres favoris

    if (error) throw new NotFoundException('Favori introuvable');
    return { message: 'Favori supprimé' };
  }
}
