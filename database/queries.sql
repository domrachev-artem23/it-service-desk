-- Examples for LR3, on the selected service_desk database.
-- JOIN: a ticket is linked to its equipment.
SELECT t.id, t.title, e.name, e.inventory_number
FROM tickets t JOIN equipment e ON e.id=t.equipment_id;

-- Aggregation for the overview page.
SELECT status, COUNT(*) AS count FROM tickets GROUP BY status;

-- Inspection of transaction result: tickets and their history.
SELECT t.id, t.status, ev.action, ev.message
FROM tickets t JOIN ticket_events ev ON ev.ticket_id=t.id
ORDER BY t.id, ev.id;
