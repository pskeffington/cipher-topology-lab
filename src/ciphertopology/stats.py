from __future__ import annotations

import math

import numpy as np
from scipy import stats


def monobit_frequency_test(data: bytes) -> dict[str, float]:
    """Simple monobit frequency test.

    This is not a replacement for the full NIST SP 800-22 test suite.
    It is included as a lightweight internal diagnostic for early development.
    """
    arr = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    n = arr.size
    s_obs = abs(np.sum(2 * arr - 1)) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return {
        "n_bits": float(n),
        "ones": float(arr.sum()),
        "zeros": float(n - arr.sum()),
        "s_obs": float(s_obs),
        "p_value": float(p_value),
    }


def ks_compare_feature(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    res = stats.ks_2samp(x, y)
    return {"ks_statistic": float(res.statistic), "p_value": float(res.pvalue)}
