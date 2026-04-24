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
      error: () => {
        this.error.set('Email ou mot de passe incorrect.');
        this.loading.set(false);
      },
    });
  }
}
