import typing as t

import httpx


class HuntflowAPI:
    def __init__(
        self,
        base_url: str,
        token: str,
        request_event_hooks: t.List[t.Callable] = None,
        response_event_hooks: t.List[t.Callable] = None,
    ):
        self.base_url = base_url
        self.token = token
        self.http_client = self.init_http_client(request_event_hooks, response_event_hooks)

    def init_http_client(
        self,
        request_event_hooks: t.List[t.Callable] = None,
        response_event_hooks: t.List[t.Callable] = None,
    ) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["request"] = request_event_hooks or []
        http_client.event_hooks["response"] = response_event_hooks or []
        return http_client
