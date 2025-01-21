import math

import pytest
import pandas as pd
import numpy as np
import itertools
import dask.dataframe as dd

from tests.utils import get_daily_spy
from tests import test_data_path

test_k_pct = 0.01
test_f = 100.0


@pytest.fixture
def nonstationary_series():
    np.random.seed(42)
    data = np.cumsum(np.random.randn(1000))  # Random walk
    yield pd.Series(data)


@pytest.fixture
def daily_spy_data():
    return get_daily_spy(test_data_path / 'SPY.csv')


@pytest.fixture
def simple_encode_test_df_pandas():
    yield pd.DataFrame.from_dict(generate_simple_encode_dict())


@pytest.fixture
def simple_encode_test_df_dask():
    yield dd.from_pandas(pd.DataFrame.from_dict(generate_simple_encode_dict()), npartitions=2)


def generate_multi_encode_dict():
    f1 = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
          'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
          'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', ]
    f2 = ['Y', 'X', 'X', 'Y', 'X', 'Z', 'X', 'Y',
          'X', 'X', 'X', 'X', 'Y', 'Z', 'X', 'Z', 'X', 'Y', 'Z',
          'X', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'X', ]
    o = [1, 0, 1, 1, 1, 1, 0, 0,
         0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0,
         0, 1, 1, 1, 1, 1, 0, 0, ]

    p = sum(o)/len(o)
    combos = [e for e in itertools.product(list(set(f1)), list(set(f2)))]
    counts = {k: 0 for k in combos}
    sums = {k: 0 for k in combos}
    f1f2 = list(zip(f1, f2, o))
    for f in f1f2:
        k = tuple(f[:2])
        counts[k] += 1
        sums[k] += f[2]
    loo = []
    ema_loo = []
    for f in f1f2:
        k = tuple(f[:2])
        if counts[k] > 1:
            loo_val = (sums[k] - f[2]) / (counts[k] - 1)
            loo.append(loo_val)
            l = 1 / (1 + math.exp(-(counts[k] - test_k_pct * len(o)) / test_f))
            ema_loo.append(l * loo_val + (1 - l) * p)
        elif counts[k] == 1:
            loo.append(sums[k])
            ema_loo.append(sums[k])
        else:
            loo.append(0.5)
            ema_loo.append(0.5)
    return {
        'Feature1': f1,
        'Feature2': f2,
        'Outcome': o,
        'LOOEncode': loo,
        'EMA_LOOEncode': ema_loo,
    }


def generate_simple_encode_dict():
    f1 = ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', ]
    #'NumericFeature1': [0.22, 0.35, 0.12, 0.24, 0.45, 0.14, 0.74, 0.39, 0.14, ],
    o = [1, 0, 1, 1, 1, 1, 0, 1, 1, ]
    # [2. / 3., 1.00, 2. / 3., 2. / 3., 0.50, 0.50, 1.00, 1.00, 1.00, ]

    p = sum(o)/len(o)
    combos = set(f1)
    counts = {k: 0 for k in combos}
    sums = {k: 0 for k in combos}
    f1o = list(zip(f1, o))
    for f in f1o:
        k = f[0]
        counts[k] += 1
        sums[k] += f[1]
    loo = []
    ema_loo = []
    for f in f1o:
        k = f[0]
        if counts[k] > 1:
            loo_val = (sums[k] - f[1]) / (counts[k] - 1)
            loo.append(loo_val)
            l = 1 / (1 + math.exp(-(counts[k] - test_k_pct * len(o)) / test_f))
            ema_loo.append(l * loo_val + (1 - l) * p)
        elif counts[k] == 1:
            loo.append(sums[k])
            ema_loo.append(sums[k])
        else:
            loo.append(0.5)
            ema_loo.append(0.5)
    return {
        'Feature1': f1,
        'Outcome': o,
        'LOOEncode': loo,
        'EMA_LOOEncode': ema_loo,
    }


@pytest.fixture
def multi_encode_test_df_pandas():
    yield pd.DataFrame.from_dict(generate_multi_encode_dict())


@pytest.fixture
def multi_encode_test_df_dask():
    yield dd.from_pandas(pd.DataFrame.from_dict(generate_multi_encode_dict()), npartitions=2)

