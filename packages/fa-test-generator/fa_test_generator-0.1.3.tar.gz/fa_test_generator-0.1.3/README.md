# FATestGenerator

**FATestGenerator** is a utility for automatically generating tests for APIs built with FastAPI. The library allows you to quickly create tests for your routes and neatly organize their structure.

## Особенности

- Test generation for all FastAPI routes.
- Support for the asynchronous client httpx.
- Automatic test organization by routers.
- Generation of auxiliary files:
  - `conftest.py` for fixtures and environment setup.
  - `pytest.ini` for pytest configuration.
  - `test.env` file for the test environment.

---

## Installation

Add `FATestGenerator` to your project:

```bash
pip install fa-test-generator
```

```bash
poetry add fa-test-generator
```

---

## Usage

### Initialization

```python
from fastapi import FastAPI
from fa_test_generator import FATestGenerator

# Initialize your FastAPI app
app = FastAPI()

# Initialize the generator and start generating tests
generator = FATestGenerator(app, tests_dir="./tests/")
generator.generate()
```

### Constructor Parameters

- `app` (FastAPI): Your FastAPI app.
- `tests_dir` (str, optional): The folder to store the tests. Default is `./tests/`.

---

## What is Generated?

1. **`Test Files`**:
   For each router file, a separate test file is created in `tests/api/`.

   For example, for the router located in `user_router.py`:

   ```python
    # app/api/routers/user_router.py

    from fa_test_generator import FATestGenerator
    from fastapi import APIRouter, FastAPI, status
    from pydantic import BaseModel

    from models.user import User
    from services.user_service import UserService

    user_router = APIRouter()


    @user_router.get(
        path="/users/",
        status_code=status.HTTP_200_OK,
        response_model=list[User],
    )
    async def get_users():
        users = UserService.get_users()
        return users


    class UserCreateScheme(BaseModel):
        name: str = Field(
            title="Username",
            default="Unknown"
        )


    @user_router.post(
        path="/users/",
        status_code=status.HTTP_201_CREATED,
        response_model=User,
    )
    async def create_user(
        user_scheme: UserCreateScheme,
    ):
        user = UserService.create_user(user_scheme)
        return user

    # app/main.py

    from fastapi import FastAPI

    app = FastAPI()

    app.include_router(user_router)

    if __name__ == "__main__":
        FATestGenerator(app, tests_dir="./tests/").generate()
   ```

   A file `tests/api/test_user_router.py` is created with the following structure:

   ```python
   # tests/api/test_user_router.py

   from httpx import AsyncClient
   import jsony

   class TestUsers:
       async def test_get_users(self, client: AsyncClient):
           resp = await client.get("/users")
           assert resp.status_code == 200

        async def test_create_user(self, client: AsyncClient):
            data = {
                "name": "annotation: str, title: Username, default: Unknown"
            }
           resp = await client.post("/users", json=jsony.normalize(data))
           assert resp.status_code == 2001
   ```

2. **`conftest.py`**: This file sets up fixtures and checks the test environment.

   ```python
   # app/tests/conftest.py

   import os
   from dotenv import load_dotenv
   import pytest
   from asgi_lifespan import LifespanManager
   from httpx import AsyncClient, ASGITransport
   from main import app

   load_dotenv(dotenv_path="./tests/test.env")

   @pytest.fixture(scope="session", autouse=True)
   def check_mode():
       mode = os.getenv("MODE")
       if mode != "TEST":
           raise PermissionError(f"Environment variable MODE must be TEST. Current MODE = {mode}")

   @pytest.fixture()
   async def client():
       async with LifespanManager(app):
           async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as ac:
               yield ac
   ```

3. **`pytest.ini`**: Configuration file for pytest:

   ```ini
    # app/test/pytest.ini

   [pytest]
   pythonpath = . .
   env_files = ./tests/test.env
   asyncio_mode = auto
   ```

4. **`test.env`**: Environment file for tests:

   ```env
   # app/test/test.env

   MODE=TEST
   ```

---

## How Does Test Generation Work?

- Test classes are organized by routers. The class names are generated automatically based on the module name.
- A test method is created for each route with a template to check the response status.
- If the route requires a request body, it will be automatically generated based on the FastAPI model.

Example of a generated test method:

```python
async def test_create_user(self, client: AsyncClient):
    data = {
        "name": "John Doe",
        "age": 30
    }
    resp = await client.post("/users", json=data)
    assert resp.status_code == 201
```

---

## License

This project is licensed under the MIT License. For more information, see the LICENSE file.
