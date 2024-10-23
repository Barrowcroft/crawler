#  Represnts the crawlers cooler.

from typing import Any

from crawler.crawler.modules.module import Module


class Cooler(Module):
    """Cooler

    Represnts the crawlers cooler.

    Args:
        Module: The Cooler subclasses the Module class.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:

        super().__init__(*args, **kwargs)
