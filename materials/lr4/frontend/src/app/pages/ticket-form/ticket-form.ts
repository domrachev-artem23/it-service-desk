import { Component, inject, signal, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Equipment, TicketStatus } from '../../models/ticket';
@Component({
  selector: 'app-ticket-form',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './ticket-form.html',
})
export class TicketForm implements OnInit {
  private readonly api = inject(TicketsApi);
  private readonly fb = inject(FormBuilder);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  readonly id = Number(this.route.snapshot.paramMap.get('id')) || null;
  readonly equipment = signal<Equipment[]>([]);
  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly error = signal('');
  readonly loadError = signal('');
  readonly form = this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(120)]],
    equipmentId: [0, [Validators.min(1)]],
    description: ['', [Validators.maxLength(2000)]],
    status: ['new' as TicketStatus],
  });
  ngOnInit() {
    this.load();
  }
  load() {
    this.loading.set(true);
    this.loadError.set('');
    forkJoin({
      equipment: this.api.equipment(),
      ticket: this.id ? this.api.get(this.id) : of(null),
    }).subscribe({
      next: (data) => {
        this.equipment.set(data.equipment);
        if (data.ticket) this.form.patchValue(data.ticket);
        this.loading.set(false);
      },
      error: (err) => {
        this.loadError.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }
  save() {
    // TODO(LR4-04): валидация, POST/PATCH, блокировка повтора, переход или ошибка.
    this.error.set('Реализуйте сохранение по шагу LR4-04.');
  }
}
