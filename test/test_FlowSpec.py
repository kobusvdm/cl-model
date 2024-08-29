
import os
# Add the src directory to the python path
# Jippo hack, Python testing still cannot locate its own SUT's
import sys

import pandas as pd
import pytest
from prefect.testing.utilities import prefect_test_harness


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "src"))
        import FlowSpec
        from ModelSpecs.MedmalCplParams import MedmalCplParams
        yield



def test_FlowSpec():
    res = FlowSpec.run(params=MedmalCplParams())
    assert isinstance(res, pd.DataFrame)