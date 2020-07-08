def pytest_addoption(parser):
    parser.addoption("--id", action="store", default="")
    parser.addoption("--key", action="store", default="")
    parser.addoption("--project", action="store", default="")
