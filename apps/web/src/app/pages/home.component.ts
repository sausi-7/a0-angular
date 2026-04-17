import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of } from 'rxjs';

interface Health {
  status: string;
  env: string;
}

@Component({
  selector: 'a0-home',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <main class="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 class="text-4xl font-bold">A0 for Angular</h1>
      <p class="text-lg text-gray-600">Phase 0 — repo skeleton is live.</p>

      @if (health(); as h) {
        <p class="rounded bg-green-100 px-3 py-1 text-green-800">
          API: {{ h.status }} ({{ h.env }})
        </p>
      } @else {
        <p class="rounded bg-amber-100 px-3 py-1 text-amber-800">
          Waiting for API at {{ apiUrl }}…
        </p>
      }

      <a
        href="https://github.com/sausi-7/a0-angular"
        class="text-blue-600 underline"
        target="_blank"
        rel="noopener noreferrer"
      >
        Contribute on GitHub
      </a>
    </main>
  `,
})
export class HomeComponent {
  private readonly http = inject(HttpClient);
  readonly apiUrl = 'http://localhost:8000';

  readonly health = toSignal(
    this.http.get<Health>(`${this.apiUrl}/health`).pipe(
      map((h) => h),
      catchError(() => of(null)),
    ),
    { initialValue: null },
  );
}
