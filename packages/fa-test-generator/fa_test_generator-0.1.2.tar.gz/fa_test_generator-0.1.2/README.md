# FATestGenerator

**FATestGenerator** — это утилита для автоматической генерации тестов для API, созданных с использованием FastAPI. Библиотека позволяет быстро создавать тесты для ваших маршрутов и удобно организует их структуру.

## Особенности

- Генерация тестов для всех маршрутов FastAPI.
- Поддержка асинхронного клиента `httpx`.
- Автоматическая организация тестов по роутерам.
- Генерация вспомогательных файлов:
  - `conftest.py` для фикстур и настройки окружения.
  - `pytest.ini` для конфигурации pytest.
  - `.env` файл для тестового окружения.

---

## Установка

Добавьте `FATestGenerator` в ваш проект:

```bash
pip install fa-test-generator
```

```bash
poetry add fa-test-generator
```

---

## Использование

### Инициализация

```python
from fastapi import FastAPI
from fa_test_generator import FATestGenerator

app = FastAPI()
# Инициализация вашего приложения FastAPI

generator = FATestGenerator(app, tests_dir="./tests/")
generator.generate()
```

### Параметры конструктора

- `app` (FastAPI): Ваше приложение FastAPI.
- `tests_dir` (str, optional): Папка для хранения тестов. По умолчанию — `./tests/`.

---

## Что генерируется?

1. **`Файлы тестов`**:
   Для каждого файла с маршрутами создается отдельный файл в `tests/api/`.

   Например, для роутера `user_router` лежащий в файле user_router.py:

   ```python
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


    app = FastAPI()

    app.include_router(user_router)

    if __name__ == "__main__":
        FATestGenerator(app, tests_dir="./tests/").generate()
   ```

   создается файл `tests/api/test_user_router.py` со структурой:

   ```python
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

2. **`conftest.py`**:
   Этот файл настраивает фикстуры и проверяет тестовое окружение.

   ```python
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

3. **`pytest.ini`**:
   Файл конфигурации для pytest:

   ```ini
   [pytest]
   pythonpath = . .
   env_files = ./tests/test.env
   asyncio_mode = auto
   ```

4. **`test.env`**:
   Файл окружения для тестов:

   ```env
   MODE=TEST
   ```

---

## Как работает генерация тестов?

- Классы тестов организуются по роутерам. Названия классов формируются автоматически на основе имени модуля.
- Для каждого маршрута создается метод теста с заготовкой для проверки статуса ответа.
- Если маршрут требует тело запроса, оно будет автоматически сгенерировано на основе модели FastAPI.

Пример сгенерированного метода теста:

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

## Лицензия

Этот проект распространяется под лицензией MIT. Для получения подробной информации смотрите файл LICENSE.
