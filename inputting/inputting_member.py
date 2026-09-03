import logging

from models.member import Member, RoleMember
from utils.storage import ErrorCodeMeli

logger = logging.getLogger(__name__)

# =========================================================
# گرفتن اطلاعات عضو برای ثبت
# =========================================================

def input_member() -> Member:
    logger.debug("شروع فرایند وارد کردن اطلاعات عضو")

    while True:
        firstname = input("نام: ")
        if firstname == "":
            print("لطفا نام را وارد کنید")
            logger.warning("نام کاربر وارد نشد")

            continue

        else:
            break


    while True:
        lastname = input("نام خانوادگی: ")
        if lastname == "":
            print("لطفا نام خانوادگی را وارد کنید")
            logger.warning("نام خانوادگی کاربر وارد نشد")

            continue

        else:
            break

    phone = input("تلفن: ")

    code_meli = input("کد ملی: ")



    while True:

        role_choice = input(
            "وضعیت = (1: عضو کتابخانه / 2: کاربر مهمان): "
        )

        if role_choice == "1":
            role = RoleMember.USER
            break

        elif role_choice == "2":
            role = RoleMember.GUEST
            break

        else:
            logger.warning("کد وارد شده وضعیت عضو صحیح نیست")
            print("کد وارد شده معتبر نمی‌باشد.")

    city = input("شهر: ")

    address = input("آدرس: ")

    email = input("ایمیل: ")

    logger.debug("پایان فرایند وارد کردن اطلاعات عضو")

    return Member(
        firstname=firstname,
        lastname=lastname,
        n_phone=phone,
        code_meli=code_meli,
        role=role,
        city=city,
        address=address,
        email=email
    )


# =========================================================
# گرفتن اطلاعات برای ویرایش عضو
# =========================================================

def input_member_edit() -> tuple[str, str]:
    logger.debug("شروع فرایند وارد کردن اطلاعات عضو جهت ویرایش")


    choice = input("""
کدام آیتم تغییر کند؟

1: نام
2: نام خانوادگی
3: تلفن
4: کد ملی
5: عضویت
6: شهر
7: آدرس
8: ایمیل

انتخاب:
""")

    if choice == "1":

        while True:
            change = input("نام جدید: ")
            if change == "":
                print("لطفا نام جدید را وارد کنید")
                logger.debug("اطلاعات جهت تغییر دریافت نشد")
                continue
            else:
                logger.debug("اطلاعات جهت تغییر دریافت شد")
                break


    elif choice == "2":
        while True:
            change = input("نام خانوادگی جدید: ")
            if change == "":
                print("لطفا نام خانوادگی جدید را وارد کنید")
                logger.debug("اطلاعات جهت تغییر دریافت نشد")
                continue
            else:
                logger.debug("اطلاعات جهت تغییر دریافت شد")
                break

    elif choice == "3":
        change = input("تلفن جدید: ")


    elif choice == "5":

        while True:

            role_choice = input(
                "1: عضو کتابخانه / 2: کاربر مهمان: "
            )

            if role_choice == "1":
                change = RoleMember.USER.value
                logger.debug("اطلاعات جهت تغییر دریافت شد")
                break

            elif role_choice == "2":
                change = RoleMember.GUEST.value
                logger.debug("اطلاعات جهت تغییر دریافت شد")
                break

            else:
                logger.warning("وضعیت عضویت غلط وارد شد")
                print("انتخاب نامعتبر است.")

    elif choice == "6":
        change = input("شهر جدید: ")
        logger.debug("اطلاعات جهت تغییر دریافت شد")


    elif choice == "7":
        change = input("آدرس جدید: ")
        logger.debug("اطلاعات جهت تغییر دریافت شد")


    elif choice == "8":
        change = input("ایمیل جدید: ")
        logger.debug("اطلاعات جهت تغییر دریافت شد")


    else:
        print("انتخاب نامعتبر است.")
        logger.warning("انتخاب وردی جهت تغیر نامعتبر است")

        return "", ""

    logger.debug("پایان فرایند دریافت وردی اطلاعات جهت تغییر")
    return choice, change


# =========================================================
# گرفتن کد ملی
# =========================================================



def input_code_meli() -> str:

    logger.debug("شروع فرایند دریافت کد ملی")
    code_meli = input("کد ملی را وارد کنید: ")

    if len(code_meli) != 10 or not code_meli.isdigit():
        logger.warning("اطلاعات وردی کد ملی غلط است")
        raise ErrorCodeMeli(code_meli)

    logger.debug("پایان فرایند دریافت کد ملی")
    return code_meli