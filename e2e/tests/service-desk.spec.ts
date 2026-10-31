import { test, expect } from '@playwright/test';

test('создание, сохранение после обновления, изменение статуса и удаление', async ({page, request}) => {
  const title = `Проверка E2E ${Date.now()}`;
  let ticketId: string | undefined;
  try {
    await page.goto('/tickets/new');
    await page.getByLabel('Название заявки').fill(title);
    await page.getByRole('combobox', {name:/Оборудование/}).selectOption({label:'PC-0204-01 · Рабочая станция Lenovo ThinkCentre'});
    await page.getByLabel('Описание проблемы').fill('Сквозная проверка сохранения данных');
    await page.getByRole('button', {name:'Сохранить заявку'}).click();
    await expect(page).toHaveURL(/\/tickets\/\d+$/);
    ticketId = page.url().split('/').at(-1);
    await expect(page.getByRole('heading', {name:title})).toBeVisible();
    await page.reload();
    await expect(page.getByRole('heading', {name:title})).toBeVisible();
    await page.getByRole('link', {name:'Редактировать', exact:true}).click();
    await page.getByLabel('Статус', {exact:true}).selectOption('closed');
    await page.getByRole('button', {name:'Сохранить заявку'}).click();
    await expect(page.locator('.page-heading .badge')).toHaveText('Закрыта');
    await expect(page.locator('.timeline')).toContainText('Статус: Новая → Закрыта');
    await page.getByRole('button', {name:'Удалить заявку', exact:true}).click();
    await page.getByRole('button', {name:'Подтвердить удаление'}).click();
    await expect(page).toHaveURL(/\/tickets$/);
    const response = await request.get(`/api/tickets/${ticketId}`);
    expect(response.status()).toBe(404);
    ticketId = undefined;
  } finally {
    if(ticketId) await request.delete(`/api/tickets/${ticketId}`);
  }
});

test('поиск, пустой результат и восстановление после сетевого сбоя', async ({page}) => {
  await page.goto('/tickets');
  await expect(page.getByTestId('ticket-row').first()).toBeVisible();
  await page.getByLabel('Поиск по заголовку').fill('такой-заявки-не-существует-xyz');
  await page.getByRole('button',{name:'Найти',exact:true}).click();
  await expect(page.getByTestId('empty-state')).toBeVisible();
  await page.route('**/api/tickets?**', route=>route.abort());
  await page.getByLabel('Поиск по заголовку').fill('');
  await page.getByRole('button',{name:'Найти',exact:true}).click();
  await expect(page.getByRole('alert')).toContainText('Нет связи');
  await page.unroute('**/api/tickets?**');
  await page.getByRole('button',{name:'Повторить'}).click();
  await expect(page.getByTestId('ticket-row').first()).toBeVisible();
});

test('валидация формы и неизвестный адрес', async ({page}) => {
  await page.goto('/tickets/new');
  await page.getByRole('button',{name:'Сохранить заявку'}).click();
  await expect(page.getByText('Введите название длиной')).toBeVisible();
  await expect(page.getByRole('alert').filter({hasText:'Выберите оборудование.'})).toBeVisible();
  await page.goto('/unknown-page');
  await expect(page.getByRole('heading',{name:'Страница не найдена'})).toBeVisible();
});
