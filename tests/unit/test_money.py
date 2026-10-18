from decimal import Decimal

import pytest

from ui_framework.utils.money import format_amount


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('100.50', '100.5'),
        ('1000.000', '1000'),
        ('0', '0'),
        ('0.00000001', '0.00000001'),
        (Decimal('1000') - Decimal('100.50'), '899.5'),
    ],
)
def test_format_amount(value, expected):
    assert format_amount(value) == expected


def test_decimal_from_float_is_not_exact():
    assert Decimal(0.1) != Decimal('0.1')
