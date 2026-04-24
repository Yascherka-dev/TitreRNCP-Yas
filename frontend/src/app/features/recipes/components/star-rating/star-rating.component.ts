import { Component, input, output, signal, ChangeDetectionStrategy } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-star-rating',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatIconModule],
  templateUrl: './star-rating.component.html',
  styleUrl: './star-rating.component.scss',
})
export class StarRatingComponent {

  value = input<number>(0);
  readonly = input<boolean>(false);
  ratingChange = output<number>();

  hovered = signal(0);
  stars = [1, 2, 3, 4, 5];

  select(star: number): void {
    if (!this.readonly()) this.ratingChange.emit(star);
  }

  onMouseEnter(star: number): void {
    if (!this.readonly()) this.hovered.set(star);
  }

  onMouseLeave(): void {
    if (!this.readonly()) this.hovered.set(0);
  }

  isFilled(star: number): boolean {
    return star <= (this.hovered() || this.value());
  }
}
