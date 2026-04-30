import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface PaletteItem {
  id: string;
  title: string;
  sub: string;
  kind: 'asset' | 'org' | 'tx';
}

interface SearchAsset { asset_id: string; name?: string; asset_type?: string; }
interface SearchOrg   { org_id: string; name?: string; type?: string; }
interface SearchTx    { tx_id: string; type?: string; }
interface SearchResponse {
  assets?: SearchAsset[];
  organizations?: SearchOrg[];
  transactions?: SearchTx[];
}

@Injectable({ providedIn: 'root' })
export class PaletteService {
  private base = environment.apiBase;
  readonly open$ = new BehaviorSubject(false);
  readonly items$ = new BehaviorSubject<PaletteItem[]>([]);
  readonly loading$ = new BehaviorSubject(false);

  constructor(private http: HttpClient) {}

  toggle(): void { this.open$.next(!this.open$.value); }
  close(): void  { this.open$.next(false); }

  async search(q: string): Promise<void> {
    if (!q.trim()) { this.items$.next([]); return; }
    this.loading$.next(true);
    try {
      const data = await this.http
        .get<SearchResponse>(`${this.base}/search`, { params: { q, limit: '20' } })
        .toPromise();

      const items: PaletteItem[] = [];
      (data?.assets ?? []).forEach(a =>
        items.push({ id: a.asset_id, title: a.name ?? a.asset_id, sub: a.asset_type ?? '', kind: 'asset' }));
      (data?.organizations ?? []).forEach(o =>
        items.push({ id: o.org_id, title: o.name ?? o.org_id, sub: o.type ?? '', kind: 'org' }));
      (data?.transactions ?? []).forEach(t =>
        items.push({ id: t.tx_id, title: t.tx_id, sub: t.type ?? '', kind: 'tx' }));
      this.items$.next(items);
    } catch {
      this.items$.next([]);
    } finally {
      this.loading$.next(false);
    }
  }
}
