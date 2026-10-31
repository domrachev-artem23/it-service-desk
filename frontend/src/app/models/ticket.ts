export type TicketStatus = 'new' | 'in_progress' | 'closed';

export interface Ticket {
  id: number;
  equipmentId: number;
  title: string;
  description: string;
  status: TicketStatus;
}
