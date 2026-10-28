import logging

import allure

logger = logging.getLogger(__name__)


def report(response):
    request = response.request
    logger.info('%s %s -> %s (%d ms) request_id=%s',
                request.method, response.url, response.status_code,
                response.elapsed.total_seconds() * 1000,
                response.headers.get('X-Request-ID'))

    if '/auth/' in response.url:
        return
    if request.body:
        allure.attach(request.body, name='request', attachment_type=allure.attachment_type.JSON)
    allure.attach(response.text, name=f'response {response.status_code}',
                  attachment_type=allure.attachment_type.JSON)