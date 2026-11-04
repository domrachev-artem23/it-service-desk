import { Component, inject, signal, OnInit, OnDestroy } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Subscription } from 'rxjs';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Ticket, STATUS_LABELS } from '../../models/ticket';
@Component({
  selector: 'app-tickets',
  imports: [RouterLink, FormsModule, DatePipe],
  templateUrl: './tickets.html',
})
export class Tickets implements OnInit, OnDestroy {
  private readonly api = inject(TicketsApi);
  private request?: Subscription;
  readonly tickets = signal<Ticket[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');
  readonly mode = signal('all');
  readonly labels = STATUS_LABELS;
  readonly filters = [
    { id: 'all', label: 'Все' },
    { id: 'open', label: 'Незакрытые' },
    { id: 'new', label: 'Новые' },
    { id: 'in_progress', label: 'В работе' },
    { id: 'closed', label: 'Закрытые' },
  ];
  query = '';
  ngOnInit() {
    this.load();
  }
  ngOnDestroy() {
    this.request?.unsubscribe();
  }
  setFilter(mode: string) {
    this.mode.set(mode);
    this.load();
  }
  load() {
    this.request?.unsubscribe();
    this.loading.set(true);
    this.error.set('');
    this.request = this.api.list(this.query, this.mode()).subscribe({
      next: (data) => {
        this.tickets.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }
}
