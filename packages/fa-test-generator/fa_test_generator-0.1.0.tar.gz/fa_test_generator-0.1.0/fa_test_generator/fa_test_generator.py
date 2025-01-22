import json
import os
from collections import defaultdict

from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefinedType


class FATestGenerator:
    def __init__(self, app: FastAPI, test_dir: str = "./tests/api/"):
        self.app = app
        self.test_dir = test_dir

    def generate(self):
        os.makedirs(self.test_dir, exist_ok=True)

        routes_by_router: defaultdict[str, list[APIRoute]] = defaultdict(list)
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                router_name = self._get_router_name(route)
                routes_by_router[router_name].append(route)

        for router_name, routes in routes_by_router.items():
            test_class_name = f"Test{''.join([word.capitalize() for word in router_name.split("_")])}"
            test_file = os.path.join(self.test_dir, f"test_{router_name}.py")

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
