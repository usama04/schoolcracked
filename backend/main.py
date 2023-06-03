import asyncio
from api import run_api
## New Stuff
import subprocess
import settings
import signal

async def main():
    # await run_api()
    ## New Stuff
    command = [
        "hypercorn",
        "api:app",
        "--bind", f"{settings.HOST}:{settings.PORT}",
        "--workers", "3"
    ]
    process = await asyncio.create_subprocess_exec(*command)
    
    # Register a signal handler to gracefully shutdown the server
    async def cleanup():
        process.send_signal(signal.SIGTERM)
        await process.wait()

    for signame in {'SIGINT', 'SIGTERM'}:
        asyncio.get_event_loop().add_signal_handler(getattr(signal, signame), lambda: asyncio.ensure_future(cleanup()))

    await process.wait()

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
    