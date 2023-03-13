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
        self._request_event_hooks = request_event_hooks or []
        self._response_event_hooks = response_event_hooks or []

    @property
    def client(self) -> httpx.AsyncClient:
        headers = {"Authorization": f"Bearer {self.token}"}
        http_client = httpx.AsyncClient(base_url=self.base_url, headers=headers)
        http_client.event_hooks["request"] = self._request_event_hooks
        http_client.event_hooks["response"] = self._response_event_hooks
        return http_client
