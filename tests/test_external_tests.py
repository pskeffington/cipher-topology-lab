from ciphertopology.external_tests import parse_dieharder_text


def test_parse_dieharder_text_extracts_result_row():
    text = "test_name | ntup | tsamples | psamples | p-value | assessment\n"
    text += "diehard_birthdays | 0 | 100 | 100 | 0.5321 | PASSED\n"
    rows = parse_dieharder_text(text, source_file="sample.txt")
    assert len(rows) == 1
    assert rows[0]["suite"] == "dieharder"
    assert rows[0]["test_name"] == "diehard_birthdays"
    assert rows[0]["p_value"] == 0.5321
    assert rows[0]["assessment"] == "PASSED"
