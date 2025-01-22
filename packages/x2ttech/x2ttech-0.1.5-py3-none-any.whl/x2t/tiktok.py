from requests import post, put, patch, delete, Response
from typing import Callable, Dict
from datetime import datetime
from urllib.parse import urlencode


class TikTok:

    @staticmethod
    def requestCommon(
        base_url: str,
        endpoint: str,
        method: Callable,
        params: Dict[str, str] = None,
        headers: Dict[str, str] = None,
        body: Dict = None,
    ) -> Response:
        if method not in {post, put, patch, delete}:
            raise ValueError(
                "Invalid method. Method must be one of: post, put, patch, delete.")

        params = params or {}

        if "timestamp" not in params:
            params["timestamp"] = str(int(datetime.timestamp(datetime.now())))

        query_string = urlencode(params)
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?{query_string}"
        return method(url=url, headers=headers, json=body)
