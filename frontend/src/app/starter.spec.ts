import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { describe, expect, it } from 'vitest';
import { App } from './app';
import { Home } from './pages/home/home';
import { DEMO_TICKETS } from './data/demo-tickets';

describe('Исправность заготовки', () => {
  it('создаёт оболочку', async () => {
    await TestBed.configureTestingModule({imports: [App], providers: [provideRouter([])]})
      .compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('h1').textContent)
      .toContain('Сервис заявок ИТ-отдела');
  });
  it('показывает стартовую страницу', async () => {
    await TestBed.configureTestingModule({imports: [Home]}).compileComponents();
    const fixture = TestBed.createComponent(Home);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Заготовка проекта запущена');
  });
  it('содержит три заявки с уникальными идентификаторами', () => {
    expect(DEMO_TICKETS.length).toBe(3);
    expect(new Set(DEMO_TICKETS.map(item => item.id)).size).toBe(3);
  });
});
