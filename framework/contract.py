from functools import cache

import jsonschema
import requests

from framework.config.settings import settings


@cache
def openapi_spec():
    return requests.get(settings.base_url + '/openapi.json', timeout=settings.timeout).json()


def assert_matches_schema(data, schema_name):
    schema = {'$ref': f'#/components/schemas/{schema_name}', 'components': openapi_spec()['components']}
    jsonschema.validate(data, schema)