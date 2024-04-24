# Веб-приложение для организации онлайн-заказов

В рамках работы над проектом я реаливал готовый шаблон для сервиса оформления онлайн заказов.
С помощью шаблона малый бизнес может самостоятельно запустить сервис онлайн заказов без наема специалистов. Достаточчно скачать репозиторий, настроить под себя содержимое веб-страниц и запустить сайт на сервере.

## Основной функционал
### Авторизация
- Регистрация
- Вход
- Просмотр профиля с информацией о пользователе и его заказах
- Выход

### Администрирование
- Создание, измененение категорий товаров
- Создание, измененение товаров
- Управление заказами

### Каталог
- Просмотр всех товаров с фильтрацией по категории
- Просмотр страницы товара с описанием
- Добавление товара в корзину
- Удаление товара из корзины

### Корзина
- Оформление заказа
- Изменение содержимого корзины

## Запуск проекта
- (желательно) Задать secret_key в main.py
- Запустить с помощью команды ```python main.py```

## Работа с add_admin.py
Необходимо запустить через командную строку

```python add_admin.py <user email> ```