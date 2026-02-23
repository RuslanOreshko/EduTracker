import logging
import sys


def setup_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)