import { Component, ChangeDetectionStrategy } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-skeleton-match-card',
  standalone: true,
  imports: [MatCardModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './skeleton-match-card.component.html',
  styleUrl: './skeleton-match-card.component.scss',
})
export class SkeletonMatchCardComponent {}
