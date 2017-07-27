import pytest

from foxpuppet import FoxPuppet


@pytest.fixture
def browser(foxpuppet):
    """Initial Firefox browser window."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    return FoxPuppet(selenium)
