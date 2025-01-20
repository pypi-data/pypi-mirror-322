from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class UserStats:
    _id: str
    """Returns the ID of the user."""
    coins: int
    """Returns the coins of the user."""
    claimed: datetime | str
    """Returns the last datetime, when the user claimed his daily coins. Returns 'Never', when the user never claimed his daily coins before."""
    streak: int
    """Returns the user's current daily streak."""
    max_streak: int
    """Returns the user's max daily streak."""
    in_guild: bool
    """Returns if the user is in the guild."""

    @property
    def id(self) -> str:
        """Returns the ID of the user."""
        return self._id