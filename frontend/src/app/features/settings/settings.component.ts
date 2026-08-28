import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

/**
 * Paramètres du compte, et exercice du droit à l'effacement.
 *
 * Les mentions légales annoncent que les données sont « supprimées avec le
 * compte » : la suppression est donc définitive et emporte favoris,
 * commentaires et notes.
 */
@Component({
  selector: 'app-settings',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FormsModule, RouterLink],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss',
})
export class SettingsComponent {
  private auth   = inject(AuthService);
  private router = inject(Router);

  utilisateur = computed(() => this.auth.currentUser());

  /** La zone de suppression reste repliée : on ne tombe pas dessus par hasard. */
  zoneOuverte  = signal(false);
  motDePasse   = signal('');
  suppression  = signal(false);
  erreur       = signal('');

  ouvrirLaZone(): void {
    this.zoneOuverte.set(true);
  }

  annuler(): void {
    this.zoneOuverte.set(false);
    this.motDePasse.set('');
    this.erreur.set('');
  }

  supprimer(): void {
    const motDePasse = this.motDePasse();
    if (!motDePasse) {
      this.erreur.set('Saisissez votre mot de passe pour confirmer.');
      return;
    }

    this.erreur.set('');
    this.suppression.set(true);

    this.auth.deleteAccount(motDePasse).subscribe({
      next: () => this.router.navigate(['/'], { replaceUrl: true }),
      error: (err) => {
        this.suppression.set(false);
        this.erreur.set(
          err?.error?.password?.[0]
          ?? "La suppression n'a pas pu aboutir. Réessayez dans un instant."
        );
      },
    });
  }
}
