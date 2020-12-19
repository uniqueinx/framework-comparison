import typing
import aioredis
import fastapi
import fastapi_plugins
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from datetime import datetime
import orjson


class User(BaseModel):
    id: str


class AppSettings(fastapi_plugins.RedisSettings):
    api_name: str = str(__name__)


app = fastapi.FastAPI(default_response_class=ORJSONResponse)
config = AppSettings()


@app.post("/status")
async def set_status(
    user: User,
    cache: aioredis.Redis = fastapi.Depends(fastapi_plugins.depends_redis),
) -> typing.Dict:
    try:
        data = {"status": "live", "last_time": datetime.utcnow()}
        await cache.setex(user.id, 50, orjson.dumps(data))
        return {"status": True}
    except:
        from traceback import print_exc
        print_exc()


@app.get("/status/{user}")
async def get_status(
    user: str,
    cache: aioredis.Redis = fastapi.Depends(fastapi_plugins.depends_redis),
) -> typing.Dict:
    try:
        data = await cache.get(user)
        return orjson.loads(data) if data else {}
    except:
        from traceback import print_exc
        print_exc()


@app.on_event("startup")
async def on_startup() -> None:
    await fastapi_plugins.redis_plugin.init_app(app, config=config)
    await fastapi_plugins.redis_plugin.init()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await fastapi_plugins.redis_plugin.terminate()