import pytest

from common.utils import get_current_timestamp


def test_it_should_generate_a_valid_slug():
    timestamp = get_current_timestamp()
    assert isinstance(timestamp, int)


if __name__ == "__main__":
    pytest.main()
