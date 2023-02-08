import httpx


class BaseEntity:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get(self, *args, **kwargs):
        raise NotImplementedError()

    async def list(self, *args, **kwargs):
        raise NotImplementedError()

    async def create(self, *args, **kwargs):
        raise NotImplementedError()

    async def update(self, *args, **kwargs):
        raise NotImplementedError()

    async def delete(self, *args, **kwargs):
        raise NotImplementedError()
