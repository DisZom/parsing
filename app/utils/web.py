from typing import Self
from utils.logger import Logger

from dataclasses import dataclass
from enum import Enum

import httpx
import time


class WebRequestMethods(Enum):
    GET = "GET"
    POST = "POST"

@dataclass(frozen = True)
class WebResponse:
    StatusCode: int
    Content: str

class WebClient:
    def __enter__(self) -> Self:
        self.__session = httpx.Client()
        return self
    
    def __exit__(self, exc_type, exc, tb) -> None:
        self.__session.close()

    def Fetch(self, url: str, *, method: WebRequestMethods = WebRequestMethods.GET, **kwargs) -> WebResponse | None:
        Response: httpx.Response = self.__session.request(method.value, url, **kwargs)
        if Response.status_code == 429:
            Logger.warning("Too Many Requests, Waiting...")
            time.sleep(float(Response.headers.get("Retry-After", 1)))
            return self.Fetch(url, method = method, **kwargs)

        elif Response.status_code == 404:
            Logger.error(f"Error 404 for {url}")
            return None

        return WebResponse(Response.status_code, Response.content.decode())
