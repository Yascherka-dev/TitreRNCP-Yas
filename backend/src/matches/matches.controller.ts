import { Controller, Get, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { MatchesService } from './matches.service';
import { GetMatchesDto } from './dto/get-matches.dto';

@ApiTags('Matches')
@Controller('matches')
export class MatchesController {
  constructor(private readonly matchesService: MatchesService) {}

  @Get()
  @ApiOperation({ summary: 'Récupérer les matchs du jour (avec cache 23h)' })
  @ApiResponse({ status: 200, description: 'Liste des fixtures API-Football' })
  getFixtures(@Query() query: GetMatchesDto) {
    const date = query.date ?? new Date().toISOString().split('T')[0];
    return this.matchesService.getFixtures(date);
  }
}
