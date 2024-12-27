import pytest

@pytest.fixture
def setup():
    print("Commun set up")
    yield
    print("Final teardown")


@pytest.fixture(scope="class")
def load_credential():
    return {"Username": "Manguito_Loco", "Password": "Wel092w", "Email": "juan_123@gmachines.com"}


@pytest.fixture(params=[("raul", "qw1", "ele@wet.com"), ("juan", "Passwoed123", "juancho@wet.com"), ("single_param")])
def multiple_credentials(request):
    return request.param