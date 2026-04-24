import { Component, OnInit, AfterViewInit, OnDestroy, ViewChild, ElementRef, signal, ChangeDetectionStrategy } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatchesService } from '../../core/services/matches.service';

interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  r: number; alpha: number;
}

@Component({
  selector: 'app-landing',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.scss',
})
export class LandingComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('particlesCanvas') canvasRef!: ElementRef<HTMLCanvasElement>;

  todayMatchCount = signal<number | null>(null);

  private animFrame = 0;
  private particles: Particle[] = [];
  private observer!: IntersectionObserver;

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

  ngAfterViewInit() {
    this.initParticles();
    this.initReveal();
  }

  ngOnDestroy() {
    cancelAnimationFrame(this.animFrame);
    this.observer?.disconnect();
  }

  private initParticles() {
    const canvas = this.canvasRef?.nativeElement;
    if (!canvas) return;
    const ctx = canvas.getContext('2d')!;

    const resize = () => {
      canvas.width  = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < 60; i++) {
      this.particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - .5) * .4,
        vy: (Math.random() - .5) * .4,
        r: Math.random() * 1.5 + .5,
        alpha: Math.random() * .4 + .1,
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const p of this.particles) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(244,128,26,${p.alpha})`;
        ctx.fill();
      }
      this.animFrame = requestAnimationFrame(draw);
    };
    draw();
  }

  private initReveal() {
    this.observer = new IntersectionObserver(
      entries => entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          this.observer.unobserve(e.target);
        }
      }),
      { threshold: 0.15 }
    );
    document.querySelectorAll('.reveal').forEach(el => this.observer.observe(el));
  }
}
