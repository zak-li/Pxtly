import { Component, Input, AfterViewInit, OnDestroy } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    background: '#000000',
    primaryColor: '#4f8ffc',
    primaryTextColor: '#e6e8ef',
    lineColor: 'rgba(255,255,255,0.12)',
    fontSize: '12px',
  },
});

@Component({
  selector: 'app-mermaid-block',
  standalone: false,
  template: `
    <div class="mermaid-wrap">
      <div class="mermaid-header"><span class="mermaid-type">DIAGRAM</span></div>
      <div class="mermaid-body">
        <div class="mermaid-svg">
          <div *ngIf="safeSvg" [innerHTML]="safeSvg"></div>
          <pre *ngIf="error" class="mermaid-err">{{ error }}</pre>
        </div>
      </div>
    </div>
  `
})
export class MermaidBlockComponent implements AfterViewInit {
  @Input() code = '';
  safeSvg: SafeHtml | null = null;
  error = '';

  constructor(private sanitizer: DomSanitizer) {}

  async ngAfterViewInit(): Promise<void> {
    try {
      const id = 'mermaid-' + crypto.randomUUID();
      const { svg } = await mermaid.render(id, this.code);
      /* Mermaid produces trusted SVG — sanitize then mark safe for binding */
      this.safeSvg = this.sanitizer.bypassSecurityTrustHtml(svg);
    } catch (e: unknown) {
      this.error = e instanceof Error ? e.message : 'Render error';
    }
  }
}
