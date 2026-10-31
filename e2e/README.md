# Browser checks
Start the full application with MySQL before running these tests.
Use a dedicated demo environment: the CRUD scenario creates and removes a test ticket.
From e2e: npm ci; npx playwright install chromium; npm test.
Default target: http://127.0.0.1:4200. For Docker set BASE_URL=http://127.0.0.1:8080.
No mock database is used by the CRUD scenario. A separate test intentionally aborts
an HTTP request to verify the error message and retry button.
