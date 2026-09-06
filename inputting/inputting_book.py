import logging
from models.book import Book

logger = logging.getLogger(__name__)


# =========================================================
# گرفتن اطلاعات برای ثبت کتاب
# =========================================================

def input_book() -> Book:

    logger.debug("شروع فرایند دریافت اطلاعات کتاب")

    title = input("عنوان کتاب: ")
    author = input("نویسنده: ")

    while True:
        try:
            year = int(input("سال انتشار: "))
            break
        except ValueError:
            logger.warning("سال انتشار صحیح وارد نشد")
            print("سال انتشار باید عدد باشد.")

    logger.debug("پایان فرایند دریافت اطلاعات کتاب")

    return Book(
        title=title,
        author=author,
        year=year
    )

# =========================================================
# گرفتن اطلاعات برای ویرایش کتاب
# =========================================================

def input_book_edit() -> tuple[str, str]:

    logger.debug("شروع فرایند دریافت اطلاعات کتاب جهت ویرایش")


    choice = input("""
کدام آیتم تغییر کند؟

1: نام کتاب
2: نام نویسنده
3: سال انتشار

انتخاب:
""")

    if choice == "1":
        change = input("عنوان جدید کتاب: ")

    elif choice == "2":
        change = input("نام نویسنده جدید: ")

    elif choice == "3":

        while True:
            change = input("سال انتشار جدید: ")

            try:
                int(change)
                break
            except ValueError:
                logger.warning("سال صحیح وارد نشده است")
                print("سال باید عدد باشد.")

    else:
        print("انتخاب نامعتبر است.")
        logger.warning("ورودی اشتباه انتخاب شده است")
        return "", ""

    logger.debug("پایان فرایند دریافت اطلاعات جهت ویرایش کتاب")
    return choice, change


# =========================================================
# گرفتن ID کتاب
# =========================================================

def input_book_id() -> int:
    logger.debug("شروع فرایند دریافت آی دی کتاب")

    while True:
        try:
            book_id=int(input("آی دی کتاب را وارد کنید: "))
            break
        except ValueError:
            logger.warning("آی دی صحیح وارد نشد")
            print("لطفا عدد وارد کنید")

    logger.debug("پایان فرایند دریافت آی دی کتاب")
    return book_id