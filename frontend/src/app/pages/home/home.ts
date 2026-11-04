import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Stats, Ticket, STATUS_LABELS } from '../../models/ticket';
@Component({ selector: 'app-home', imports: [RouterLink], templateUrl: './home.html' })
export class Home implements OnInit {
  private readonly api = inject(TicketsApi);
  readonly stats = signal<Stats | null>(null);
  readonly recent = signal<Ticket[]>([]);
  readonly error = signal('');
  readonly loading = signal(true);
  readonly labels = STATUS_LABELS;
  ngOnInit() {
    this.load();
  }
  load() {
    this.loading.set(true);
    this.error.set('');
    forkJoin({ stats: this.api.stats(), tickets: this.api.list('', 'open') }).subscribe({
      next: (data) => {
        this.stats.set(data.stats);
        this.recent.set(data.tickets.slice(0, 4));
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }
}
