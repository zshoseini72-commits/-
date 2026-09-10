import logging
from inputting.inputting_book import input_book, input_book_edit, input_book_id
from inputting.inputting_member import input_member, input_member_edit, input_code_meli
from models.book import StateBook
from services.book_service import BookService
from services.member_service import MemberService
from services.loan_service import LoanService
from services.service_static import ServiceStatic
from utils.storage import ErrorCodeMeli
from utils.logger import setup_logging
from utils.ui import success, error, warning, title
setup_logging()
logger = logging.getLogger(__name__)


# =========================================================
# منوی کتاب‌ها
# =========================================================

def book_menu() -> None:
    logger.debug("شروع تابع منو")

    while True:

        title("مدیریت کتاب‌ها")
        print("""
========================================
              مدیریت کتاب‌ها
========================================

1. ثبت کتاب
2. نمایش کتاب‌ها
3. جستجوی کتاب
4. ویرایش کتاب
5. حذف کتاب

0. بازگشت
========================================
""")

        choice = input("انتخاب شما: ")

        # -----------------------------------------
        # ثبت کتاب
        # -----------------------------------------

        if choice == "1":
            logger.debug("انتخاب ثبت کتاب")

            try:
                book = input_book()

                result =  BookService.add_book(book)

                print(result)

                #برای اجرای Generic
                # print(BookService.repository.all())

                # یا از جای دیگه اجرا کن
                # s = SimpleRepository[Book]()
                # s.add(book)
                # print(s.all())


            except ValueError as error:
                logger.exception("خطا در ثبت کتاب")
                print(f"خطا: {error}")

        # -----------------------------------------
        # نمایش کتاب‌ها
        # -----------------------------------------

        elif choice == "2":
            logger.debug("انتخاب نمایش کتاب")

            BookService.show_books()

        # -----------------------------------------
        # جستجوی کتاب
        # -----------------------------------------

        elif choice == "3":
            logger.debug("انتخاب جستجوی کتاب")

            put_id = input_book_id()

            print(BookService.find_book(put_id))

        # -----------------------------------------
        # ویرایش کتاب
        # -----------------------------------------

        elif choice == "4":
            logger.debug("انتخاب ویرایش کتاب")

            put_id = input_book_id()

            choice_edit, change = input_book_edit()

            if not choice_edit:
                continue

            BookService.edit_book(
                put_id,
                choice_edit,
                change
            )

        # -----------------------------------------
        # حذف کتاب
        # -----------------------------------------

        elif choice == "5":
            logger.debug("انتخاب حذف کتاب")

            put_id = input_book_id()

            print(BookService.remove_book(put_id))

        # -----------------------------------------
        # بازگشت
        # -----------------------------------------

        elif choice == "0":
            logger.debug("انتخاب بازگشت")


            break

        else:
            logger.info("انتخاب نامعتبر در منو")
            warning("انتخاب نامعتبر است.")


# =========================================================
# منوی اعضا
# =========================================================

