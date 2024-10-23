#  The module logger, keeps the latest message for each module.


class ModuleLogger:

    def __init__(self) -> None:
        self.messages: dict[str, tuple[str, int, int]] = {}

    def log(self, module: str, message: str, percent: int, level: int) -> None:
        self.messages[module] = (message, percent, level)


module_logger = ModuleLogger()
