import sys
import types

import pytest


@pytest.fixture(autouse=True)
def mock_qbruntime_module(monkeypatch):
    class MockAccelerator:
        def __init__(self, dev_no):
            if dev_no >= 4:
                raise RuntimeError("No such device")
            self._dev_no = dev_no

        def get_available_cores(self):
            return [0]

        def get_device_name(self):
            return "ARIES"

    mock_qbruntime = types.ModuleType("qbruntime")
    mock_qbruntime_accelerator = types.ModuleType("qbruntime.accelerator")
    mock_qbruntime_accelerator.Accelerator = MockAccelerator
    mock_qbruntime.accelerator = mock_qbruntime_accelerator

    monkeypatch.setitem(sys.modules, "qbruntime", mock_qbruntime)
    monkeypatch.setitem(sys.modules, "qbruntime.accelerator", mock_qbruntime_accelerator)
