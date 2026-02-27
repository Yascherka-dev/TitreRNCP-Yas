import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { SupabaseService } from '../../supabase/supabase.service';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private supabase: SupabaseService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers['authorization'];

    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedException('Token manquant ou invalide');
    }

    const token = authHeader.slice(7);

    const { data, error } = await this.supabase.db.auth.getUser(token);

    if (error || !data.user) {
      throw new UnauthorizedException('Session expirée ou invalide');
    }

    // Injecte le user dans la requête pour les controllers
    request.user = data.user;
    return true;
  }
}
