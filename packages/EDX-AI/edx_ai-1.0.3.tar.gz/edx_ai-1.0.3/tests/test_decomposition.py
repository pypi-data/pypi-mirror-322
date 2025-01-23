#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest
import numpy as np
from STEM_EDX import STEM_EDX_DATA

@pytest.fixture
def load_test_data():
    """Load the reference input data from a .pts file."""
    file_path = "tests/data/reference.pts"
    return STEM_EDX_DATA(file_path)

## Test PCA reference file is too big to be uploaded to GitLab (> 100 Mo).

# def test_pca(load_test_data):
#     """Test PCA decomposition by comparing results with the reference output."""
#     data = load_test_data
#     result = data.apply_PCA()

#     assert result == "Success", "PCA algorithm failed to execute."

#     # Load reference PCA result
#     expected_factors = np.load("tests/data/reference_PCA.npy")

#     # Compare the PCA factors (first component)
#     np.testing.assert_allclose(
#         data.PCA.factors.data[0], expected_factors[0], rtol=1e-3, atol=1e-5
#     )

def test_nmf(load_test_data):
    """Test NMF decomposition by comparing results with the reference output."""
    data = load_test_data
    result = data.apply_NMF()

    assert result == "Success", "NMF algorithm failed to execute."

    # Load reference NMF result
    expected_factors = np.load("tests/data/reference_NMF.npy")

    # Compare the NMF factors (first component)
    np.testing.assert_allclose(
        data.NMF.factors.data[0], expected_factors[0], rtol=1e-3, atol=1e-5
    )
