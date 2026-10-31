import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', fullyParallel: false, workers: 1,
  timeout: 30000, expect: { timeout: 10000 },
  use: { baseURL: process.env.BASE_URL || 'http://localhost:4200',
    headless: true, screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  reporter: [['list'], ['html', {open: 'never'}]],
});
