import asyncio

from src.settings.logging import setup_logging
from telegram.bot import bootstrap


async def main() -> None:
    setup_logging()
    await bootstrap()


if __name__ == "__main__":
    asyncio.run(main())
