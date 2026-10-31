# Публикация учебного шаблона

Этот каталог — корень будущего репозитория. В нём находятся README.md, frontend, backend,
database, материалы ЛР4, тесты и методички. Решений преподавателя здесь нет.

1. Создайте на GitHub новый пустой репозиторий, например it-service-desk-template.
   Не добавляйте автоматически README, лицензию или .gitignore: README и .gitignore уже есть.
2. Откройте терминал в распакованной папке it-service-desk и выполните:

```bash
git init -b main
git add .
git commit -m "Initial laboratory template"
git remote add origin https://github.com/OWNER/it-service-desk-template.git
git push -u origin main
```

Замените OWNER своим именем на GitHub, а имя репозитория — фактическим.
Для push авторизуйтесь своим способом доступа к GitHub. Пароль/токен в файлы проекта не записывайте.
Загружается содержимое папки, а не ZIP-архив как один файл.

3. Выдайте студентам ссылку. При работе через шаблон студент создаёт личную копию,
   затем выполняет команды из ЛР1 с URL своего репозитория:

```bash
git clone https://github.com/STUDENT/it-service-desk.git it-service-desk
cd it-service-desk
git switch -c course
```

Далее — окружение Python, зависимости и Angular по методичке. ЛР2–4 выполняются в той же копии.
Исходные приёмочные тесты TODO-функций ожидаемо не проходят до выполнения заданий.
Workflow запускает сборку и стартовые тесты frontend, а не все проверки незавершённых ЛР.
