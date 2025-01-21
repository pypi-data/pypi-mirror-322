from typing import Optional, Union, Iterator, AsyncIterator
from websockets.sync.client import connect as ws_connect_sync
from websockets.client import connect as ws_connect_async
from .base_client import BaseClient
from .models import Order, Task, TokenInfo, ApiState, ApiError
import httpx
import json

class Client(BaseClient):
    """
    Синхронный клиент для работы с API
    """

    def send_order(self, order: Order | dict) -> str:
        """
        Отправка заказа
        :param order: Объект заказа
        :return: Хэш заказа или ошибка

        :raises ApiError
        """
        if isinstance(order, dict):
            order = Order.from_json(order)
        res = httpx.post(
            self._build_url("order"),
            json=order.as_json(),
            headers=self.headers
        )
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return res.text

    def valid_order(self, order: Order | dict) -> Order:
        """
        Валидация заказа
        :param order: Объект заказа для проверки
        :return: Проверенный заказ или ошибка

        :raises ApiError
        """
        if isinstance(order, dict):
            order = Order.from_json(order)
        res = httpx.post(
            self._build_url("valid-order"),
            json=order.as_json(),
            headers=self.headers
        )
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return Order.from_json(res.json())

    def stream_task(self, order_hash: str) -> Iterator[Task]:
        """
        Стриминг статуса задачи через WebSocket
        :param order_hash: Хэш заказа
        :yield: Объект задачи или ошибка

        :raises ApiError
        """
        uri = f"ws://{self.base_domain.split('://')[1]}{self.API_PATH}/task-ws/{order_hash}"
        with ws_connect_sync(uri, additional_headers=self.headers) as ws:
            while (task := ws.recv()):
                task_json = json.loads(task)
                if "status" in task_json:
                    task = Task.from_json(task_json)
                    yield task
                    if task.is_done_by_status():
                        return
                elif "error" in task_json:
                    raise ApiError(**task_json)

    def get_task(self, order_hash: str) -> Task:
        """
        Получение информации о задаче
        :param order_hash: Хэш заказа
        :return: Объект задачи или ошибка

        :raises ApiError
        """
        res = httpx.get(
            self._build_url(f"task/{order_hash}"),
            headers=self.headers
        )
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return Task.from_json(res.json())

    def get_token_info(self) -> TokenInfo:
        """
        Получение информации о текущем токене
        :return: Информация о токене или ошибка

        :raises ApiError
        """
        res = httpx.get(
            self._build_url("token-info"),
            headers=self.headers
        )
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return TokenInfo.from_json(res.json())

    def get_test_token(self) -> TokenInfo:
        """
        Получение тестового токена
        :return: Информация о тестовом токене или ошибка

        :raises ApiError
        """
        res = httpx.get(self._build_url("test-token"))
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return TokenInfo.from_json(res.json())

    def get_api_state(self) -> ApiState:
        """
        Получение состояния API
        :return: Состояние API или ошибка

        :raises ApiError
        """
        res = httpx.get(self._build_url("state"))
        if res.status_code != 200:
            raise self._handle_error_response(res.status_code, res.text)
        return ApiState.from_json(res.json())


class AsyncClient(BaseClient):
    """
    Асинхронный клиент для работы с API
    """

    def __init__(self, base_domain: Optional[str] = None, token: Optional[str] = None):
        """
        Инициализация асинхронного клиента
        :param base_domain: Базовый домен API (опционально)
        :param token: Токен авторизации (опционально)
        """
        super().__init__(base_domain, token)
        self._http_client = None

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Получение HTTP клиента. Создает новый, если не существует
        :return: AsyncClient
        """
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    async def __aenter__(self):
        """Поддержка асинхронного контекстного менеджера"""
        self._http_client = await self._get_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие клиента при выходе из контекстного менеджера"""
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Union[dict, str]:
        """
        Вспомогательный метод для выполнения HTTP-запросов
        :param method: HTTP метод
        :param endpoint: Конечная точка API
        :return: Ответ от API

        :raises ApiError
        """
        kwargs["headers"] = kwargs.get("headers", self.headers)
        client = await self._get_client()
        response = await client.request(method, self._build_url(endpoint), **kwargs)

        if response.status_code != 200:
            raise self._handle_error_response(response.status_code, response.text)

        return response.json()

    async def send_order(self, order: Order | dict) -> str:
        """
        Отправка заказа
        :param order: Объект заказа
        :return: Хэш заказа или ошибка

        :raises ApiError
        """
        if isinstance(order, dict):
            order = Order.from_json(order)
        return await self._make_request(
            "POST",
            "order",
            json=order.as_json()
        )

    async def valid_order(self, order: Order | dict) -> Order:
        """
        Валидация заказа
        :param order: Объект заказа для проверки
        :return: Проверенный заказ или ошибка

        :raises ApiError
        """
        if isinstance(order, dict):
            order = Order.from_json(order)
        result = await self._make_request(
            "POST",
            "valid-order",
            json=order.as_json()
        )
        return Order.from_json(result)

    async def stream_task(self, order_hash: str) -> AsyncIterator[Task]:
        """
        Стриминг статуса задачи через WebSocket
        :param order_hash: Хэш заказа
        :yield: Объект задачи или ошибка

        :raises ApiError
        """
        uri = f"ws://{self.base_domain.split('://')[1]}{self.API_PATH}/task-ws/{order_hash}"

        async with ws_connect_async(uri, extra_headers=self.headers) as ws:
            while (task := await ws.recv()):
                task_json = json.loads(task)
                if "status" in task_json:
                    task = Task.from_json(task_json)
                    yield task
                    if task.is_done_by_status():
                        return
                elif "error" in task_json:
                    raise ApiError(**task_json)

    async def get_task(self, order_hash: str) -> Task:
        """
        Получение информации о задаче
        :param order_hash: Хэш заказа
        :return: Объект задачи или ошибка

        :raises ApiError
        """
        result = await self._make_request("GET", f"task/{order_hash}")
        return Task.from_json(result)

    async def get_token_info(self) -> TokenInfo:
        """
        Получение информации о текущем токене
        :return: Информация о токене или ошибка

        :raises ApiError
        """
        result = await self._make_request("GET", "token-info")
        return TokenInfo.from_json(result)

    async def get_test_token(self) -> TokenInfo:
        """
        Получение тестового токена
        :return: Информация о тестовом токене или ошибка

        :raises ApiError
        """
        result = await self._make_request("GET", "test-token")
        return TokenInfo.from_json(result)

    async def get_api_state(self) -> ApiState:
        """
        Получение состояния API
        :return: Состояние API или ошибка
        """
        result = await self._make_request("GET", "state")
        return ApiState.from_json(result)
