#  Represents a salvage item in the crawler's hold.

import crawler.constants as c


class Salvage:
    """Salvage

    Represents a salvage item in the crawler's hold.
    """

    @property
    def health_level(self) -> int:
        #  Returns the health level. 3 = Danger, 2 = Warning, 1 = Notice, 0 = Normal.
        if self.health <= 25:
            return 3
        elif self.health <= 50:
            return 2
        elif self.health <= 75:
            return 1
        else:
            return 0

    def destroy(self) -> None:

        self.health = 0
        self.status = c.SALVAGE_STATUS_DESTROYED

    def __init__(
        self,
        name: str,
        description: str,
        health: int,
        status: str = c.SALVAGE_STATUS_OK,
    ) -> None:

        self.name: str = name
        self.description: str = description

        self.health: int = health
        self.status: str = status
