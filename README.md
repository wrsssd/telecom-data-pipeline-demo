# telecom-data-pipeline-demo
Telecom data ETL pipeline &amp; analytics demo: web scraping, API data ingestion (Python, Pandas), and analytical SQL queries with window functions.
# Telecom Data Pipeline & Web Scraping

Небольшой репозиторий с примерами скриптов для сбора, предобработки и агрегации данных на Python и SQL.

## Стек
- Python 3.10+ (`pandas`, `requests`, `beautifulsoup4`, `sqlite3`)
- SQL (SQLite: `CTE`, `JOIN`, агрегатные и оконные функции)

## Описание скриптов

### 1. `telecom_pipeline.py`
Имитация мини-пайплайна обработки телеком-данных (тарифы и ежедневный трафик абонентов):
- Создает локальную БД `telecom_data.db` с таблицами `tariffs` и `traffic_logs`.
- Заполняет таблицы тестовыми данными по мобильному и фиксированному трафику.
- Выполняет аналитический запрос (через `WITH` и оконную функцию `RANK() OVER`) для расчета суммарного трафика в ГБ и ранжирования абонентов внутри каждого тарифа.
- Выгружает итоговый отчет в `telecom_analytical_report.csv`.

Пример результата выгрузки:

| user_id | tariff_name | monthly_fee | total_mobile_gb | total_fixed_gb | total_traffic_gb | rank_in_tariff |
|---|---|---|---|---|---|---|
| 104 | Базовый | 450.0 | 8.12 | 29.45 | 37.57 | 1 |
| 101 | Базовый | 450.0 | 5.40 | 21.10 | 26.50 | 2 |
| 108 | Смарт Плюс | 750.0 | 9.80 | 34.20 | 44.00 | 1 |
| 102 | Ультра Безлимит | 1200.0 | 11.25 | 41.15 | 52.40 | 1 |

### 2. `web_scraper.py`
Парсер книжного каталога (`books.toscrape.com`):
- Собирает данные по страницам каталога через `requests` и `BeautifulSoup`.
- Очищает значения цен от символов валют, приводит к числовому типу `float`.
- Сохраняет результат в `books_dataset.csv`.

## Запуск

Установка библиотек:
```bash
pip install -r requirements.txt
```

Запуск скриптов:
```bash
python telecom_pipeline.py
python web_scraper.py
```
