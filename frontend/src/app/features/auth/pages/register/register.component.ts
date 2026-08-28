import { Component, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';


/**
 * Rassemble les messages d'erreur renvoyés par l'API.
 *
 * DRF répond par champ — {password: ["..."], prenom: ["..."]}. L'ancienne
 * version ne lisait que `email` et `detail` : une erreur sur le mot de passe
 * ou le prénom devenait « Une erreur est survenue », et la personne ne savait
 * pas quoi corriger.
 */
function messageDErreur(err: unknown): string {
  const DEFAUT = "Une erreur est survenue. Vérifiez vos informations et réessayez.";
  const corps = (err as { error?: unknown })?.error;

  if (typeof corps === 'string') return corps || DEFAUT;
  if (!corps || typeof corps !== 'object') return DEFAUT;

  const champs = corps as Record<string, unknown>;
  if (typeof champs['detail'] === 'string') return champs['detail'];

  const messages = Object.values(champs)
    .flatMap(valeur => Array.isArray(valeur) ? valeur : [valeur])
    .filter((m): m is string => typeof m === 'string' && m.trim() !== '');

  return messages.length ? messages.join(' ') : DEFAUT;
}

@Component({
  selector: 'app-register',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private router      = inject(Router);

  // Les 4 champs du formulaire, liés au HTML via [(ngModel)]
  email    = '';
  password = '';
  nom      = '';
  prenom   = '';
  showPw   = false;

  // Signal pour désactiver le bouton pendant l'appel API
  loading = signal(false);

  // Signal pour afficher l'erreur retournée par le backend
  error = signal('');

  onSubmit() {
    this.loading.set(true);
    this.error.set('');

    this.authService.register(this.email, this.password, this.nom, this.prenom)
      .subscribe({
        next: () => {
          // Compte créé → on redirige vers la page de connexion
          this.router.navigate(['/login']);
        },
        error: (err) => {
          this.error.set(messageDErreur(err));
          this.loading.set(false);
        },
      });
  }
}
