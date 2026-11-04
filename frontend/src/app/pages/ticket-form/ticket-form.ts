import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { TicketsApi, errorMessage } from '../../services/tickets-api';
import { Equipment, Ticket, TicketStatus } from '../../models/ticket';

@Component({
  selector: 'app-ticket-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './ticket-form.html',
  styleUrl: './ticket-form.css',
})
export class TicketForm implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(TicketsApi);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly loading = signal(false);
  readonly loadError = signal('');
  readonly saving = signal(false);
  readonly error = signal('');
  readonly equipment = signal<Equipment[]>([]);

  id: number | null = null;

  readonly form = this.fb.group({
    title: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(120)]],
    description: ['', [Validators.maxLength(2000)]],
    equipmentId: [null as number | null, [Validators.required]],
    status: ['new' as TicketStatus],
  });

  ngOnInit(): void {
    this.id = Number(this.route.snapshot.paramMap.get('id')) || null;
    this.load();
  }

  load() {
    this.loading.set(true);
    this.loadError.set('');

    const ticket$ = this.id ? this.api.get(this.id) : of(null);

    forkJoin([this.api.equipment(), ticket$]).subscribe({
      next: ([equipment, ticket]) => {
        this.equipment.set(equipment);
        if (ticket) {
          this.form.patchValue({
            title: ticket.title,
            description: ticket.description,
            equipmentId: ticket.equipmentId,
            status: ticket.status,
          });
        }
        this.loading.set(false);
      },
      error: (err) => {
        this.loadError.set(errorMessage(err));
        this.loading.set(false);
      },
    });
  }

  save() {
    if (this.saving()) return;

    const value = this.form.getRawValue();
    this.form.controls.title.setValue(value.title!.trim());
    this.form.markAllAsTouched();

    if (this.form.invalid) return;

    const input = {
      title: value.title!.trim(),
      description: (value.description ?? '').trim(),
      equipmentId: Number(value.equipmentId),
    };

    this.saving.set(true);
    this.error.set('');

    const request = this.id
      ? this.api.update(this.id, { ...input, status: value.status! })
      : this.api.create(input);

    request.subscribe({
      next: (ticket) => {
        this.saving.set(false);
        this.router.navigate(['/tickets', ticket.id]);
      },
      error: (err) => {
        this.error.set(errorMessage(err));
        this.saving.set(false);
      },
    });
  }
}