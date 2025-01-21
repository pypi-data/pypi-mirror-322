from icecream import ic
from loguru import logger


def init_icecream() -> None:
    ic.configureOutput(
        prefix="", outputFunction=lambda s: logger.opt(depth=2).log("ICECREAM", s)
    )
