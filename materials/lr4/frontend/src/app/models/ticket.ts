export type TicketStatus = 'new' | 'in_progress' | 'closed';
export interface Ticket {
  id: number;
  equipmentId: number;
  title: string;
  description: string;
  status: TicketStatus;
  equipmentName?: string;
  inventoryNumber?: string;
  createdAt?: string;
  updatedAt?: string;
}
export interface Equipment {
  id: number;
  name: string;
  inventoryNumber: string;
  location: string;
}
export interface TicketInput {
  equipmentId: number;
  title: string;
  description: string;
}
export interface TicketEvent {
  id: number;
  action: string;
  message: string;
  createdAt: string;
}
export interface Stats {
  total: number;
  equipment: number;
  byStatus: Record<TicketStatus, number>;
}
export const STATUS_LABELS: Record<TicketStatus, string> = {
  new: 'Новая',
  in_progress: 'В работе',
  closed: 'Закрыта',
};
