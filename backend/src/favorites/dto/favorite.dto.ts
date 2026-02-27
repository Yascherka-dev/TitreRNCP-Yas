import { ApiProperty } from '@nestjs/swagger';
import { IsIn, IsString, IsNotEmpty } from 'class-validator';

export class CreateFavoriteDto {
  @ApiProperty({ example: 'match', enum: ['match', 'recipe'] })
  @IsIn(['match', 'recipe'])
  type: 'match' | 'recipe';

  @ApiProperty({ example: '1001', description: 'ID du match ou de la recette' })
  @IsString()
  @IsNotEmpty()
  referenceId: string;
}
