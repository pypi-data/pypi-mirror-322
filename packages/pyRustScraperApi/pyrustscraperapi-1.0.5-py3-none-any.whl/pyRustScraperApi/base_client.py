from abc import ABC, abstractmethod
from typing import Optional, Union, TypeVar
from .models import Order, Task, TokenInfo, ApiState, ApiError
import json

T = TypeVar('T')

class BaseClient(ABC):
    """
    Базовый абстрактный класс для API клиента.
    Определяет общий интерфейс и константы для обоих типов клиентов.
    """
    API_PATH = "/api"
    DEFAULT_BASE_DOMAIN = "https://rustscraper.ru"

    def __init__(self, token: Optional[str] = None, base_domain: Optional[str] = None):
        """
        Инициализация базового клиента
        :param base_domain: Базовый домен API (опционально)
        :param token: Токен авторизации (опционально)
        """
        self.base_domain = base_domain or self.DEFAULT_BASE_DOMAIN
        self.headers = {"Authorization": f"Bearer {token}"} if token else ""

    def _build_url(self, endpoint: str) -> str:
        """
        Построение полного URL для запроса
        :param endpoint: Конечная точка API
        :return: Полный URL
        """
        return f"{self.base_domain}{self.API_PATH}/{endpoint}"

    def _handle_error_response(self, status_code: int, text: str) -> ApiError:
        """
        Обработка ошибочного ответа от API
        :param status_code: HTTP статус код
        :param text: Текст ответа
        :return: Объект ошибки
        """
        try:
            error_data = json.loads(text)
            return ApiError(**error_data)
        except Exception:
            return ApiError("Any", text, status_code)

    @abstractmethod
    def send_order(self, order: Order) -> Union[str, ApiError]:
        """Отправка заказа"""
        pass

    @abstractmethod
    def valid_order(self, order: Order) -> Union[Order, ApiError]:
        """Валидация заказа"""
        pass

    @abstractmethod
    def get_task(self, order_hash: str) -> Union[Task, ApiError]:
        """Получение информации о задаче"""
        pass

    @abstractmethod
    def get_token_info(self) -> Union[TokenInfo, ApiError]:
        """Получение информации о токене"""
        pass

    @abstractmethod
    def get_test_token(self) -> Union[TokenInfo, ApiError]:
        """Получение тестового токена"""
        pass

    @abstractmethod
    def get_api_state(self) -> Union[ApiState, ApiError]:
        """Получение состояния API"""
        pass
