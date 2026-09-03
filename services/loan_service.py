import logging
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.utils.exceptions import InvalidFileException
from config import file_name_member, file_name, file_name_loan
from models.book import StateBook
from services.service_static import ServiceStatic
from utils.storage import Storage
from utils.contracts import BaseService

logger = logging.getLogger(__name__)


class LoanService(BaseService):

    @classmethod
    def service_name(cls) -> str:
        return "LoanService"

    # =========================================================
    # اطلاعات موقت مورد استفاده سه متد
    # =========================================================

    _book_id: int | None = None
    _code_meli: str = ""
    _firstname: str = ""
    _lastname: str = ""
    _state: StateBook | None = None

    # =========================================================
    # متد اصلی
    # =========================================================

    @classmethod
    def change_loan_state(
        cls,
        put_id: int,
        code_meli: str,
        state: StateBook
    ) -> None:
        logger.debug("شروع تابع ذخیره اطلاعات اولیه")

        # ==========================================
        # ذخیره اطلاعات اولیه
        # ==========================================

        cls._book_id = put_id
        cls._code_meli = code_meli
        cls._state = state

        # ==========================================
        # 1. پیدا کردن عضو
        # ==========================================

        if not cls.find_member():
            return

        # ==========================================
        # 2. بررسی کتاب
        # ==========================================

        if not cls.change_book_state():
            return

        # ==========================================
        # 3. ثبت / تغییر سابقه امانت
        # ==========================================

        if not cls.save_loan():
            return

        logger.info("عملیات با موفقیت انجام شد")
        print("عملیات با موفقیت انجام شد")

    # =========================================================
    # متد اول
    # پیدا کردن عضو
    # =========================================================

    @classmethod
    def find_member(cls) -> bool:

        if not Storage.check_file(file_name_member):
            logger.warning(f"فایل یافت نشد, {file_name_member}")
            return False

        wb_member = None

        try:

            wb_member, ws_member = Storage.load_sheet()
            logger.debug("فایل باز شد")

            logger.debug("شروع فرایند پیدا کردن عضو با کد ملی")
            for row in ws_member.iter_rows(min_row=2):

                # ==========================================
                # گرفتن کد ملی از Excel
                # ==========================================

                value = row[3].value

                # فقط کد ملی متنی را بررسی می‌کنیم
                if not isinstance(value, str):
                    continue

                if value.strip() != cls._code_meli.strip():
                    continue

                # ==========================================
                # عضو پیدا شد
                # ==========================================
                logger.info("عضو با کد ملی وارد شده پیدا شد")
                firstname_value = row[0].value
                lastname_value = row[1].value

                if isinstance(firstname_value, str):
                    cls._firstname = firstname_value
                else:
                    cls._firstname = ""

                if isinstance(lastname_value, str):
                    cls._lastname = lastname_value
                else:
                    cls._lastname = ""
                    
                print("عضو پیدا شد")

                print(
                    f"نام: {cls._firstname} "
                    f"{cls._lastname}"
                )

                return True

            # ==========================================
            # عضو پیدا نشد
            # ==========================================

            logger.warning("کاربر با این کد ملی یافت نشد")
            print("کد ملی موجود نمی باشد")
            return False

        except (InvalidFileException, PermissionError) as e:
            logger.exception("خطا در جستجوی عضو")

            print(f"خطا در فایل اعضا: {e}")
            return False

        finally:

            if wb_member is not None:
                wb_member.close()
                logger.debug("فایل بسته شد")

    # =========================================================
    # متد دوم
    # بررسی وضعیت کتاب
    #
    # این متد هنوز وضعیت کتاب را ذخیره نمی‌کند.
    # فقط بررسی می‌کند که عملیات مجاز است یا نه.
    # =========================================================

    @classmethod
    def change_book_state(cls) -> bool:

        if not Storage.check_file(file_name):
            logger.warning(f"فایل یافت نشد, {file_name}")
            return False

        wb_book = None

        try:

            wb_book, ws_book = Storage.workbook()
            logger.debug("فایل باز شد")

            logger.debug("شروع فرایند پیدا کردن کتاب با آی دی")
            for row in ws_book.iter_rows(min_row=2):

                # ==========================================
                # پیدا کردن کتاب
                # ==========================================

                if row[3].value != cls._book_id:
                    continue

                logger.debug("کتاب با آی دی وارد شده پیدا شد")
                print("کتاب پیدا شد")
                print(ServiceStatic.print_book(row))

                # ==========================================
                # امانت گرفتن کتاب
                # ==========================================

                if cls._state == StateBook.BORROWED:
                    logger.info("کتاب در وضعیت امانت میباشد")

                    # کتاب باید موجود باشد
                    if row[4].value != StateBook.AVAILABLE.value:
                        logger.warning("کتاب در وضعیت امانت می باشد")

                        print(
                            "این کتاب قبلاً امانت داده شده"
                        )

                        return False

                    # فقط بررسی شد
                    # هنوز ذخیره نمی‌کنیم

                    return True

                # ==========================================
                # پس دادن کتاب
                # ==========================================

                elif cls._state == StateBook.AVAILABLE:
                    logger.info("کتاب موجود میباشد")

                    # کتاب باید امانت داده شده باشد
                    if row[4].value != StateBook.BORROWED.value:
                        logger.warning("کتاب موجود می باشد")

                        print(
                            "این کتاب در حال حاضر "
                            "امانت داده نشده است"
                        )

                        return False

                    # فقط بررسی شد
                    # هنوز ذخیره نمی‌کنیم

                    return True

                # ==========================================
                # وضعیت نامعتبر
                # ==========================================

                else:
                    logger.warning("وضعیت امانت کتاب صحیح نیست")
                    print(
                        "وضعیت کتاب صحیح نمی باشد"
                    )

                    return False

            # ==========================================
            # کتاب پیدا نشد
            # ==========================================

            logger.warning("کتاب با آی دب وارد شده موجود نمی باشد")
            print("آی دی کتاب موجود نمی باشد")
            return False

        except (InvalidFileException, PermissionError) as e:
            logger.exception("خطا در وضعیت امانت کتاب")

            print(f"خطا در فایل کتاب‌ها: {e}")
            return False

        finally:

            if wb_book is not None:
                wb_book.close()
                logger.debug("فایل بسته شد")

    # =========================================================
    # متد سوم
    # ثبت / تغییر سابقه امانت
    #
    # این متد هیچ ورودی ندارد.
    # اطلاعات را از متغیرهای کلاس می‌گیرد.
    # =========================================================

    @classmethod
    def save_loan(cls) -> bool:

        wb_loan = None

        try:

            # ==========================================
            # باز کردن یا ساخت فایل loans
            # ==========================================
            logger.debug("شروع فرایند باز کردن فایل")

            if file_name_loan.exists():

                wb_loan = load_workbook(file_name_loan)
                ws_loan = wb_loan.worksheets[0]
                logger.info("فایل باز شد")

            else:

                wb_loan = Workbook()
                ws_loan = wb_loan.worksheets[0]

                ws_loan.append([
                    "ID کتاب",
                    "کد ملی",
                    "نام",
                    "نام خانوادگی",
                    "وضعیت کتاب",
                    "تاریخ امانت",
                    "پس داده؟",
                    "تاریخ پس دادن"
                ])
                logger.info("فایل موجود نبود. فایل جدید ساخته شد")

            # =================================================
            # امانت گرفتن کتاب
            # =================================================

            if cls._state == StateBook.BORROWED:
                logger.info("شروع فرایند تغییر و ثبت وضعیت جدید امانت کتاب ")

                # ==========================================
                # ثبت سابقه امانت
                # ==========================================

                ws_loan.append([
                    cls._book_id,
                    cls._code_meli,
                    cls._firstname,
                    cls._lastname,
                    StateBook.BORROWED.value,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "خیر",
                    None
                ])

                # ==========================================
                # ذخیره loans
                # ==========================================

                wb_loan.save(file_name_loan)
                logger.info("وضعیت امانت با موفقیت ثبت شد")

                print(
                    "اطلاعات امانت با موفقیت ثبت شد"
                )

                # ==========================================
                # حالا وضعیت کتاب را تغییر می‌دهیم
                #
                # چون ثبت loan موفق بوده است
                # ==========================================

                wb_book = None

                try:
                    logger.debug("شروع فرایند باز کردن فایل")

                    wb_book, ws_book = Storage.workbook()

                    for row in ws_book.iter_rows(
                        min_row=2
                    ):

                        if row[3].value == cls._book_id:

                            row[4].value = (
                                StateBook.BORROWED.value
                            )
                            logger.debug("کتاب با آی دی وارد شده پیدا شد")
                            break

                    wb_book.save(file_name)
                    logger.debug("فایل سیو شد")

                except (
                    InvalidFileException,
                    PermissionError
                ) as e:
                    logger.exception("خطا در ثبت وضعیت امانت")

                    print(
                        f"خطا در تغییر وضعیت کتاب: {e}"
                    )

                    return False

                finally:

                    if wb_book is not None:
                        wb_book.close()
                        logger.debug("فایل بسته شد")

                return True

            # =================================================
            # پس دادن کتاب
            # =================================================

            elif cls._state == StateBook.AVAILABLE:

                # ==========================================
                # پیدا کردن سابقه امانت فعال
                # ==========================================

                for row in ws_loan.iter_rows(min_row=2):

                    # کد ملی سابقه
                    loan_code_meli = row[1].value

                    # ------------------------------------------
                    # بررسی ID کتاب
                    # ------------------------------------------

                    if row[0].value != cls._book_id:
                        continue

                    # ------------------------------------------
                    # بررسی نوع کد ملی
                    # ------------------------------------------

                    if not isinstance(
                        loan_code_meli,
                        str
                    ):
                        continue

                    # ------------------------------------------
                    # بررسی کد ملی
                    # ------------------------------------------

                    if (
                        loan_code_meli.strip()
                        != cls._code_meli.strip()
                    ):
                        continue

                    # ------------------------------------------
                    # بررسی اینکه هنوز پس داده نشده
                    # ------------------------------------------

                    if row[6].value != "خیر":
                        continue

                    # ==========================================
                    # سابقه امانت پیدا شد
                    # ==========================================

                    # وضعیت سابقه
                    row[4].value = (
                        StateBook.AVAILABLE.value
                    )

                    # پس داده شد
                    row[6].value = "بله"

                    # تاریخ پس دادن
                    row[7].value = (
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )
                    logger.info("وضعیت امانت با موفقیت ثبت شد")

                    # ==========================================
                    # ذخیره loans
                    # ==========================================

                    wb_loan.save(file_name_loan)

                    print(
                        "اطلاعات پس دادن کتاب ثبت شد"
                    )

                    # ==========================================
                    # حالا وضعیت خود کتاب را تغییر می‌دهیم
                    # ==========================================

                    wb_book = None

                    try:

                        wb_book, ws_book = (
                            Storage.workbook()
                        )

                        for book_row in ws_book.iter_rows(
                            min_row=2
                        ):

                            if (
                                book_row[3].value
                                == cls._book_id
                            ):

                                book_row[4].value = (
                                    StateBook.AVAILABLE.value
                                )

                                break

                        wb_book.save(file_name)
                        logger.info("وضعیت کتاب با موفقیت به موجود تغییر کرد")

                    except (
                        InvalidFileException,
                        PermissionError
                    ) as e:
                        logger.exception("خطا در ثبت وضعیت امانت")

                        print(
                            f"خطا در تغییر وضعیت کتاب: {e}"
                        )

                        return False

                    finally:

                        if wb_book is not None:
                            wb_book.close()
                            logger.debug("فایل بسته شد")

                    return True

                # ==========================================
                # سابقه امانت پیدا نشد
                # ==========================================

                logger.warning("سابقه امانت برای این عضو یافت نشد")
                print(
                    "سابقه امانت این کتاب "
                    "برای این عضو پیدا نشد"
                )

                return False

            # =================================================
            # وضعیت نامعتبر
            # =================================================

            else:
                logger.warning("وضعیت کتاب صحیح نیست")

                print(
                    "وضعیت کتاب صحیح نمی باشد"
                )

                return False

        except (
            InvalidFileException,
            PermissionError
        ) as e:
            logger.exception("خطا در فایل امانت")

            print(f"خطا در فایل امانت: {e}")
            return False

        finally:

            if wb_loan is not None:
                wb_loan.close()
                logger.debug("فایل بسته شد")