# Сервис заявок ИТ-отдела — учебный шаблон

## Начало работы

Создайте личный репозиторий из шаблона преподавателя (Use this template), затем:

```bash
git clone URL_ЛИЧНОГО_РЕПОЗИТОРИЯ it-service-desk
cd it-service-desk
git switch -c course
python -m venv backend/.venv
```

На macOS/Linux до активации может потребоваться команда python3 вместо python.
Активируйте окружение: macOS/Linux — `source backend/.venv/bin/activate`,
Windows PowerShell — `.\backend\.venv\Scripts\Activate.ps1`.

```bash
python -m pip install -r backend/requirements-dev.txt
cd frontend
npm ci
npm run check:starter
npm start
```

Требуются Git, Python 3.12 и Node.js 24.x. Angular устанавливается локально через npm ci,
глобальный ng и ng new не нужны. Версии зафиксированы lock-файлом.
MySQL 8.4 устанавливается в ЛР №3, браузер Playwright — в ЛР №4.


