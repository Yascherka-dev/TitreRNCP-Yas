import { Body, Controller, Post, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { SuggestionsService } from './suggestions.service';
import { CreateSuggestionDto } from './dto/create-suggestion.dto';

@ApiTags('Suggestions')
@Controller('suggestions')
export class SuggestionsController {
  constructor(private readonly suggestionsService: SuggestionsService) {}

  @Post()
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Générer deux recettes pour un match' })
  @ApiResponse({ status: 200, description: 'Deux recettes générées par Claude' })
  @ApiResponse({ status: 400, description: 'Paramètres invalides' })
  generate(@Body() dto: CreateSuggestionDto) {
    return this.suggestionsService.generateSuggestion(dto);
  }
}
