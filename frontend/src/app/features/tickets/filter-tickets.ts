import { Ticket } from '../../models/ticket';

export type TicketFilter = 'all' | 'open' | 'new';

export function filterTickets(items: readonly Ticket[], mode: TicketFilter): Ticket[] {
  if (!items) return [];
  
  if (mode === 'all' || !mode) {
    return [...items]; 
  }
  if (mode === 'open') {
    return items.filter(ticket => ticket.status !== 'closed');
  }
  if (mode === 'new') {
    return items.filter(ticket => ticket.status === 'new');
  }
  return [];
}