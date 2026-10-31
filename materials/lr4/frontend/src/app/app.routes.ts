import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Tickets } from './pages/tickets/tickets';
import { About } from './pages/about/about';
import { NotFound } from './pages/not-found/not-found';
import { EquipmentPage } from './pages/equipment/equipment';
import { TicketDetail } from './pages/ticket-detail/ticket-detail';
import { TicketForm } from './pages/ticket-form/ticket-form';
export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'tickets', component: Tickets },
  { path: 'tickets/new', component: TicketForm },
  { path: 'tickets/:id/edit', component: TicketForm },
  { path: 'tickets/:id', component: TicketDetail },
  { path: 'equipment', component: EquipmentPage },
  { path: 'about', component: About },
  { path: '**', component: NotFound },
];
