from ciphertopology.stats import monobit_frequency_test


def test_monobit_frequency_test_runs():
    data = b"\x00\xff" * 64
    result = monobit_frequency_test(data)
    assert "p_value" in result
    assert result["n_bits"] == len(data) * 8
