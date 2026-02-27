import { ApiPropertyOptional } from '@nestjs/swagger';
import { IsDateString, IsOptional } from 'class-validator';

export class GetMatchesDto {
  @ApiPropertyOptional({
    example: '2026-02-27',
    description: 'Date des matchs (YYYY-MM-DD). Par défaut : aujourd\'hui.',
  })
  @IsOptional()
  @IsDateString()
  date?: string;
}
