import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export type EntityKind = 'asset' | 'org' | 'tx';

@Injectable({ providedIn: 'root' })
export class EntityService {
  private base = environment.apiBase;
  readonly open$ = new BehaviorSubject(false);
  readonly activeId$ = new BehaviorSubject<string | null>(null);
  readonly activeKind$ = new BehaviorSubject<EntityKind | null>(null);
  readonly detail$ = new BehaviorSubject<Record<string, unknown> | null>(null);
  readonly loading$ = new BehaviorSubject(false);
  readonly error$ = new BehaviorSubject<string | null>(null);

  constructor(private http: HttpClient) {}

  async open(id: string, kind: EntityKind): Promise<void> {
    this.open$.next(true);
    this.activeId$.next(id);
    this.activeKind$.next(kind);
    this.detail$.next(null);
    this.error$.next(null);
    this.loading$.next(true);

    const pathMap: Record<EntityKind, string> = {
      asset: `assets/${id}`,
      org:   `organizations/${id}`,
      tx:    `transactions/${id}`,
    };

    try {
      const data = await this.http
        .get<Record<string, unknown>>(`${this.base}/${pathMap[kind]}`)
        .toPromise();
      this.detail$.next(data ?? null);
    } catch (e: unknown) {
      this.error$.next(e instanceof Error ? e.message : 'Request failed');
    } finally {
      this.loading$.next(false);
    }
  }

  close(): void { this.open$.next(false); }
}
