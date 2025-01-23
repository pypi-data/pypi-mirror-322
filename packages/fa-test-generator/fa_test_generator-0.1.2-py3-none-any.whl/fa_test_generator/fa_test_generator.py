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
        tests_dir: str | None = None,
    ):
        if not isinstance(app, FastAPI):
            raise ValueError("app must be an instance of FastAPI")
        if not tests_dir:
            tests_dir = "./tests/"
        if tests_dir[-1] != "/":
            tests_dir += "/"
        self.app = app
        self.tests_dir = tests_dir

    def generate(self):
        os.makedirs(self.tests_dir, exist_ok=True)
        os.makedirs(self.tests_dir + "api/", exist_ok=True)

        routes_by_router: defaultdict[str, list[APIRoute]] = defaultdict(list)
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                router_name = self._get_router_name(route)
                routes_by_router[router_name].append(route)

        for router_name, routes in routes_by_router.items():
            test_class_name = (
                f"Test{''.join([word.capitalize() for word in router_name.split("_")])}"
            )
            test_file = os.path.join(self.tests_dir + "api/", f"test_{router_name}.py")

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
            conftest_code = f"""import os

from dotenv import load_dotenv
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

from main import app # change to your FastAPI app

load_dotenv(dotenv_path="{self.tests_dir}test.env")

@pytest.fixture(scope="session", autouse=True)
def check_mode():
    mode = os.getenv("MODE")
    if mode != "TEST":
        raise PermissionError(
            f"Envrironment variable MODE must be TEST for testing. Current MODE = {"{"}mode{"}"}"
        )

@pytest.fixture()
async def client():
    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
            yield ac"""
            conftest_file = os.path.join(self.tests_dir, "conftest.py")
            with open(conftest_file, "w", encoding="utf-8") as f:
                f.write(conftest_code)
            pytest_ini_code = f"""[pytest]
pythonpath = . .
env_files = {self.tests_dir}test.env
asyncio_mode=auto"""
            pytest_ini_file = os.path.join(self.tests_dir, "pytest.ini")
            with open(pytest_ini_file, "w", encoding="utf-8") as f:
                f.write(pytest_ini_code)

            env_test_code = "MODE=TEST"
            pytest_ini_file = os.path.join(self.tests_dir, "test.env")
            with open(pytest_ini_file, "w", encoding="utf-8") as f:
                f.write(env_test_code)

    @staticmethod
    def _generate_test_code(route: APIRoute) -> str:
        method = route.methods.pop()
        path = route.path
        test_method_name = f"test_{route.name}"

        if route.body_field:
            body_dct: dict[str, FieldInfo] = route.body_field.type_.model_fields
            body = {
                k: f" annotation: {v.annotation} {f", title: {v.title}" if v.title else ''}{f", default: {v.default}" if not isinstance(v.default, PydanticUndefinedType) else f", default_factory: {v.default_factory}" if v.default_factory else ''}"
                for k, v in body_dct.items()
            }
            req = f"""data = {"{"}
{str(json.dumps(body, indent=12,ensure_ascii=False))[1: -1].strip("\n")},
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
