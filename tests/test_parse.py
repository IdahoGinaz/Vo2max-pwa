import pytest
from app import parse_vo2_from_fit_bytes

def test_parse_sample_fit_returns_none_or_number():
    # Place a sample .fit at tests/data/test_sample.fit to fully test parsing.
    # This test ensures the function runs without raising on a real file.
    import os
    p = os.path.join(os.path.dirname(__file__), "data", "test_sample.fit")
    if not os.path.exists(p):
        pytest.skip("No test_sample.fit provided")
    with open(p, "rb") as fh:
        data = fh.read()
    vo = parse_vo2_from_fit_bytes(data)
    assert vo is None or isinstance(vo, (int, float))
