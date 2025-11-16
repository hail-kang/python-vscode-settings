"""Prisma client lifecycle manager."""

from prisma import Prisma


class PrismaManager:
    """Singleton manager for Prisma client."""

    _client: Prisma | None = None

    @classmethod
    async def init(cls) -> None:
        """Initialize Prisma client (called from lifespan)."""
        cls._client = Prisma()
        await cls._client.connect()

    @classmethod
    async def close(cls) -> None:
        """Close Prisma client (called from lifespan)."""
        if cls._client is not None:
            await cls._client.disconnect()
            cls._client = None

    @classmethod
    def get(cls) -> Prisma:
        """Get Prisma client instance as a dependency."""
        if cls._client is None:
            msg = "Prisma client not initialized. Call PrismaManager.init() first."
            raise RuntimeError(msg)
        return cls._client
