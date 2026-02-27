import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsNotEmpty, IsOptional, IsNumber } from 'class-validator';

export class CreateSuggestionDto {
  @ApiProperty({ example: 'fr', description: 'Code pays de l\'équipe domicile' })
  @IsString()
  @IsNotEmpty()
  homeCountry: string;

  @ApiProperty({ example: 'de', description: 'Code pays de l\'équipe extérieure' })
  @IsString()
  @IsNotEmpty()
  awayCountry: string;

  @ApiProperty({ example: 'France', description: 'Nom de l\'équipe domicile' })
  @IsString()
  @IsNotEmpty()
  homeName: string;

  @ApiProperty({ example: 'Allemagne', description: 'Nom de l\'équipe extérieure' })
  @IsString()
  @IsNotEmpty()
  awayName: string;

  @ApiProperty({ example: 1001, description: 'ID du match (optionnel pour le cache)', required: false })
  @IsOptional()
  @IsNumber()
  matchId?: number;
}
