"""Fixtures for LODKit testing."""

from lodkit import plist, ttl
import pytest


@pytest.fixture(params=[ttl, plist], scope="module")
def constructor(request):
    """Parametrized fixture for testing ttl /and/ plist constructors.

    Note that hypothesis doesn't accept function scoped fixtures.
    """
    return request.param
