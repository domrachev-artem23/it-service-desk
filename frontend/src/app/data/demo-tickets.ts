import { Ticket } from '../models/ticket';

export const DEMO_TICKETS: Ticket[] = [
  {
    id: 1,
    equipmentId: 101,
    title: 'Не включается компьютер в аудитории 204',
    description: 'После нажатия кнопки питания индикаторы не горят.',
    status: 'new',
  },
  {
    id: 2,
    equipmentId: 102,
    title: 'Проектор не выводит изображение',
    description: 'Кабель подключён, источник сигнала выбран.',
    status: 'in_progress',
  },
  {
    id: 3,
    equipmentId: 103,
    title: 'Восстановить подключение к локальной сети',
    description: 'Подключение восстановлено после замены кабеля.',
    status: 'closed',
  },
];
