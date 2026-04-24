import { Component, input, computed, ChangeDetectionStrategy } from '@angular/core';
import { Beer } from '../../../../core/models/recipe.model';

@Component({
  selector: 'app-beer-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [],
  templateUrl: './beer-card.component.html',
  styleUrl: './beer-card.component.scss',
})
export class BeerCardComponent {
  beer = input.required<Beer>();

  labelLine1 = computed(() => {
    const name = this.beer().brasserie || this.beer().nom;
    const words = name.split(' ');
    if (name.length <= 13 || words.length === 1) return name.slice(0, 13);
    return words.slice(0, Math.ceil(words.length / 2)).join(' ');
  });

  labelLine2 = computed(() => {
    const name = this.beer().brasserie || this.beer().nom;
    const words = name.split(' ');
    if (name.length <= 13 || words.length <= 1) return '';
    return words.slice(Math.ceil(words.length / 2)).join(' ');
  });
}
