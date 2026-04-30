import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface User { id: string; email: string; role: string; }
export interface LoginResponse { mfa_required?: boolean; access_token?: string; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private base = environment.apiBase;

  readonly user$ = new BehaviorSubject<User | null>(null);
  readonly checked$ = new BehaviorSubject(false);

  constructor(private http: HttpClient) {}

  async hydrate(): Promise<void> {
    try {
      const user = await this.http.get<User>(`${this.base}/auth/me`).toPromise();
      this.user$.next(user ?? null);
    } catch {
      this.user$.next(null);
    } finally {
      this.checked$.next(true);
    }
  }

  async login(username: string, password: string, mfaToken?: string): Promise<LoginResponse> {
    const body: Record<string, string> = { username, password };
    if (mfaToken) body['mfa_token'] = mfaToken;

    const res = await this.http
      .post<LoginResponse>(`${this.base}/auth/login`, body)
      .toPromise();

    if (res?.mfa_required) return { mfa_required: true };
    await this.hydrate();
    return {};
  }

  async logout(): Promise<void> {
    try {
      await this.http.post(`${this.base}/auth/logout`, {}).toPromise();
    } catch {}
    this.user$.next(null);
  }
}
