from ciphertopology.generators import StreamSpec, generate_stream


def test_aes_ctr_stream_reproducible_for_same_spec() -> None:
    spec = StreamSpec("aes128_ctr_keystream_zero_plaintext", 0, 20260523, 128)
    stream_a, meta_a = generate_stream(spec)
    stream_b, meta_b = generate_stream(spec)

    assert stream_a == stream_b
    assert len(stream_a) == spec.n_bytes
    assert meta_a["algorithm"] == "AES-128"
    assert meta_a["mode"] == "CTR"
    assert "ctr_initial_value_hex" in meta_a
    assert "nonce_hex" not in meta_a
    assert meta_a == meta_b


def test_aes_ctr_stream_changes_by_replicate() -> None:
    spec_a = StreamSpec("aes128_ctr_keystream_zero_plaintext", 0, 20260523, 128)
    spec_b = StreamSpec("aes128_ctr_keystream_zero_plaintext", 1, 20260523, 128)

    stream_a, _ = generate_stream(spec_a)
    stream_b, _ = generate_stream(spec_b)

    assert stream_a != stream_b


def test_sha256_seeded_baseline_is_reproducible() -> None:
    spec = StreamSpec("sha256_seeded_baseline", 0, 20260523, 128)
    stream_a, meta_a = generate_stream(spec)
    stream_b, meta_b = generate_stream(spec)

    assert stream_a == stream_b
    assert len(stream_a) == spec.n_bytes
    assert meta_a == meta_b
    assert meta_a["algorithm"] == "SHA256-expansion"
    assert meta_a["mode"] == "deterministic-baseline"


def test_weak_controls_return_requested_length() -> None:
    for condition in ("lcg_weak", "xorshift32_weak"):
        spec = StreamSpec(condition, 0, 20260523, 130)
        stream, meta = generate_stream(spec)

        assert len(stream) == spec.n_bytes
        assert meta["mode"] == "weak-control"


def test_legacy_condition_names_remain_supported() -> None:
    for condition in ("aes128_ctr_random_plaintext", "aes128_ctr_zero_plaintext"):
        spec = StreamSpec(condition, 0, 20260523, 64)
        stream, meta = generate_stream(spec)

        assert len(stream) == spec.n_bytes
        assert meta["algorithm"] == "AES-128"
