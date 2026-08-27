import { Component, input, computed, ChangeDetectionStrategy } from '@angular/core';
import { Beer } from '../../../../core/models/recipe.model';

const BEER_IMGS: Record<string, string> = {
  tulipe: '/assets/images/beer/beer-tulipe.webp',
  chope:  '/assets/images/beer/beer-chope.webp',
  ballon: '/assets/images/beer/beer-ballon.webp',
};

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

  beerImage = computed(() => {
    const style = (this.beer().style || '').toLowerCase();
    if (style.includes('ipa') || style.includes('pale') || style.includes('blonde') || style.includes('wheat') || style.includes('blanche')) {
      return BEER_IMGS['tulipe'];
    }
    if (style.includes('lager') || style.includes('pils') || style.includes('amber') || style.includes('ambrée')) {
      return BEER_IMGS['chope'];
    }
    return BEER_IMGS['ballon'];
  });
}
