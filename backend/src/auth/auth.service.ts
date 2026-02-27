import { Injectable, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { SupabaseService } from '../supabase/supabase.service';
import { RegisterDto, LoginDto } from './dto/auth.dto';

@Injectable()
export class AuthService {
  constructor(private supabase: SupabaseService) {}

  async register(dto: RegisterDto) {
    const { data, error } = await this.supabase.db.auth.signUp({
      email: dto.email,
      password: dto.password,
    });

    if (error) throw new BadRequestException(error.message);

    return {
      user: data.user,
      session: data.session,
      message: 'Inscription réussie. Vérifiez votre email pour confirmer votre compte.',
    };
  }

  async login(dto: LoginDto) {
    const { data, error } = await this.supabase.db.auth.signInWithPassword({
      email: dto.email,
      password: dto.password,
    });

    if (error) throw new UnauthorizedException('Email ou mot de passe incorrect');

    return {
      user: data.user,
      session: data.session,
      accessToken: data.session?.access_token,
    };
  }

  async logout(token: string) {
    await this.supabase.db.auth.admin.signOut(token);
    return { message: 'Déconnexion réussie' };
  }
}
