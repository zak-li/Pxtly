import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS']);

@Injectable()
export class CsrfInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let cloned = req.clone({ withCredentials: true });

    if (!SAFE_METHODS.has(req.method)) {
      const token = this.getToken();
      if (token) {
        cloned = cloned.clone({ setHeaders: { 'X-CSRF-Token': token } });
      }
    }

    return next.handle(cloned);
  }

  getToken(): string | null {
    const match = document.cookie.match(/(?:^|;\s*)rwa_csrf=([^;]*)/);
    return match ? decodeURIComponent(match[1]) : null;
  }
}
