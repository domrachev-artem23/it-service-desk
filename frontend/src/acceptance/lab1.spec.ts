import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { describe, expect, it } from 'vitest';
import { App } from '../app/app';
import { routes } from '../app/app.routes';
import { Tickets } from '../app/pages/tickets/tickets';
import { DEMO_TICKETS } from '../app/data/demo-tickets';
import { filterTickets } from '../app/features/tickets/filter-tickets';

const ids = (items: ReturnType<typeof filterTickets>) => items.map(item => item.id);

describe('ЛР1: функция отбора', () => {
  it('all возвращает заявки 1, 2, 3', () => {
    expect(ids(filterTickets(DEMO_TICKETS, 'all'))).toEqual([1, 2, 3]);
  });
  it('open возвращает новые и находящиеся в работе', () => {
    expect(ids(filterTickets(DEMO_TICKETS, 'open'))).toEqual([1, 2]);
  });
  it('new возвращает только новые', () => {
    expect(ids(filterTickets(DEMO_TICKETS, 'new'))).toEqual([1]);
  });
  it('не меняет входные объекты или массив', () => {
    const input = Object.freeze(DEMO_TICKETS.map(item => Object.freeze({...item})));
    const before = JSON.stringify(input);
    filterTickets(input, 'open');
    expect(JSON.stringify(input)).toBe(before);
  });
  it('обрабатывает пустую коллекцию', () => {
    expect(filterTickets([], 'new')).toEqual([]);
  });
});

describe('ЛР1: страницы и меню', () => {
  for (const [path, heading] of [
    ['/home', 'Заготовка проекта запущена'],
    ['/tickets', 'Заявки на обслуживание'],
    ['/about', 'О системе'],
    ['/does-not-exist', 'Страница не найдена'],
  ]) {
    it(`открывает ${path}`, async () => {
      TestBed.configureTestingModule({providers: [provideRouter(routes)]});
      const harness = await RouterTestingHarness.create();
      await harness.navigateByUrl(path);
      expect(harness.routeNativeElement?.querySelector('h2')?.textContent).toContain(heading);
    });
  }
  it('содержит три навигационные ссылки', async () => {
    await TestBed.configureTestingModule({imports: [App], providers: [provideRouter(routes)]})
      .compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const links = [...root.querySelectorAll('nav a')].map(a => a.getAttribute('href'));
    expect(links).toEqual(['/home', '/tickets', '/about']);
  });
});

describe('ЛР1: интерфейс заявок', () => {
  async function setup() {
    await TestBed.configureTestingModule({imports: [Tickets]}).compileComponents();
    const fixture = TestBed.createComponent(Tickets);
    fixture.detectChanges();
    const root = fixture.nativeElement as HTMLElement;
    const cards = () => [...root.querySelectorAll('[data-testid="ticket-card"]')]
      .map(card => card.getAttribute('data-ticket-id'));
    const click = (mode: string) => {
      const button = root.querySelector<HTMLButtonElement>(`[data-testid="filter-${mode}"]`);
      if (!button) throw new Error(`Не найдена кнопка filter-${mode}`);
      button.click();
      fixture.detectChanges();
    };
    return {fixture, root, cards, click};
  }
  it('показывает данные всех заявок', async () => {
    const {root, cards} = await setup();
    expect(cards()).toEqual(['1','2','3']);
    for (const item of DEMO_TICKETS) {
      expect(root.textContent).toContain(item.title);
      expect(root.textContent).toContain(item.description);
    }
    expect(root.querySelector('[data-testid="ticket-count"]')?.textContent).toContain('3');
  });
  it('переключает open → new → all и обновляет счётчик', async () => {
    const {root, cards, click} = await setup();
    click('open'); expect(cards()).toEqual(['1','2']);
    expect(root.querySelector('[data-testid="ticket-count"]')?.textContent).toContain('2');
    click('new'); expect(cards()).toEqual(['1']);
    expect(root.querySelector('[data-testid="ticket-count"]')?.textContent).toContain('1');
    click('all'); expect(cards()).toEqual(['1','2','3']);
  });
  it('отмечает выбранную кнопку для средств доступности', async () => {
    const {root, click} = await setup();
    click('new');
    expect(root.querySelector('[data-testid="filter-new"]')?.getAttribute('aria-pressed'))
      .toBe('true');
    expect(root.querySelector('[data-testid="filter-all"]')?.getAttribute('aria-pressed'))
      .toBe('false');
  });
  it('объясняет пустой результат фильтра, исходная коллекция не пустая', async () => {
    const {fixture, root, cards, click} = await setup();
    fixture.componentInstance.tickets.set([DEMO_TICKETS[2]]);
    click('new');
    expect(cards()).toEqual([]);
    expect(root.querySelector('[data-testid="empty-state"]')?.textContent).toContain('заявок нет');
    expect(root.querySelector('[data-testid="ticket-count"]')?.textContent).toContain('0');
  });
});
