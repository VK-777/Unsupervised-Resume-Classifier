import asyncio
import sys
import uvicorn
from Controller.classifier_controller import shutdown_event


async def shutdown_server(server):
    # Wait for the shutdown event
    await shutdown_event.wait()
    # Shutdown the server gracefully
    await server.shutdown()
    # Force exit
    sys.exit(0)  # Exit with code 0 indicating success


async def main():
    config = uvicorn.Config("main:app", host="192.168.1.15", port=8000, log_level="info")
    server = uvicorn.Server(config)

    # Start server and background tasks
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown_server(server))

    # Start the server and wait for it to stop
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
