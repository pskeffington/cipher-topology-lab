from __future__ import annotations

import hashlib
import os
import random
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


@dataclass(frozen=True)
class StreamSpec:
    condition: str
    replicate: int
    master_seed: int
    n_bytes: int


def deterministic_bytes(label: str, n: int) -> bytes:
    """Generate deterministic bytes from repeated SHA-256 expansion.

    This is used for reproducible keys, initial counter blocks, structured inputs,
    and deterministic baseline streams. It is not used as a claim of cryptographic
    randomness.
    """
    out = bytearray()
    counter = 0
    while len(out) < n:
        block = hashlib.sha256(f"{label}:{counter}".encode("utf-8")).digest()
        out.extend(block)
        counter += 1
    return bytes(out[:n])


def aes128_ctr_stream(spec: StreamSpec, plaintext: bytes) -> tuple[bytes, dict[str, str]]:
    key = deterministic_bytes(f"aes-key:{spec.master_seed}:{spec.replicate}", 16)
    ctr_initial_value = deterministic_bytes(
        f"aes-ctr-initial-value:{spec.master_seed}:{spec.replicate}", 16
    )
    cipher = Cipher(algorithms.AES(key), modes.CTR(ctr_initial_value))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    meta = {
        "algorithm": "AES-128",
        "mode": "CTR",
        "key_hex": key.hex(),
        "ctr_initial_value_hex": ctr_initial_value.hex(),
    }
    return ciphertext, meta


def sha256_seeded_baseline_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    stream = deterministic_bytes(
        f"sha256-seeded-baseline:{spec.master_seed}:{spec.replicate}", spec.n_bytes
    )
    return stream, {"algorithm": "SHA256-expansion", "mode": "deterministic-baseline"}


def os_csprng_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    return os.urandom(spec.n_bytes), {"algorithm": "OS-CSPRNG", "mode": "raw-nondeterministic"}


def lcg_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    m = 2**32
    a = 1664525
    c = 1013904223
    x = (spec.master_seed + spec.replicate) % m
    out = bytearray()
    while len(out) < spec.n_bytes:
        x = (a * x + c) % m
        out.extend(x.to_bytes(4, "little"))
    return bytes(out[: spec.n_bytes]), {
        "algorithm": "LCG",
        "mode": "weak-control",
        "a": str(a),
        "c": str(c),
        "m": str(m),
    }


def xorshift32_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    x = (spec.master_seed ^ (spec.replicate + 0x9E3779B9)) & 0xFFFFFFFF
    if x == 0:
        x = 1
    out = bytearray()
    while len(out) < spec.n_bytes:
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        out.extend(x.to_bytes(4, "little"))
    return bytes(out[: spec.n_bytes]), {"algorithm": "xorshift32", "mode": "weak-control"}



def periodic_byte_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    pattern = deterministic_bytes(
        f"periodic-byte-pattern:{spec.master_seed}:{spec.replicate}",
        16,
    )
    repeats = (spec.n_bytes // len(pattern)) + 1
    stream = (pattern * repeats)[: spec.n_bytes]
    return stream, {
        "algorithm": "periodic-byte-pattern",
        "mode": "weak-control",
        "period_bytes": str(len(pattern)),
    }


def biased_byte_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    rng = random.Random(f"biased-byte-weak:{spec.master_seed}:{spec.replicate}")
    out = bytearray()
    while len(out) < spec.n_bytes:
        value = rng.randrange(0, 64)
        out.append(value)
    return bytes(out), {
        "algorithm": "biased-byte-generator",
        "mode": "weak-control",
        "bias": "values restricted to 0..63",
    }

def generate_stream(spec: StreamSpec) -> tuple[bytes, dict[str, str]]:
    if spec.condition in {
        "aes128_ctr_random_plaintext",
        "aes128_ctr_xor_deterministic_plaintext",
    }:
        rng = random.Random(f"{spec.master_seed}:{spec.replicate}:plaintext")
        plaintext = bytes(rng.randrange(0, 256) for _ in range(spec.n_bytes))
        stream, meta = aes128_ctr_stream(spec, plaintext)
        meta["plaintext_pattern"] = "deterministic_random"
        return stream, meta

    if spec.condition in {
        "aes128_ctr_zero_plaintext",
        "aes128_ctr_keystream_zero_plaintext",
    }:
        plaintext = bytes(spec.n_bytes)
        stream, meta = aes128_ctr_stream(spec, plaintext)
        meta["plaintext_pattern"] = "zero"
        return stream, meta

    if spec.condition == "sha256_seeded_baseline":
        stream, meta = sha256_seeded_baseline_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta

    if spec.condition == "os_csprng":
        stream, meta = os_csprng_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta

    if spec.condition == "lcg_weak":
        stream, meta = lcg_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta

    if spec.condition == "xorshift32_weak":
        stream, meta = xorshift32_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta


    if spec.condition == "periodic_byte_weak":
        stream, meta = periodic_byte_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta

    if spec.condition == "biased_byte_weak":
        stream, meta = biased_byte_stream(spec)
        meta["plaintext_pattern"] = "n/a"
        return stream, meta

    raise ValueError(f"Unknown condition: {spec.condition}")
