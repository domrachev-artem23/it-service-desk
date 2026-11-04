import { TestBed } from '@angular/core/testing';
import { provideHttpClient, HttpErrorResponse } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { TicketsApi, errorMessage } from './tickets-api';
describe('HTTP contract', () => {
  let api: TicketsApi;
  let http: HttpTestingController;
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    api = TestBed.inject(TicketsApi);
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => http.verify());
  it('encodes query and open scope', () => {
    api.list('  % printer  ', 'open').subscribe();
    const req = http.expectOne((r) => r.url === '/api/tickets');
    expect(req.request.params.get('q')).toBe('% printer');
    expect(req.request.params.get('scope')).toBe('open');
    req.flush([]);
  });
  it('uses POST without a client assigned id or status', () => {
    api.create({ title: 'Broken PC', equipmentId: 101, description: '' }).subscribe();
    const req = http.expectOne('/api/tickets');
    expect(req.request.method).toBe('POST');
    expect(req.request.body.status).toBeUndefined();
    expect(req.request.body.id).toBeUndefined();
    req.flush({ id: 4 });
  });
  it('uses DELETE and accepts no content', () => {
    api.delete(7).subscribe();
    const req = http.expectOne('/api/tickets/7');
    expect(req.request.method).toBe('DELETE');
    req.flush(null, { status: 204, statusText: 'No Content' });
  });
  it('distinguishes network and API errors', () => {
    expect(errorMessage(new HttpErrorResponse({ status: 0 }))).toContain('Нет связи');
    expect(
      errorMessage(
        new HttpErrorResponse({ status: 400, error: { error: { message: 'Проверьте поля' } } }),
      ),
    ).toBe('Проверьте поля');
  });
});
