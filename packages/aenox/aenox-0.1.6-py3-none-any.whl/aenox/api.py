import os
from datetime import date, datetime
from typing import overload

import httpx
from dotenv import load_dotenv

from .errors import InvalidAPIKey, NotFound, UserNotFound, CooldownError, NoMoreCreditsAvailable, UserNotInGuild
from .models import UserStats

BASE_URL = 'https://api.aenox.xyz/v1/'


def _stats_dict(data: dict[str, int]) -> dict[date, int]:
    return {datetime.strptime(d, "%Y-%m-%d").date(): count for d, count in data.items()}


class AenoXAPI:
    """A class to interact with the API of AenoX.

    Parameters
    ----------
    api_key:
        The API key to use.
    httpx_client:
        An existing httpx client to use.

    Raises
    ------
    InvalidAPIKey:
        Raised when an invalid API key is provided.
    """
    def __init__(self, api_key: str, httpx_client: httpx.Client | None = None):
        self._httpx_client: httpx.Client | None = httpx_client

        if httpx_client is None:
            self._httpx_client = httpx.Client()
        if api_key is None:
            raise InvalidAPIKey

        self._header = {"key": api_key, "accept": "application/json"}

    @overload
    def _get(self, endpoint: str) -> dict:
        ...

    @overload
    def _get(self, endpoint: str, stream: bool) -> bytes:
        ...

    def _get(self, endpoint: str, stream: bool = False):
        response = self._httpx_client.get(BASE_URL + endpoint, headers=self._header)

        if response.status_code == 401:
            raise InvalidAPIKey()
        elif response.status_code == 429:
            raise CooldownError
        elif response.status_code == 404:
            response = response.json()
            message = response.get("detail")
            if "user" in message.lower() or "member" in message.lower():
                raise UserNotFound()
            elif "credits" in message.lower():
                raise NoMoreCreditsAvailable
            elif "guild" in message.lower():
                raise UserNotInGuild
            raise NotFound()

        if stream:
            return response.read()

        return response.json()

    def get_user(self, user_id: int) -> UserStats:
        """Get the user's level stats.

        Parameters
        ----------
        user_id:
            The user's ID.

        Raises
        ------
        UserNotFound:
            The user was not found.
        NoMoreCreditsAvailable:
            No more credits. Check /api on Discord.
        CooldownError:
            You are on cooldown.
        """
        data = self._get(f"user/{user_id}")

        def parse_datetime(date_str: str) -> datetime:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                return None


        if data:
            for item in data:
                if item['claimed'] == 0:
                    item['claimed'] = "Never"
                else:
                    item['claimed'] = parse_datetime(str(item.get('claimed', '')))

                if "_id" in item:
                    del item['_id']

            return UserStats(str(user_id), **data[0])
        else:
            raise ValueError("Die Liste data ist leer und kann nicht verarbeitet werden.")
