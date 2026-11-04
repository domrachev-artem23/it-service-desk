import { Component, inject, signal, OnInit } from '@angular/core';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Equipment } from '../../models/ticket';
@Component({ selector: 'app-equipment', templateUrl: './equipment.html' })
export class EquipmentPage implements OnInit {
  private readonly api = inject(TicketsApi);
  readonly items = signal<Equipment[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');
  ngOnInit() {
    this.load();
  }
  load() {
    this.loading.set(true);
    this.error.set('');
    this.api.equipment().subscribe({
      next: (data) => {
        this.items.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }
}
