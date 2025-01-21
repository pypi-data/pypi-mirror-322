# pyRustScraperApi

Клиентская библиотека для **RustScraperApi**

**RustScraperApi** — это высокопроизводительное API для сбора данных о товарах с популярных маркетплейсов, разработанное на языке программирования [Rust](https://ru.wikipedia.org/wiki/Rust_(%D1%8F%D0%B7%D1%8B%D0%BA_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)). Оно спроектировано для работы в условиях высокой нагрузки, обеспечивая надежность и максимальную скорость работы.

С помощью RustScraperApi вы можете разрабатывать автоматизированные системы для мониторинга и управления ценами на товары. Этот инструмент идеально подходит для сбора статистики, анализа и решения широкого спектра задач, соответствующих вашим бизнес-целям.

Проект разрабатывается и поддерживается одним человеком.
По любым вопросам:

- Telegram: [@Nikita5612](https://t.me/Nikita5612)

Полный доступ к сервису предоставляется на коммерческой основе. Подробности можно узнать в личных сообщениях.

Доступ для тестирования предоставляется бесплатно, однако он имеет ограничения по времени использования и лимитам в заказе.

### Установка

```bash
pip install pyRustScraperApi
```

### Получение тестового токена

Для начала работы получите тестовый токен через метод `/test-token`. Токен предоставляется для уникальных IP-адресов и действует ограниченное время.

```python
from pyRustScraperApi import Client

client = Client()
test_token = client.get_test_token()
print(test_token)
```

### Парсинг товаров

```python
from pyRustScraperApi import Client
from pyRustScraperApi.models import Order
import json


def main():
    client = Client(
        token="rs.ikx1u7xvQfBCgLt9RchNCaOB4d",
        # base_domain="https://rustscraper.ru"
    )

    # Товары на парсинг
    products = [
        "oz/1596079870",
        "ym/1732949807-100352880819-5997015",
        "wb/300365052",
        "mm/100028286032",
        "https://www.ozon.ru/product/nozhnitsy-kantselyarskie-21-sm-calligrata-nerzhaveyushchaya-stal-plastik-173091046/",
        "https://www.wildberries.ru/catalog/95979396/detail.aspx",
        "https://market.yandex.ru/product--igrovaia-pristavka-sony-playstation-5-slim-digital-edition-bez-diskovoda-1000-gb-ssd-2-geimpada-bez-igr-belyi/925519649?sku=103706885579&uniqueId=162025048",
        "https://megamarket.ru/catalog/details/nabor-instrumentov-v-keyse-108-predmetov-100065768905/"
	]

    # Создание заказа
    order = Order(
		products,
		cookies=[],
  		proxy_pool=[
            # "username:password@host:port"
            ]
	)

    # Отправка закза
    order_hash = client.send_order(order)

    # Отлеживание выполнение задачи через WebSocket
    for task in client.stream_task(order_hash):
        print(task)

    print(f"\n\n{task.extract_result_data()}")
    print(f"\n\n{json.dumps(task.result, ensure_ascii=False, indent=4)}")


if __name__ == "__main__":
    main()
```

### Асинхронный клиент

```python
from pyRustScraperApi import AsyncClient

async with AsyncClient(token="your_token") as client:
    order_hash = await client.send_order(order)
    async for update in client.stream_task(order_hash):
        print(update)
```
