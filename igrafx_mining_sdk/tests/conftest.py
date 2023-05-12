import pytest


def pytest_addoption(parser):
    parser.addoption("--id", action="store", default="ceb26b8b-d026-44ee-93a7-2e04ab03bea5")
    parser.addoption("--key", action="store", default="63c1d566-580a-45fc-a4ef-cc4f71e10111")
    parser.addoption("--project", action="store", default="8fe914fb-1f2f-4d0e-902e-6adfafb048bd")
    parser.addoption("--apiurl", action="store", default="https://api.igfx-eastus-qa.logpickr.com")
    parser.addoption("--authurl", action="store", default="https://auth-staging.igrafxcloud.com/realms/logpickr-api-qa")


"""All necessary fixtures, available to all pytest tests: """


@pytest.fixture()
def ID(pytestconfig):
    return pytestconfig.getoption("id")


@pytest.fixture()
def SECRET(pytestconfig):
    return pytestconfig.getoption("key")


@pytest.fixture()
def API(pytestconfig):
    return pytestconfig.getoption("apiurl")


@pytest.fixture()
def AUTH(pytestconfig):
    return pytestconfig.getoption("authurl")


@pytest.fixture()
def PROJECT_ID(pytestconfig):
    return pytestconfig.getoption("project")
