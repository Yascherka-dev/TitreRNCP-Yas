import { Component, signal, inject } from '@angular/core';
import { Router, NavigationEnd, RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { filter } from 'rxjs/operators';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from './core/services/auth.service';
import { FavoritesService } from './core/services/favorites.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, MatButtonModule, MatIconModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  isLanding        = signal(true);
  authService      = inject(AuthService);
  favoritesService = inject(FavoritesService);

  constructor() {
    const router = inject(Router);
    router.events
      .pipe(filter(e => e instanceof NavigationEnd))
      .subscribe((e: NavigationEnd) => {
        this.isLanding.set(e.urlAfterRedirects === '/');
      });

    if (this.authService.isLoggedIn()) {
      this.favoritesService.loadFavorites().subscribe();
    }
  }
}