def member_menu() -> None:
    logger.debug("شروع منوی اعضا")

    while True:

        title("مدیریت اعضا")
        print("""
========================================
              مدیریت اعضا
========================================

1. ثبت عضو
2. نمایش اعضا
3. جستجوی عضو
4. ویرایش عضو
5. حذف عضو

0. بازگشت
========================================
""")

        choice = input("انتخاب شما: ")

        # -----------------------------------------
        # ثبت عضو
        # -----------------------------------------

        if choice == "1":
            logger.debug("انتخاب ثبت عضو")


            try:

                member = input_member()

                result = MemberService.add_member(member)

                print(result)

            except ValueError as error:
                logger.exception("خطا در ثبت عضو")

                print(f"خطا: {error}")

        # -----------------------------------------
        # نمایش اعضا
        # -----------------------------------------

        elif choice == "2":
            logger.debug("انتخاب نمایش عضو")

            MemberService.show_members()

        # -----------------------------------------
        # جستجوی عضو
        # -----------------------------------------

        elif choice == "3":
            logger.debug("انتخاب جستجوی عضو")


            try:
                code_meli = input_code_meli()
            except ErrorCodeMeli as e:
                error(f"خطا: {e}")
            else:
                MemberService.find_member(code_meli)
                logger.debug("کد ملی دریافت شد")


        # -----------------------------------------
        # ویرایش عضو
        # -----------------------------------------

        elif choice == "4":
            logger.debug("انتخاب ویرایش عضو")


            try:
                code_meli = input_code_meli()
            except ErrorCodeMeli as e:
                error(f"خطا: {e}")
            else:
                choice_edit, change = input_member_edit()
                logger.debug("کد ملی دریافت شد")


                if not choice_edit:
                    logger.info("ورودی ویرایش عضو نامعتبر است")
                    continue

                MemberService.edit_member(
                    code_meli,
                    choice_edit,
                    change
                )

        # -----------------------------------------
        # حذف عضو
        # -----------------------------------------

        elif choice == "5":
            logger.debug("انتخاب حذف عضو")

            try:
                code_meli = input_code_meli()
            except ErrorCodeMeli as e:
                error(f"خطا: {e}")
            else:
                MemberService.remove_member(code_meli)

        # -----------------------------------------
        # بازگشت
        # -----------------------------------------

        elif choice == "0":
            logger.debug("انتخاب بازگشت منوی عضو")


            break

        else:
            logger.warning("انتخاب نامعتبر است")
            warning("انتخاب نامعتبر است.")


# =========================================================
# امانت دادن کتاب
# =========================================================

def borrow_book() -> None:
    logger.debug("انتخاب منوی تغییر وضعیت امانت کتاب")

    title("امانت دادن کتاب")
    print("""
========================================
             امانت دادن کتاب
========================================
""")

    put_id = input_book_id()

    try:
        code_meli = input_code_meli()
    except ErrorCodeMeli as e:
        error(f"خطا: {e}")
    else:
        LoanService.change_loan_state(
        put_id=put_id,
        code_meli=code_meli,
        state=StateBook.BORROWED
        )


# =========================================================
# پس دادن کتاب
# =========================================================

def return_book() -> None:
    logger.debug("انتخاب منوی تغییر وضعیت امانت کتاب")


    title("پس دادن کتاب")
    print("""
========================================
              پس دادن کتاب
========================================
""")

    put_id = input_book_id()

    try:
        code_meli = input_code_meli()
    except ErrorCodeMeli as e:
        error(f"خطا: {e}")

    else:
        LoanService.change_loan_state(
        put_id=put_id,
        code_meli=code_meli,
        state=StateBook.AVAILABLE
        )


# =========================================================
# نمایش آمار
# =========================================================

def show_statistics() -> None:
    logger.debug("انتخاب منوی آمار")



    title("آمار")
    print("""
========================================
                 آمار
========================================
""")

    statistics = ServiceStatic()

    print(statistics)


# =========================================================
# منوی اصلی
# =========================================================

def main() -> None:
    logger.debug("انتخاب منوی سیستم مدیریت کتابخانه")

    while True:

        title("سیستم مدیریت کتابخانه")
        print("""
========================================
          << سیستم مدیریت کتابخانه >>
========================================

1. مدیریت کتاب‌ها
2. مدیریت اعضا
3. امانت دادن کتاب
4. پس دادن کتاب
5. نمایش آمار

0. خروج

========================================
""")

        choice = input("انتخاب شما: ")

        if choice == "1":

            book_menu()

        elif choice == "2":

            member_menu()

        elif choice == "3":

            borrow_book()

        elif choice == "4":

            return_book()

        elif choice == "5":

            show_statistics()

        elif choice == "0":

            success("برنامه بسته شد.")
            break

        else:
            logger.warning("انتخاب نامعتبر در منوی مدیریت کتابخانه")

            warning("انتخاب نامعتبر است.")


# =========================================================
# نقطه شروع برنامه
# =========================================================

if __name__ == "__main__":
    main()
