-- Initial demo data. Execute once after schema.sql in a new database.
INSERT INTO equipment(id, name, inventory_number, location) VALUES
(101, 'Рабочая станция Lenovo ThinkCentre', 'PC-0204-01', 'Аудитория 204'),
(102, 'Проектор Epson EB-X49', 'PR-0301-01', 'Аудитория 301'),
(103, 'Коммутатор TP-Link TL-SG1024', 'NET-0101-01', 'Серверная'),
(104, 'Принтер HP LaserJet Pro', 'PRN-0200-01', 'Кабинет ИТ-отдела');

INSERT INTO tickets(id, equipment_id, title, description, status) VALUES
(1,101,'Не включается компьютер в аудитории 204','После нажатия кнопки питания индикаторы не горят.', 'new'),
(2,102,'Проектор не выводит изображение','Кабель подключён, источник сигнала выбран.', 'in_progress'),
(3,103,'Восстановить подключение к локальной сети','Подключение восстановлено после замены кабеля.','closed');

INSERT INTO ticket_events(ticket_id, action, message) VALUES
(1,'created','Учебная заявка загружена'),(2,'created','Учебная заявка загружена'),
(3,'created','Учебная заявка загружена');