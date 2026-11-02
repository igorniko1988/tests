"""Хуки behave — замена conftest.py. behave вызывает их сам.

before_scenario — перед КАЖДЫМ сценарием: новый API-клиент в context.api
after_scenario  — после каждого сценария, даже упавшего: уборка и закрытие клиента
"""

from framework.api.app import Api
from framework.api.client import ApiClient
from framework.config.settings import get_settings
from framework.fixtures.api import cancel_open_orders


def before_scenario(context, scenario):
    settings = get_settings()
    context.api = Api(ApiClient(settings.base_url, settings.timeout))


def after_scenario(context, scenario):
    # Стакан общий: залогиненный пользователь мог оставить открытые ордера
    if context.api.client.token:
        cancel_open_orders(context.api)
    context.api.client.close()
