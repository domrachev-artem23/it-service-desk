import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { TicketForm } from './ticket-form';
describe('Ticket form', () => {
  let http: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [TicketForm],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
    });
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => http.verify());
  function setup() {
    const f = TestBed.createComponent(TicketForm);
    f.detectChanges();
    http
      .expectOne('/api/equipment')
      .flush([{ id: 101, name: 'PC', inventoryNumber: 'PC-1', location: 'Room' }]);
    f.detectChanges();
    return f;
  }
  it('does not send invalid or whitespace titles', () => {
    const f = setup();
    f.componentInstance.form.patchValue({ title: '   ', equipmentId: 101 });
    f.componentInstance.save();
    http.expectNone('/api/tickets');
    f.detectChanges();
    expect(f.nativeElement.textContent).toContain('Введите название');
  });
  it('prevents duplicate submits and preserves data on server error', () => {
    const f = setup();
    f.componentInstance.form.patchValue({
      title: '  Broken PC  ',
      equipmentId: 101,
      description: 'Details',
    });
    f.componentInstance.save();
    f.componentInstance.save();
    const req = http.expectOne('/api/tickets');
    expect(req.request.body.title).toBe('Broken PC');
    req.flush({ error: { message: 'Сбой записи' } }, { status: 503, statusText: 'Unavailable' });
    f.detectChanges();
    expect(f.componentInstance.form.controls.title.value).toBe('Broken PC');
    expect(f.componentInstance.saving()).toBe(false);
    expect(f.nativeElement.textContent).toContain('Сбой записи');
  });
});
