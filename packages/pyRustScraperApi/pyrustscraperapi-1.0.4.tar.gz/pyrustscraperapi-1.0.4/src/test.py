import pytest
import asyncio
from typing import AsyncGenerator
from pyRustScraperApi import Client, AsyncClient
from pyRustScraperApi.models import Order, Task, TokenInfo, ApiState, ApiError

# Константы для тестов
BASE_DOMAIN = "http://127.0.0.1:5050"
TOKEN = "TOKEN"
ORDER_HASH = "7ba68e6ab4acac02e1e1c78bc47c6d8022548eb2"
TEST_PRODUCTS = ["wb/300365052"]

# Фикстуры для синхронного клиента
@pytest.fixture
def sync_client() -> Client:
    """
    Фикстура для создания синхронного клиента
    """
    return Client(BASE_DOMAIN, TOKEN)

@pytest.fixture
def test_order() -> Order:
    """
    Фикстура для создания тестового заказа
    """
    return Order(TEST_PRODUCTS, [], [])

# Фикстуры для асинхронного клиента
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура для создания асинхронного клиента с поддержкой контекстного менеджера
    """
    async with AsyncClient(BASE_DOMAIN, TOKEN) as client:
        yield client

# Тесты для синхронного клиента
def test_sync_send_order(sync_client: Client, test_order: Order):
    """
    Тест отправки заказа через синхронный клиент
    """
    result = sync_client.send_order(test_order)
    assert isinstance(result, str)
    assert len(result) > 0

def test_sync_valid_order(sync_client: Client, test_order: Order):
    """
    Тест валидации заказа через синхронный клиент
    """
    result = sync_client.valid_order(test_order)
    assert isinstance(result, Order)
    assert len(result.products) > 0

def test_sync_stream_task(sync_client: Client):
    """
    Тест стриминга задачи через синхронный клиент
    """
    tasks = list(sync_client.stream_task(ORDER_HASH))
    assert len(tasks) > 0
    assert all(isinstance(task, (Task, ApiError)) for task in tasks)

def test_sync_get_task(sync_client: Client):
    """
    Тест получения задачи через синхронный клиент
    """
    task = sync_client.get_task(ORDER_HASH)
    assert isinstance(task, Task)
    assert task.order_hash == ORDER_HASH

def test_sync_get_token_info(sync_client: Client):
    """
    Тест получения информации о токене через синхронный клиент
    """
    token_info = sync_client.get_token_info()
    assert isinstance(token_info, TokenInfo)
    assert token_info.token == TOKEN

def test_sync_get_test_token(sync_client: Client):
    """
    Тест получения тестового токена через синхронный клиент
    """
    test_token = sync_client.get_test_token()
    assert isinstance(test_token, TokenInfo)
    assert test_token.token.startswith("rs.")

def test_sync_get_api_state(sync_client: Client):
    """
    Тест получения состояния API через синхронный клиент
    """
    state = sync_client.get_api_state()
    assert isinstance(state, ApiState)
    assert hasattr(state, 'version')

# Тесты для асинхронного клиента
@pytest.mark.asyncio
async def test_async_send_order(async_client: AsyncClient, test_order: Order):
    """
    Тест отправки заказа через асинхронный клиент
    """
    result = await async_client.send_order(test_order)
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_async_valid_order(async_client: AsyncClient, test_order: Order):
    """
    Тест валидации заказа через асинхронный клиент
    """
    result = await async_client.valid_order(test_order)
    assert isinstance(result, Order)
    assert len(result.products) > 0

@pytest.mark.asyncio
async def test_async_stream_task(async_client: AsyncClient):
    """
    Тест стриминга задачи через асинхронный клиент
    """
    tasks = []
    async for task in async_client.stream_task(ORDER_HASH):
        tasks.append(task)
    assert len(tasks) > 0
    assert all(isinstance(task, (Task, ApiError)) for task in tasks)

@pytest.mark.asyncio
async def test_async_get_task(async_client: AsyncClient):
    """
    Тест получения задачи через асинхронный клиент
    """
    task = await async_client.get_task(ORDER_HASH)
    assert isinstance(task, Task)
    assert task.order_hash == ORDER_HASH

@pytest.mark.asyncio
async def test_async_get_token_info(async_client: AsyncClient):
    """
    Тест получения информации о токене через асинхронный клиент
    """
    token_info = await async_client.get_token_info()
    assert isinstance(token_info, TokenInfo)
    assert token_info.token == TOKEN

@pytest.mark.asyncio
async def test_async_get_test_token(async_client: AsyncClient):
    """
    Тест получения тестового токена через асинхронный клиент
    """
    test_token = await async_client.get_test_token()
    assert isinstance(test_token, TokenInfo)
    assert test_token.token.startswith("rs.")

@pytest.mark.asyncio
async def test_async_get_api_state(async_client: AsyncClient):
    """
    Тест получения состояния API через асинхронный клиент
    """
    state = await async_client.get_api_state()
    assert isinstance(state, ApiState)
    assert hasattr(state, 'version')

# Простой вариант запуска тестов
if __name__ == "__main__":
    # Для синхронного клиента
    client = Client(BASE_DOMAIN, TOKEN)

    def run_sync_tests():
        """Запуск тестов синхронного клиента"""
        print("\nТестирование синхронного клиента:")

        print("\nТест send_order:")
        order_hash = client.send_order(Order(TEST_PRODUCTS, [], []))
        print(f"Получен hash: {order_hash}")

        print("\nТест stream_task:")
        for task in client.stream_task(order_hash):
            print(f"Получена задача: {task}")

        print("\nТест get_task:")
        task = client.get_task(order_hash)
        print(f"Получена задача: {task}")

        print("\nТест get_token_info:")
        token_info = client.get_token_info()
        print(f"Информация о токене: {token_info}")

        print("\nТест get_api_state:")
        state = client.get_api_state()
        print(f"Состояние API: {state}")

    async def run_async_tests():
        """Запуск тестов асинхронного клиента"""
        print("\nТестирование асинхронного клиента:")

        async with AsyncClient(BASE_DOMAIN, TOKEN) as async_client:
            print("\nТест send_order:")
            order_hash = await async_client.send_order(Order(TEST_PRODUCTS, [], []))
            print(f"Получен hash: {order_hash}")

            print("\nТест stream_task:")
            async for task in async_client.stream_task(order_hash):
                print(f"Получена задача: {task}")

            print("\nТест get_task:")
            task = await async_client.get_task(order_hash)
            print(f"Получена задача: {task}")

            print("\nТест get_token_info:")
            token_info = await async_client.get_token_info()
            print(f"Информация о токене: {token_info}")

            print("\nТест get_api_state:")
            state = await async_client.get_api_state()
            print(f"Состояние API: {state}")

    # Запуск тестов
    run_sync_tests()
    asyncio.run(run_async_tests())
