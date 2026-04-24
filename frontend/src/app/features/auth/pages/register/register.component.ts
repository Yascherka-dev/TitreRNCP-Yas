import { Component, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';

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
          // On affiche le premier message d'erreur du backend
          this.error.set(
            err.error?.email?.[0] ?? err.error?.detail ?? 'Une erreur est survenue.'
          );
          this.loading.set(false);
        },
      });
  }
}
