from hypercorn.config import Config
from hypercorn.asyncio import serve
from api.api import app
import settings

config = Config()
url = f"{settings.HOST}:{settings.PORT}"
config.bind = [url]
config.accesslog = "-"
config.errorlog = "-"

async def run_api():
    await serve(get_app(), config)
    
def get_app():
    return app
    
"""
from api.api import app
import settings


def get_app():
    return app

async def run_api():
    import uvicorn
    uvicorn_config = uvicorn.Config(app, host=settings.HOST, 
                                    port=int(settings.PORT), 
                                    ssl_certfile="/home/aalimadmin/certs/fullchain.pem", 
                                    ssl_keyfile="/home/aalimadmin/certs/privkey.pem")
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_api())
"""