import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { EntityKind, EntityService } from '../../services/entity.service';

@Component({
  selector: 'app-entity-panel',
  standalone: false,
  template: `
    <ng-container *ngIf="open">
      <div class="entity-overlay" (click)="entity.close()"></div>
      <div class="entity-panel">
        <div class="entity-head">
          <div class="entity-title-wrap">
            <span class="entity-kind-tag">{{ kind?.toUpperCase() }}</span>
            <span class="entity-title">{{ id }}</span>
          </div>
          <button class="entity-close" (click)="entity.close()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="entity-body">
          <div *ngIf="loading" class="entity-empty">Loading...</div>
          <div *ngIf="error" class="entity-empty entity-err">{{ error }}</div>
          <div *ngIf="detail && !loading" class="entity-table">
            <div class="entity-row" *ngFor="let entry of entries">
              <span class="entity-k">{{ entry.key }}</span>
              <span class="entity-v">{{ entry.value }}</span>
            </div>
          </div>
        </div>
      </div>
    </ng-container>
  `
})
export class EntityPanelComponent implements OnInit, OnDestroy {
  open = false;
  id: string | null = null;
  kind: EntityKind | null = null;
  detail: Record<string, unknown> | null = null;
  loading = false;
  error: string | null = null;
  entries: { key: string; value: string }[] = [];
  private destroy$ = new Subject<void>();

  constructor(public entity: EntityService) {}

  ngOnInit(): void {
    this.entity.open$.pipe(takeUntil(this.destroy$)).subscribe(v => this.open = v);
    this.entity.activeId$.pipe(takeUntil(this.destroy$)).subscribe(v => this.id = v);
    this.entity.activeKind$.pipe(takeUntil(this.destroy$)).subscribe(v => this.kind = v);
    this.entity.loading$.pipe(takeUntil(this.destroy$)).subscribe(v => this.loading = v);
    this.entity.error$.pipe(takeUntil(this.destroy$)).subscribe(v => this.error = v);
    this.entity.detail$.pipe(takeUntil(this.destroy$)).subscribe(d => {
      this.detail = d;
      this.entries = d
        ? Object.entries(d).map(([k, v]) => ({
            key: k,
            value: typeof v === 'object' ? JSON.stringify(v, null, 2) : String(v)
          }))
        : [];
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
