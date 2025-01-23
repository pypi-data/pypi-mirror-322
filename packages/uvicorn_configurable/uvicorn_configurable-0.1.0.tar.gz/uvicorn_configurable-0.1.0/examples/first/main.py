"""Main function"""

import uvicorn
from config import ExampleConfig
from loguru import logger


async def app(scope, receive, send):  # type: ignore  # pylint: disable=unused-argument
    """Dummy app"""

    assert scope["type"] == "http"

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": b"Hello, world!",
        }
    )


def main() -> int:
    """Run a simple uvicorn process that is configured with uvicorn_configurable"""
    cfg = ExampleConfig.get().uvicorn_config.as_uvicorn_config_dict()
    logger.debug(f"{cfg = }")
    uvicorn.run(**cfg)
    return 0


if __name__ == "__main__":
    main()
