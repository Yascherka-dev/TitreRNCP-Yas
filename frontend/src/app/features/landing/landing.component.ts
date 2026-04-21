import { Component, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatchesService } from '../../core/services/matches.service';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss',
})
export class LandingComponent implements OnInit {
  todayMatchCount = signal<number | null>(null);

  constructor(private matchesService: MatchesService) {}

  ngOnInit() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm   = String(today.getMonth() + 1).padStart(2, '0');
    const dd   = String(today.getDate()).padStart(2, '0');

    this.matchesService.getFixturesByDate(`${yyyy}-${mm}-${dd}`).subscribe(matches => {
      this.todayMatchCount.set(matches.length);
    });
  }
}
