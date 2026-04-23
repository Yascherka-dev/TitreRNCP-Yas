import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { Beer } from '../../../../core/models/recipe.model';

@Component({
  selector: 'app-beer-card',
  standalone: true,
  imports: [MatCardModule, MatIconModule, MatChipsModule],
  templateUrl: './beer-card.component.html',
  styleUrl: './beer-card.component.scss',
})
export class BeerCardComponent {
  beer = input.required<Beer>();
}
