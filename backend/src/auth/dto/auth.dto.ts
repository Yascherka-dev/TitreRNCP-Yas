import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString, MinLength } from 'class-validator';

export class RegisterDto {
  @ApiProperty({ example: 'camille@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'motdepasse123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;
}

export class LoginDto {
  @ApiProperty({ example: 'camille@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'motdepasse123' })
  @IsString()
  password: string;
}
