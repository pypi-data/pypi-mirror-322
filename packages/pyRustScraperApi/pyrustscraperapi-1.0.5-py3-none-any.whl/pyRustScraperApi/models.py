"""
Модели данных pyRustScraperApi
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum
import json


@dataclass
class Order:
    """
    Класс, представляющий заказ на получение данных о товарах.

    Атрибуты:
        products (List[str]): Список идентификаторов товаров для сбора данных
        proxy_pool (List[str]): Список прокси-серверов для выполнения запросов
        cookies (List[dict]): Список куки для авторизации на сайте
    """

    products: List[str]
    proxy_pool: List[str]
    cookies: List[dict]

    def as_json(self) -> dict:
        """
        Преобразует объект заказа в JSON формат.

        Returns:
            dict: Словарь с данными заказа в формате JSON
        """
        json = self.__dict__
        json["proxyPool"] = json.pop("proxy_pool")
        return json

    @classmethod
    def from_json(cls, json: dict) -> 'Order':
        """
        Создает объект заказа из JSON данных.

        Args:
            json (dict): Словарь с данными заказа

        Returns:
            Order: Новый объект заказа
        """
        return cls(
            json["products"] if json.get("products") else [],
            json["proxyPool"] if json.get("proxyPool") else [],
            json["cookies"] if json.get("cookies") else []
        )


class TaskStatus(Enum):
    """
    Перечисление возможных статусов задачи.

    Значения:
        Waiting: Задача ожидает выполнения
        Processing: Задача выполняется
        Completed: Задача успешно завершена
        Interrupted: Выполнение задачи прервано
        Error: Произошла ошибка при выполнении задачи
    """
    Waiting = "waiting"
    Processing = "processing"
    Completed = "completed"
    Interrupted = "interrupted"
    Error = "error"


@dataclass
class ProductData:
    """
    Класс, представляющий данные о товаре.

    Атрибуты:
        sku (str): Уникальный идентификатор товара
        url (str): URL страницы товара
        name (Optional[str]): Название товара
        price (Optional[int]): Текущая цена товара
        cprice (Optional[int]): Цена товара со скидкой
        seller (Optional[str]): Имя продавца
        seller_id (Optional[str]): Идентификатор продавца
        img (Optional[str]): URL изображения товара
        reviews (Optional[int]): Количество отзывов
        rating (Optional[float]): Рейтинг товара
        brand (Optional[str]): Бренд товара
    """
    sku: str
    url: str
    name: Optional[str] = None
    price: Optional[int] = None
    cprice: Optional[int] = None
    seller: Optional[str] = None
    seller_id: Optional[str] = None
    img: Optional[str] = None
    reviews: Optional[int] = None
    rating: Optional[float] = None
    brand: Optional[str] = None


@dataclass
class Task:
    """
    Класс, представляющий задачу по сбору данных.

    Атрибуты:
        created_at (int): Timestamp создания задачи
        queue_num (int): Номер задачи в очереди
        status (TaskStatus): Текущий статус задачи
        progress (Optional[Tuple[int]]): Прогресс выполнения задачи
        result (Optional[dict]): Результаты выполнения задачи
    """
    created_at: int
    queue_num: int
    status: TaskStatus
    progress: Optional[Tuple[int]] = None
    result: Optional[dict] = None

    @classmethod
    def from_json(cls, json: dict) -> 'Task':
        """
        Создает объект задачи из JSON данных.

        Args:
            json (dict): Словарь с данными задачи

        Returns:
            Task: Новый объект задачи
        """
        return cls(
            json["createdAt"],
            json["queueNum"],
            TaskStatus(json["status"]),
            tuple(json["progress"]) if json.get("progress") else None,
            json["result"] if json.get("result") else None
        )

    def is_done_by_status(self) -> bool:
        """
        Проверяет, завершена ли задача (успешно или с ошибкой).

        Returns:
            bool: True если задача завершена, False в противном случае
        """
        return self.status in (
            TaskStatus.Completed,
            TaskStatus.Error,
            TaskStatus.Interrupted
        )

    def extract_result_data(self) -> Optional[Dict[str, Optional[ProductData]]]:
        """
        Извлекает данные о товарах из результата выполнения задачи.

        Returns:
            Optional[Dict[str, Optional[ProductData]]]: Словарь с данными о товарах,
            где ключ - идентификатор товара, значение - объект ProductData или None,
            если данные не удалось получить
        """
        if self.result and self.result.get('data'):
            result_data = self.result['data']
            for key in result_data.copy():
                product_data = result_data[key]
                if product_data:
                    result_data[key] = ProductData(
                        product_data['sku'],
                        product_data['url'],
                        product_data.get('name'),
                        product_data.get('price'),
                        product_data.get('cprice'),
                        product_data.get('seller'),
                        product_data.get('sellerId'),
                        product_data.get('img'),
                        product_data.get('reviews'),
                        product_data.get('rating'),
                        product_data.get('brand')
                    )
            return result_data
        return None


@dataclass
class TokenInfo:
    """
    Класс, представляющий информацию о токене доступа.

    Атрибуты:
        id (str): Идентификатор токена
        created_at (int): Timestamp создания токена
        ttl (int): Время жизни токена в секундах
        op_limit (int): Максимальное количество товаров в одном заказе
        tc_limit (int): Максимальное количество параллельных задач
    """
    id: str
    created_at: int
    ttl: int
    op_limit: int
    tc_limit: int

    @classmethod
    def from_json(cls, json: dict) -> 'TokenInfo':
        """
        Создает объект информации о токене из JSON данных.

        Args:
            json (dict): Словарь с данными о токене

        Returns:
            TokenInfo: Новый объект информации о токене
        """
        return cls(
            json["id"],
            json["createdAt"],
            json["ttl"],
            json["orderProductsLimit"],
            json["taskCountLimit"]
        )


@dataclass
class ApiState:
    """
    Класс, представляющий состояние API.

    Атрибуты:
        curr_open_ws (int): Текущее количество открытых WebSocket соединений
        curr_task_queue (int): Текущее количество задач в очереди
        handlers_count (int): Количество обработчиков задач
        open_ws_limit (int): Максимальное количество одновременных WebSocket соединений
        tasks_queue_limit (int): Максимальный размер очереди задач
    """
    curr_open_ws: int
    curr_task_queue: int
    handlers_count: int
    open_ws_limit: int
    tasks_queue_limit: int

    @classmethod
    def from_json(cls, json: dict) -> 'ApiState':
        """
        Создает объект состояния API из JSON данных.

        Args:
            json (dict): Словарь с данными о состоянии API

        Returns:
            ApiState: Новый объект состояния API
        """
        return cls(
            json["currOpenWs"],
            json["currTaskQueue"],
            json["handlersCount"],
            json["openWsLimit"],
            json["tasksQueueLimit"],
        )


class ApiError(Exception):
    """
    Класс, представляющий ошибку API.

    Атрибуты:
        error (str): Тип ошибки.
        code (int): Код ошибки.
        message (str): Описание ошибки.
    """
    def __init__(self, error: str, code: int, message: str):
        self.error = error
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {error}: {message}")

    def __str__(self):
        """
        Возвращает строковое представление ошибки.
        """
        return f"[{self.code}] {self.error}: {self.message}"

    def __repr__(self):
        """
        Возвращает техническое представление объекта ошибки.
        """
        return f"ApiError(error={self.error!r}, code={self.code}, message={self.message!r})"
