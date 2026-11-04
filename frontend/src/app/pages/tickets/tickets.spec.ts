import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { beforeEach, afterEach, describe, expect, it } from 'vitest';
import { Tickets } from './tickets';
describe('Ticket list states', () => {
  let http: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [Tickets],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
    });
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => http.verify());
  function setup() {
    const fixture = TestBed.createComponent(Tickets);
    fixture.detectChanges();
    return fixture;
  }
  it('shows loading then empty result', () => {
    const f = setup();
    expect(f.nativeElement.textContent).toContain('Загружаем');
    http.expectOne((r) => r.url === '/api/tickets').flush([]);
    f.detectChanges();
    expect(f.nativeElement.querySelector('[data-testid="empty-state"]').textContent).toContain(
      'заявок нет',
    );
  });
  it('shows server error and supports retry', () => {
    const f = setup();
    http
      .expectOne((r) => r.url === '/api/tickets')
      .flush({ error: { message: 'База недоступна' } }, { status: 503, statusText: 'Unavailable' });
    f.detectChanges();
    expect(f.nativeElement.textContent).toContain('База недоступна');
    f.nativeElement.querySelector('[role="alert"] button').click();
    f.detectChanges();
    http.expectOne((r) => r.url === '/api/tickets').flush([]);
    f.detectChanges();
    expect(f.nativeElement.querySelector('[role="alert"]')).toBeNull();
  });
  it('cancels an older request when filter changes', () => {
    const f = setup();
    const old = http.expectOne((r) => r.url === '/api/tickets');
    f.componentInstance.setFilter('new');
    expect(old.cancelled).toBe(true);
    const latest = http.expectOne((r) => r.params.get('status') === 'new');
    latest.flush([]);
  });
});
