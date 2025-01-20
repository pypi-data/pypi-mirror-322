from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._client import ShangshanAI


class BaseAPI:
    _client: ShangshanAI

    def __init__(self, client: ShangshanAI) -> None:
        self._client = client
        self._delete = client.delete
        self._get = client.get
        self._post = client.post
        self._put = client.put
        self._patch = client.patch
        self._get_api_list = client.get_api_list
