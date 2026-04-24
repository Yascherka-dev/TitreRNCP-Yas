import {
  Component, input, signal, computed,
  OnInit, OnDestroy, inject, ChangeDetectionStrategy,
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

export type Token = string | { italic: string };

export interface ChefScript {
  chef: 'marco' | 'dolce';
  matchLabel: string;
  tokens: Token[];
  steps?: string[];
}

@Component({
  selector: 'app-marco-loader',
  standalone: true,
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="loader-wrap">
      <header class="head">
        <div class="avatar" [class.dolce]="script().chef === 'dolce'">
          {{ script().chef === 'dolce' ? 'D' : 'M' }}
        </div>
        <div class="meta">
          <div class="who">
            <span class="dot"></span>
            {{ script().chef === 'dolce' ? 'Dolce · pâtissière IA' : 'Marco · votre chef agent' }}
          </div>
          <div class="status" [innerHTML]="statusHtml()"></div>
        </div>
      </header>

      <div class="bubble">
        <span [innerHTML]="renderedText()"></span>
        <span class="cursor" [class.hidden]="done()"></span>
      </div>

      @if (script().steps?.length) {
        <ol class="steps">
          @for (s of script().steps!; track $index; let i = $index) {
            <li [class.done]="i < activeStep()"
                [class.active]="i === activeStep() && !done()">
              <span class="badge">{{ i < activeStep() ? '✓' : (i + 1) }}</span>
              {{ s }}
            </li>
          }
        </ol>
      }
    </div>
  `,
  styleUrl: './marco-loader.component.scss',
})
export class MarcoLoaderComponent implements OnInit, OnDestroy {
  script      = input.required<ChefScript>();
  autoRestart = input<boolean>(true);
  charDelayMs = input<number>(22);

  private readonly sanitizer = inject(DomSanitizer);

  private readonly built   = signal('');
  private readonly current = signal('');
  readonly done            = signal(false);

  readonly renderedText = computed<SafeHtml>(() =>
    this.sanitizer.bypassSecurityTrustHtml(this.built() + this.current())
  );

  readonly activeStep = computed(() => {
    const steps = this.script().steps;
    if (!steps?.length) return 0;
    const progress = this.totalLen() > 0 ? this.built().length / this.totalLen() : 0;
    return Math.min(Math.floor(progress * steps.length), steps.length - 1);
  });

  readonly statusHtml = computed(() => {
    const label = this.escape(this.script().matchLabel);
    return this.done()
      ? `servi pour <strong>${label}</strong> ✦`
      : `cuisine pour <strong>${label}</strong>…`;
  });

  private timer?: ReturnType<typeof setTimeout>;

  private totalLen(): number {
    return this.script().tokens.reduce(
      (n, t) => n + (typeof t === 'string' ? t.length : t.italic.length), 0
    );
  }

  ngOnInit()    { this.play(); }
  ngOnDestroy() { clearTimeout(this.timer); }

  play(): void {
    clearTimeout(this.timer);
    this.built.set('');
    this.current.set('');
    this.done.set(false);
    this.step(0, 0);
  }

  private step(tokenIdx: number, charIdx: number): void {
    const tokens = this.script().tokens;
    if (tokenIdx >= tokens.length) {
      this.done.set(true);
      if (this.autoRestart()) {
        this.timer = setTimeout(() => this.play(), 3200);
      }
      return;
    }

    const tok = tokens[tokenIdx];
    const raw = typeof tok === 'string' ? tok : tok.italic;

    if (charIdx < raw.length) {
      const piece = raw.slice(0, charIdx + 1);
      const html  = typeof tok === 'string'
        ? this.escape(piece)
        : `<em class="ital">${this.escape(piece)}</em>`;
      this.current.set(html);
      this.timer = setTimeout(
        () => this.step(tokenIdx, charIdx + 1),
        this.charDelayMs() + Math.random() * 20,
      );
    } else {
      this.built.update(b => b + (
        typeof tok === 'string'
          ? this.escape(raw)
          : `<em class="ital">${this.escape(raw)}</em>`
      ));
      this.current.set('');
      this.timer = setTimeout(() => this.step(tokenIdx + 1, 0), 75);
    }
  }

  private escape(s: string): string {
    return s.replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!)
    );
  }
}
