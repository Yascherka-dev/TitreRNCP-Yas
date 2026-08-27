import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

/**
 * Mentions légales.
 *
 * Contenu strictement aligné sur ce que l'application collecte réellement
 * (voir apps/users/models.py) et sur son hébergement réel. Toute évolution du
 * modèle utilisateur doit se répercuter ici.
 */
@Component({
  selector: 'app-legal-notice',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink],
  templateUrl: './legal-notice.component.html',
  styleUrl: './legal-notice.component.scss',
})
export class LegalNoticeComponent {
  readonly updatedAt = 'août 2026';
}
