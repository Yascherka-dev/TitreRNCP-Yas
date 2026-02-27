import { Module } from '@nestjs/common';
import { FavoritesController } from './favorites.controller';
import { FavoritesService } from './favorites.service';
import { AuthGuard } from '../common/guards/auth.guard';

@Module({
  controllers: [FavoritesController],
  providers: [FavoritesService, AuthGuard],
})
export class FavoritesModule {}
