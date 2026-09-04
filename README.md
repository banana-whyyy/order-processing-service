# Order Processing Service

Backend-сервис обработки заказов на Django и Django REST Framework.

Проект ориентирован не на реализацию обычного CRUD-магазина, а на бизнес-логику оформления заказов, резервирования складских остатков, обработки платежей и конкурентных запросов.

## Planned Features

- Каталог товаров
- Корзина пользователя
- Создание заказов
- Резервирование складских остатков
- Защита от overselling при конкурентных заказах
- Отмена резерва по timeout
- Обработка статусов заказа и платежей
- Идемпотентная обработка платежных операций
- Фоновые задачи через Celery
- REST API на Django REST Framework
- Транзакции и блокировки PostgreSQL

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Docker

## Core Business Flow

```text
Cart
  ↓
Create Order
  ↓
Reserve Stock
  ↓
PENDING_PAYMENT
  ↓
 ┌───────────────┐
 │               │
Payment       Timeout
 │               │
 ↓               ↓
PAID          CANCELLED
 │               │
Confirm       Release
Reservation   Reservation
```
При создании заказа остатки резервируются атомарно. Если заказ успешно оплачен, резерв подтверждается. Если время оплаты истекло, резерв освобождается, а товар возвращается в доступный остаток.

Project Status

🚧 In development