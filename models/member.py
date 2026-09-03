import logging
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class RoleMember(Enum):
    USER = "عضو"
    GUEST = "مهمان"


class Member:
    def __init__(self, firstname: str,  lastname: str, n_phone: str,  code_meli: str,  role: RoleMember,  city: Optional[str] = None,  address: Optional[str] = None,  email: Optional[str] = None)-> None:
        self.firstname = firstname
        self.lastname = lastname
        self.phone = n_phone
        self.code_meli = code_meli
        self.role = role
        self.city = city
        self.address = address
        self.email = email

    def __str__(self)-> str:
        logger.debug("شروع نمایش عضو ")

        return (
            f"نام: {self.firstname}\n"
            f"نام خانوادگی: {self.lastname}\n"
            f"تلفن: {self.phone}\n"
            f"کد ملی: {self.code_meli}\n"
            f"عضویت: {self.role.value}\n"
            f"شهر: {self.city}\n"
            f"آدرس: {self.address}\n"
            f"ایمیل: {self.email}"
        )

    @staticmethod
    def validate_phone(value: str) -> str:
        logger.debug("شروع اعتبارسنجی تلفن: ")

        if not value.isdigit():
            logger.warning("شماره تلفن شامل حروف یا کاراکتر غیرعددی است")
            raise ValueError("شماره تلفن باید فقط شامل ارقام باشد.")

        if len(value) != 11:
            logger.warning("طول شماره تلفن نامعتبر است")
            raise ValueError("شماره تلفن باید 11 رقم باشد.")

        logger.debug("اعتبارسنجی تلفن با موفقیت انجام شد")
        return value


    @property
    def phone(self)-> str:
        return self._phone

    @phone.setter
    def phone(self, value: str)-> None:
        self._phone = self.validate_phone(value)


    @staticmethod
    def validate_code_meli(value: str) -> str:
        logger.debug("شروع اعتبارسنجی کد ملی: ")

        if not value.isdigit():
            logger.warning("کد ملی شامل حروف یا کاراکتر غیرعددی است")
            raise ValueError("کد ملی باید فقط شامل ارقام باشد.")

        if len(value) != 10:
            logger.warning("طول کد ملی نامعتبر است")
            raise ValueError("کد ملی باید 10 رقم باشد.")

        logger.debug("اعتبارسنجی کد ملی با موفقیت انجام شد")
        return value


    @property
    def code_meli(self)->str:
        return self._code_meli

    @code_meli.setter
    def code_meli(self, value:str)-> None:
        self._code_meli = self.validate_code_meli(value)


