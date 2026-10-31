import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Tickets } from './pages/tickets/tickets';
import { About } from './pages/about/about';
import { NotFound } from './pages/not-found/not-found';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'tickets', component: Tickets },
  { path: 'about', component: About },
  { path: '**', component: NotFound },   // wildcard строго последним
];