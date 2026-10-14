import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()