import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { CsrfInterceptor } from '../interceptors/csrf.interceptor';
import { Opts } from './opts.service';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  stream?: boolean;
  responseTime?: number;
  promptTokens?: number;
  completionTokens?: number;
}

export interface ChatResponse {
  response?: string;
  message?: string;
  prompt_tokens?: number;
  completion_tokens?: number;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private base = environment.apiBase;
  readonly messages$ = new BehaviorSubject<Message[]>([]);
  readonly busy$ = new BehaviorSubject(false);

  /* CsrfInterceptor is injected only to read the token for the native
     fetch streaming call — HttpClient interceptors don't cover fetch(). */
  constructor(private csrf: CsrfInterceptor) {}

  clearMessages(): void {
    this.messages$.next([]);
  }

  async send(text: string, opts: Opts): Promise<void> {
    if (this.busy$.value) return;

    const userMsg: Message = { id: crypto.randomUUID(), role: 'user', content: text };
    this.messages$.next([...this.messages$.value, userMsg]);
    this.busy$.next(true);

    const assistantId = crypto.randomUUID();
    this.messages$.next([
      ...this.messages$.value,
      { id: assistantId, role: 'assistant', content: '', stream: opts.stream }
    ]);

    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      const token = this.csrf.getToken();
      if (token) headers['X-CSRF-Token'] = token;

      const t0 = Date.now();
      const res = await fetch(`${this.base}/agent/chat`, {
        method: 'POST',
        credentials: 'include',
        headers,
        body: JSON.stringify({ message: text, ...opts })
      });

      if (!res.ok) {
        const detail = await res.text().catch(() => '');
        throw new Error(`HTTP ${res.status}${detail ? ': ' + detail : ''}`);
      }

      if (opts.stream && res.body) {
        await this.consumeStream(assistantId, res.body, t0);
      } else {
        const data: ChatResponse = await res.json();
        this.patchAssistant(assistantId, {
          content: data.response ?? data.message ?? JSON.stringify(data),
          stream: false,
          promptTokens: data.prompt_tokens,
          completionTokens: data.completion_tokens,
        });
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Unknown error';
      this.patchAssistant(assistantId, { content: `Error: ${msg}`, stream: false });
    } finally {
      this.busy$.next(false);
    }
  }

  private async consumeStream(id: string, body: ReadableStream<Uint8Array>, t0: number): Promise<void> {
    const reader = body.getReader();
    const decoder = new TextDecoder();
    let buf = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        this.patchAssistant(id, { content: buf, stream: true });
      }
    } finally {
      reader.releaseLock();
    }

    const elapsed = parseFloat(((Date.now() - t0) / 1000).toFixed(2));
    this.patchAssistant(id, { content: buf, stream: false, responseTime: elapsed });
  }

  private patchAssistant(id: string, patch: Partial<Message>): void {
    const msgs = this.messages$.value.map(m => m.id === id ? { ...m, ...patch } : m);
    this.messages$.next(msgs);
  }
}
