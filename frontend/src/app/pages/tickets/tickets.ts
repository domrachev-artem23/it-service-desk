import { Component, computed, signal } from '@angular/core';
import { Ticket, TicketStatus } from '../../models/ticket';
import { DEMO_TICKETS } from '../../data/demo-tickets';
import { filterTickets, TicketFilter } from '../../features/tickets/filter-tickets';

@Component({
  selector: 'app-tickets',
  templateUrl: './tickets.html',
  styleUrl: './tickets.css'
})
export class Tickets {
  // Используем DEMO_TICKETS (заглавными)
  readonly tickets = signal<Ticket[]>(DEMO_TICKETS);
  readonly filter = signal<TicketFilter>('all');
  readonly search = signal('');

  readonly visibleTickets = computed(() => {
    const currentTickets = this.tickets() || [];
    const currentFilter = this.filter() || 'all';
    
    // Фильтруем по статусу
    const base = filterTickets(currentTickets, currentFilter);
    
    // Фильтруем по поиску
    const query = (this.search() || '').trim().toLowerCase();
    if (!query) return base;
    
    return base.filter((ticket) => ticket.title.toLowerCase().includes(query));
  });

  readonly statusLabels: Record<TicketStatus, string> = {
    new: 'Новая',
    in_progress: 'В работе',
    closed: 'Закрыта'
  };

  setFilter(mode: TicketFilter): void {
    this.filter.set(mode);
  }

  setSearch(value: string): void {
    this.search.set(value);
  }
}