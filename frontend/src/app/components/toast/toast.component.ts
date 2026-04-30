import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { Toast, ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: false,
  template: `
    <div class="toast"
      [class.show]="toast !== null"
      [class.ok]="toast?.type === 'ok'"
      [class.err]="toast?.type === 'err'"
      [class.warn]="toast?.type === 'warn'">
      {{ toast?.message }}
    </div>
  `
})
export class ToastComponent implements OnInit, OnDestroy {
  toast: Toast | null = null;
  private destroy$ = new Subject<void>();

  constructor(private toastService: ToastService) {}

  ngOnInit(): void {
    this.toastService.toast$
      .pipe(takeUntil(this.destroy$))
      .subscribe(t => this.toast = t);
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
