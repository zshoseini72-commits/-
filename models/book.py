import logging
from dataclasses import dataclass, field
from enum import Enum
from config import last_id_file

logger = logging.getLogger(__name__)


class StateBook(Enum):
    AVAILABLE= "موجود"
    BORROWED= "امانت داده شده"
    UN_AVAILABLE= "ناموجود"


class ID:

    @staticmethod
    def get_id() -> int:
        logger.debug("شروع تابع تولید آی‌دی")

        last_id = 999

        if last_id_file.exists():
            logger.debug("شروع خواندن آخرین آی‌دی تولید شده")

            with open(last_id_file, "r") as f:
                last_id = int(f.read())

            logger.info(f"آخرین آی‌دی خوانده شد: {last_id}")

        new_id = last_id + 1

        with open(last_id_file, "w") as f:
            f.write(str(new_id))

        logger.info(f"آی‌دی جدید در فایل نوشته شد: {new_id}")

        return new_id

@dataclass
class Book:

    title: str
    author: str
    year: int
    id: int = field(init=False)


    state: StateBook = field(default=StateBook.AVAILABLE)

    def __post_init__(self) -> None:
        self.id = ID.get_id()
        logger.debug(f"کتاب با عنوان «{self.title}» و آی‌دی {self.id} ایجاد شد")