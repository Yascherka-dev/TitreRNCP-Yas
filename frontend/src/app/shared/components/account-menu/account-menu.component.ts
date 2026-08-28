import {
  ChangeDetectionStrategy, Component, ElementRef, HostListener,
  computed, inject, signal,
} from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';

/**
 * Menu du compte connecté : l'initiale de l'utilisateur ouvre un panneau
 * proposant les paramètres et la déconnexion.
 *
 * Écrit sans Angular Material : le design system du projet réserve Material
 * aux composants historiques.
 */
@Component({
  selector: 'app-account-menu',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink],
  templateUrl: './account-menu.component.html',
  styleUrl: './account-menu.component.scss',
})
export class AccountMenuComponent {
  private auth   = inject(AuthService);
  private router = inject(Router);
  private hote: ElementRef<HTMLElement> = inject(ElementRef);

  ouvert = signal(false);

  prenom = computed(() => this.auth.currentUser()?.prenom ?? '');

  /** L'initiale affichée dans la pastille, à défaut une icône neutre. */
  initiale = computed(() => this.prenom().trim().charAt(0).toUpperCase());

  basculer(): void {
    this.ouvert.update(o => !o);
  }

  fermer(): void {
    this.ouvert.set(false);
  }

  seDeconnecter(): void {
    this.fermer();
    this.auth.logout();
    this.router.navigate(['/']);
  }

  /** Un clic hors du menu le referme, comme tout menu déroulant. */
  @HostListener('document:click', ['$event'])
  auClicExterieur(evenement: MouseEvent): void {
    if (this.ouvert() && !this.hote.nativeElement.contains(evenement.target as Node)) {
      this.fermer();
    }
  }

  /** Échap referme et rend le focus au déclencheur. */
  @HostListener('document:keydown.escape')
  aEchap(): void {
    if (this.ouvert()) {
      this.fermer();
      this.hote.nativeElement.querySelector<HTMLButtonElement>('.account-trigger')?.focus();
    }
  }
}
