import { Component, signal, inject, ChangeDetectionStrategy } from '@angular/core';
import { Router, NavigationEnd, RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { filter } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { AuthService } from './core/services/auth.service';
import { FavoritesService } from './core/services/favorites.service';
import { BottomTabBarComponent } from './shared/components/bottom-tab-bar/bottom-tab-bar.component';
import { SiteFooterComponent } from './shared/components/site-footer/site-footer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, MatButtonModule, MatIconModule, BottomTabBarComponent, SiteFooterComponent],
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
      .pipe(filter(e => e instanceof NavigationEnd), takeUntilDestroyed())
      .subscribe((e: NavigationEnd) => {
        this.isLanding.set(e.urlAfterRedirects === '/');
      });

    if (this.authService.isLoggedIn()) {
      this.favoritesService.loadFavorites().subscribe();
    }
  }
}
