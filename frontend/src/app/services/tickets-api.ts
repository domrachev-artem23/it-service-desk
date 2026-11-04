import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Equipment, Stats, Ticket, TicketEvent, TicketInput, TicketStatus } from '../models/ticket';

@Injectable({ providedIn: 'root' })
export class TicketsApi {
  private readonly http = inject(HttpClient);

  list(q = '', mode = 'all') {
    let params = new HttpParams().set('q', q.trim());
    if (mode === 'open') params = params.set('scope', 'open');
    if (mode === 'new' || mode === 'in_progress' || mode === 'closed') {
      params = params.set('status', mode);
    }
    return this.http.get<Ticket[]>('/api/tickets', { params });
  }

  get(id: number) {
    return this.http.get<Ticket>(`/api/tickets/${id}`);
  }

  create(input: TicketInput) {
    return this.http.post<Ticket>('/api/tickets', input);
  }

  update(id: number, input: TicketInput & { status: TicketStatus }) {
    return this.http.patch<Ticket>(`/api/tickets/${id}`, input);
  }

  delete(id: number) {
    return this.http.delete<void>(`/api/tickets/${id}`);
  }

  equipment() {
    return this.http.get<Equipment[]>('/api/equipment');
  }

  stats() {
    return this.http.get<Stats>('/api/stats');
  }

  events(id: number) {
    return this.http.get<TicketEvent[]>(`/api/tickets/${id}/events`);
  }
}

export function errorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 0) {
      return 'Нет связи с сервером. Проверьте подключение и повторите попытку.';
    }
    if (typeof error.error?.error?.message === 'string') {
      return error.error.error.message;
    }
  }
  return 'Не удалось выполнить запрос. Повторите попытку.';
}