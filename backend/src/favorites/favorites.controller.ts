import { Body, Controller, Delete, Get, Param, Post, Request, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { FavoritesService } from './favorites.service';
import { CreateFavoriteDto } from './dto/favorite.dto';
import { AuthGuard } from '../common/guards/auth.guard';

@ApiTags('Favorites')
@ApiBearerAuth()
@UseGuards(AuthGuard)  // Toutes les routes favoris nécessitent une auth
@Controller('favorites')
export class FavoritesController {
  constructor(private readonly favoritesService: FavoritesService) {}

  @Get()
  @ApiOperation({ summary: 'Lister mes favoris' })
  findAll(@Request() req: { user: { id: string } }) {
    return this.favoritesService.findAll(req.user.id);
  }

  @Post()
  @ApiOperation({ summary: 'Ajouter un favori' })
  create(@Request() req: { user: { id: string } }, @Body() dto: CreateFavoriteDto) {
    return this.favoritesService.create(req.user.id, dto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Supprimer un favori' })
  remove(@Request() req: { user: { id: string } }, @Param('id') id: string) {
    return this.favoritesService.remove(req.user.id, id);
  }
}
