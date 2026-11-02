"""Хуки behave — аналог фикстур pytest. Вызываются самим behave в нужный момент.

before_all      — один раз перед всем прогоном (настройки)
before_scenario — перед каждым сценарием (новый API-клиент)
after_scenario  — после каждого сценария, даже упавшего (уборка)
"""

from framework.api.app import Api
from framework.api.client import ApiClient
from framework.config.settings import get_settings
from framework.fixtures.api import cancel_open_orders


def before_all(context):
    context.settings = get_settings()


def before_scenario(context, scenario):
    # context — общий «рюкзак» сценария: шаги кладут в него данные и берут из него
    context.api = Api(ApiClient(context.settings.base_url, context.settings.timeout))
    context.response = None


def after_scenario(context, scenario):
    # Стакан общий: убираем открытые ордера сценария
    if context.api.client.token:
        cancel_open_orders(context.api)
    context.api.client.close()
