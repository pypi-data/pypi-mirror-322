import json
import os
from collections import defaultdict

from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefinedType


class FATestGenerator:
    def __init__(
        self,
        app: FastAPI,
        test_dir: str | None = None,
        base_url: str | None = None,
    ):
        if not isinstance(app, FastAPI):
            raise ValueError("app must be an instance of FastAPI")
        if not test_dir:
            test_dir = "./tests/"
        if test_dir[-1] != "/":
            test_dir += "/"
        self.app = app
        self.test_dir = test_dir
        self.base_url = base_url

    def generate(self):
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.test_dir + "api/", exist_ok=True)

        routes_by_router: defaultdict[str, list[APIRoute]] = defaultdict(list)
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                router_name = self._get_router_name(route)
                routes_by_router[router_name].append(route)

        for router_name, routes in routes_by_router.items():
            test_class_name = (
                f"Test{''.join([word.capitalize() for word in router_name.split("_")])}"
            )
            test_file = os.path.join(self.test_dir + "api/", f"test_{router_name}.py")

            test_methods = [self._generate_test_code(route) for route in routes]
            test_methods_str = "".join(test_methods)
            test_class_code = f"""from httpx import AsyncClient

class {test_class_name}:
    {test_methods_str}
            """
            if test_methods_str.find("jsony.") != -1:
                test_class_code = "import jsony\n" + test_class_code
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_class_code)
            conftest_code = f"""import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

from main import app # change to your FastAPI app


@pytest.fixture()
async def client():
    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        async with AsyncClient(transport=ASGITransport(app=app){", base_url=" + self.base_url if self.base_url else ""}) as ac:
            yield ac"""
            conftest_file = os.path.join(self.test_dir, "conftest.py")
            with open(conftest_file, "w", encoding="utf-8") as f:
                f.write(conftest_code)

    @staticmethod
    def _generate_test_code(route: APIRoute) -> str:
        method = route.methods.pop()  # HTTP-метод
        path = route.path
        test_method_name = f"test_{route.name}"

        if route.body_field:
            body_dct: dict[str, FieldInfo] = route.body_field.type_.model_fields
            body = {
                k: f"title: {v.title}, annotation: {v.annotation} {f", default: {v.default}" if not isinstance(v.default, PydanticUndefinedType) else f", default_factory: {v.default_factory}" if v.default_factory else ""}"
                for k, v in body_dct.items()
            }
            req = f"""data={"{"}
{str(json.dumps(body, indent=12,ensure_ascii=False))[1: -1].strip("\n")}
        {"}"}
        resp = await client.{method.lower()}("{path}", json=jsony.normalize(data))"""
        else:
            req = f'resp = await client.{method.lower()}("{path}")'

        test_code = f"""
    async def {test_method_name}(self, client: AsyncClient):
        {req}
        assert resp.status_code == {route.status_code if route.status_code else 200}
        # TODO: realize test for {method} {path}
        """
        return test_code

    @staticmethod
    def _get_router_name(route: APIRoute) -> str:
        module_name = route.endpoint.__module__
        router_name = module_name.split(".")[-1]
        return router_name
