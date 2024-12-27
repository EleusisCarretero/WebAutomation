import pytest

pytest.mark.usefixtures("load_credential")
class TestLoadData:

    def test_load_data(self, load_credential):
        for key, value in load_credential.items():
            print(f"{key}: {value}")