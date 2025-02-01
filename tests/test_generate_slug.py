import re

import pytest

from common.utils import generate_slug


def test_it_should_generate_a_valid_slug():
    cases = ["Minha Loja", "Meu e-commerce", "Casarão da Moda", "Tudo por 10",
             "loja com @arroba@"]

    for case in cases:
        response = generate_slug(case)
        assert response
        assert bool(re.fullmatch(r'^[a-z0-9\s-]+$', response))


if __name__ == "__main__":
    pytest.main()
