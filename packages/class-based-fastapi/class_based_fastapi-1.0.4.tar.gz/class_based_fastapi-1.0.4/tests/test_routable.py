from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

from class_based_fastapi.decorators import get, post
from class_based_fastapi.routable import Routable
from tests.utilities import check_api_methods


class ExampleRoutableChildren1(Routable):
    _injected = 1

    @get(path='/add/{x:int}')
    def add(self, x: int) -> int:
        return x + self._injected

    @post(path='/sub/{x:int}')
    def sub(self, x: int) -> int:
        return x - self._injected

    @get(path='/async')
    async def do_async(self) -> int:
        return self._injected + 1

    @get(path='/aecho/{val}', response_class=PlainTextResponse)
    async def aecho(self, val: str) -> str:
        return f'{val} {self._injected}'

    @get(path='/{version}/base-method')
    async def overridable_method(self) -> int:
        return self._injected + 1

    @get(path='/{module}/1/get')
    async def template_1_method(self) -> int:
        return self._injected + 1


class ExampleRoutableParent1(ExampleRoutableChildren1):
    NAME_MODULE = 'Test'

    @get(path='/override-base-method')
    async def overridable_method(self) -> int:
        return self._injected + 2

    @get(path='get')
    async def template1_method(self) -> int:
        return self._injected + 2

    @get(path='/{controller}/get')
    async def template2_method(self) -> int:
        return self._injected + 2

    @get(path='/{module}/get')
    async def template3_method(self) -> int:
        return self._injected + 2

    @get(path='')
    async def template4_method(self) -> int:
        return self._injected + 2


def test_routes_respond() -> None:
    app = FastAPI()
    t = ExampleRoutableChildren1
    app.include_router(t.routes())

    check_api_methods(app)

    client = TestClient(app)

    response = client.get('/add/22')
    assert response.status_code == 200
    assert response.text == '23'

    response = client.post('/sub/4')
    assert response.status_code == 200
    assert response.text == '3'


def test_routes_only_respond_to_method() -> None:
    app = FastAPI()
    t = ExampleRoutableChildren1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.post('/add/22')
    assert response.status_code == 405
    response = client.put('/add/22')
    assert response.status_code == 405
    response = client.delete('/add/22')
    assert response.status_code == 405

    response = client.get('/sub/4')
    assert response.status_code == 405
    response = client.put('/sub/4')
    assert response.status_code == 405
    response = client.delete('/sub/4')
    assert response.status_code == 405


def test_async_methods_work() -> None:
    app = FastAPI()
    t = ExampleRoutableChildren1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/async')
    assert response.status_code == 200
    assert response.text == '2'

    # Make sure we can call it more than once.
    response = client.get('/async')
    assert response.status_code == 200
    assert response.text == '2'


def test_async_methods_with_args_work() -> None:
    app = FastAPI()
    t = ExampleRoutableChildren1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/aecho/hello')
    assert response.status_code == 200
    assert response.text == 'hello 1'


def test_routes_respond_parent() -> None:
    app = FastAPI()
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/add/22')
    assert response.status_code == 200
    assert response.text == '23'

    response = client.post('/sub/4')
    assert response.status_code == 200
    assert response.text == '3'


def test_routes_only_respond_to_method_parent() -> None:
    app = FastAPI()
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.post('/add/22')
    assert response.status_code == 405
    response = client.put('/add/22')
    assert response.status_code == 405
    response = client.delete('/add/22')
    assert response.status_code == 405

    response = client.get('/sub/4')
    assert response.status_code == 405
    response = client.put('/sub/4')
    assert response.status_code == 405
    response = client.delete('/sub/4')
    assert response.status_code == 405


def test_async_methods_work_parent() -> None:
    app = FastAPI()
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/async')
    assert response.status_code == 200
    assert response.text == '2'

    # Make sure we can call it more than once.
    response = client.get('/async')
    assert response.status_code == 200
    assert response.text == '2'


def test_async_methods_with_args_work_parent() -> None:
    app = FastAPI()
    n = 1
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/aecho/hello')
    assert response.status_code == 200
    assert response.text == 'hello {}'.format(n)


def test_override_method_work_parent() -> None:
    app = FastAPI()
    n = 1
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    client = TestClient(app)

    response = client.get('/base-method')
    assert response.status_code == 404
    response = client.get('/override-base-method')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 2)


def test_base_template() -> None:
    app = FastAPI()
    n = 1
    t = ExampleRoutableParent1
    app.include_router(t.routes())

    check_api_methods(app)

    client = TestClient(app)

    response = client.get('/get')
    assert response.status_code == 404

    response = client.get('/test/example-routable-parent1/v1.0/get')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 2)

    response = client.get('/example-routable-parent1/get')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 2)

    response = client.get('/test/get')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 2)

    response = client.get('/test/example-routable-parent1/v1.0')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 2)

    response = client.get('/test/1/get')
    assert response.status_code == 200
    assert response.text == '{}'.format(n + 1)
