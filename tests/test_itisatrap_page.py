import os
import pytest
from pages.itisatrap import ItisaTrapPage


PREF_SET = os.environ['PREF_SET']


@pytest.mark.nondestructive
def test_third_party_tracker_loads_correctly(base_url, selenium):
    page = ItisaTrapPage(selenium, base_url).open()

    assert page.third_party_loads_correctly


@pytest.mark.nondestructive
def test_first_party_tracker_loads_correctly(base_url, selenium):
    page = ItisaTrapPage(selenium, base_url).open()

    assert page.first_party_loads_correctly


@pytest.mark.nondestructive
def test_DNT_signal_correctly_sent(base_url, selenium):
    page = ItisaTrapPage(selenium, base_url).open()

    assert page.dnt_signal_correctly_sent
