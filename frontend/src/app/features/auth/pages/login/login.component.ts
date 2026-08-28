import { Component, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router      = inject(Router);

  email    = '';
  password = '';
  showPw   = false;
  loading  = signal(false);
  error    = signal('');

  onSubmit() {
    this.loading.set(true);
    this.error.set('');

    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        // Connexion réussie → aller sur les matchs
        this.router.navigate(['/matches']);
      },
      error: (err) => {
        // 429 : la limite de tentatives est atteinte. Annoncer « mot de passe
        // incorrect » enverrait la personne corriger ce qui est peut-être juste.
        // Les autres cas restent volontairement vagues : préciser que l'email
        // est inconnu révélerait quels comptes existent.
        this.error.set(
          err?.status === 429
            ? "Trop de tentatives de connexion. Patientez quelques minutes avant de réessayer."
            : 'Email ou mot de passe incorrect.'
        );
        this.loading.set(false);
      },
    });
  }
}
