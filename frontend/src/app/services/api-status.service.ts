import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

interface AgentStatus { ready?: boolean; model?: string; provider?: string; }

@Injectable({ providedIn: 'root' })
export class ApiStatusService implements OnDestroy {
  private base = environment.apiBase;
  private intervalId: ReturnType<typeof setInterval>;

  readonly apiOk$ = new BehaviorSubject(false);
  readonly agentReady$ = new BehaviorSubject(false);
  readonly agentModel$ = new BehaviorSubject('');
  readonly agentProvider$ = new BehaviorSubject('');

  constructor(private http: HttpClient) {
    this.poll();
    this.intervalId = setInterval(() => this.poll(), 30_000);
  }

  private async poll(): Promise<void> {
    try {
      const [health, status] = await Promise.all([
        this.http.get(`${this.base}/health`).toPromise().then(() => true).catch(() => false),
        this.http.get<AgentStatus>(`${this.base}/agent/status`).toPromise().catch(() => null),
      ]);
      this.apiOk$.next(health as boolean);
      if (status) {
        this.agentReady$.next(status.ready ?? false);
        this.agentModel$.next(status.model ?? '');
        this.agentProvider$.next(status.provider ?? '');
      }
    } catch {
      this.apiOk$.next(false);
    }
  }

  ngOnDestroy(): void { clearInterval(this.intervalId); }
}
