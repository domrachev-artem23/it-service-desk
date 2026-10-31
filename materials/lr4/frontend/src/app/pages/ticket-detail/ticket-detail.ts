import { Component, inject, signal, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { forkJoin } from 'rxjs';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Ticket, TicketEvent, STATUS_LABELS } from '../../models/ticket';
@Component({
  selector: 'app-ticket-detail',
  imports: [RouterLink, DatePipe],
  templateUrl: './ticket-detail.html',
})
export class TicketDetail implements OnInit {
  private readonly api = inject(TicketsApi);
  private readonly router = inject(Router);
  readonly id = Number(inject(ActivatedRoute).snapshot.paramMap.get('id'));
  readonly ticket = signal<Ticket | null>(null);
  readonly events = signal<TicketEvent[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');
  readonly deleting = signal(false);
  readonly confirmDelete = signal(false);
  readonly deleteError = signal('');
  readonly labels = STATUS_LABELS;
  ngOnInit() {
    this.load();
  }
  load() {
    this.loading.set(true);
    this.error.set('');
    forkJoin({ ticket: this.api.get(this.id), events: this.api.events(this.id) }).subscribe({
      next: (data) => {
        this.ticket.set(data.ticket);
        this.events.set(data.events);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }
  remove() {
    if (this.deleting()) return;
    this.deleting.set(true);
    this.deleteError.set('');
    this.api.delete(this.id).subscribe({
      next: () => this.router.navigate(['/tickets']),
      error: (err) => {
        this.deleteError.set(errorMessage(err));
        this.deleting.set(false);
      },
    });
  }
}
