"""Services for coupons app."""
from datetime import datetime
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from xlrd import open_workbook, xldate_as_tuple
from xlrd.biffh import XLRDError
from xlrd.book import Book
from xlrd.sheet import Sheet
from xlrd.xldate import XLDateAmbiguous

from coupons.constants import DISTANCE_INDEX, PRICE_AND_DISTANCE
from coupons.enums import CouponsErrors
from coupons.models import Coupon
from user_auth.models import BoltUser

from .logger import ExcelLogger
from .utils import is_float, is_integer


class CouponService:
    """The service describes methods of working with the Coupon instance."""
    def get_coupon_by_distance(self, user: BoltUser) -> Coupon or ValidationError:
        """
        Get coupon by distance and assign it to user.
        
        :param user: user.
        :raises ValidationError: if any coupons do not exists.
        :return: coupon.
        """
        coupons = Coupon.objects.filter(user__isnull=True)
        self._check_distance(user.distance)
        coupon = self._get_coupon_by_distance(user.distance, coupons)

        if not coupon:
            raise ValidationError(detail=CouponsErrors.NO_COUPONS_AVAILIABLE.value, code=HTTP_400_BAD_REQUEST)

        coupon.user = user
        coupon.save()

        return coupon
        
    @staticmethod        
    def _check_distance(distance: int) -> None or ValidationError:
        """
        Check if the user's distance is enough to get the coupon.
        
        :param distance: user distance.
        :raises ValidationEror: if user distance to small.
        :return: None.
        """
        if distance < PRICE_AND_DISTANCE[0][DISTANCE_INDEX]:
            raise ValidationError(detail=CouponsErrors.TOO_SMALL_DISTANCE.value, code=HTTP_400_BAD_REQUEST)

    @staticmethod
    def _get_coupon_by_distance(distance: int, coupons: QuerySet[Coupon]) -> Coupon or None:
        """
        Get coupon by distance.
        
        :param distance: user distance.
        :param coupons: list of availiable coupons.
        :return: coupon if found else None.
        """
        if distance >= PRICE_AND_DISTANCE[0][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[1][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[0][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[1][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[2][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[1][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[2][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[3][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[2][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[3][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[3][DISTANCE_INDEX]).first()


class ExcelParserService:
    """Reading data from Excel into a dictionary."""
    def __init__(self, file: InMemoryUploadedFile, headers_map_fields: dict or None, logger: ExcelLogger) -> None:
        self._logger = logger
        self.workbook = self.get_workbook(file)
        self._headers_map_fields = headers_map_fields

    def get_headers(self, sheet: Sheet) -> list or None:
        """
        Get headers from sheet.
        
        :param sheet: sheet from excel file.
        :return: headers.
        """
        if not sheet:
            self._handle_error(Exception('Error during excel file import by user'), self._logger.error_patterns['only_headers'])

        try:
            headers = [cell for cell in sheet.row_values(0)]
            self.validate_headers(headers)

            if self._headers_map_fields:
                headers = self.headers_mapping(headers)
        except Exception as error:
            headers = None
            self._handle_error(error, self._logger.error_patterns['only_headers'])

        return headers

    def headers_mapping(self, headers: list) -> list:
        """
        Mapping excel headers.
        
        :param headers: headers.
        :return: list of headers.
        """
        mapped = []
        if len(headers) == len(self._headers_map_fields):
            for header in headers:
                mapped.append(self._headers_map_fields[header])

        return mapped

    def validate_headers(self, headers: tuple) -> None:
        """
        Validate headers.
        
        :param headers: headers.
        :return: None
        """
        if len(headers) < len(self._headers_map_fields):
            self._handle_error(Exception("Broken headers.", self._logger['only_headers']))

    def get_rows(self, sheet: Sheet) -> list:
        """
        Get rows from sheet.

        :param sheet: sheet from excel file.
        :return: list of rows.
        """
        rows = []
        try:
            for row in list(sheet.get_rows())[1:]:
                self.validate_row(row)
                rows.append(row)
        except Exception as error:
            self._handle_error(error, self._logger.error_patterns.get('only_headers', ''))

        return rows

    def validate_row(self, row: list) -> None:
        """
        Validate row.

        :param row: exel row.
        :return: None
        """
        promocod_index = 0
        price_index = 1
        distance_index = 2
        date_index = 3

        if len(row[promocod_index].value) != 8 and not row[promocod_index].value.isupper():
            self._handle_error(Exception('Invalid promocod.'), 'Неправильний формат промокоду.')

        if not is_float(row[price_index].value) or not is_integer(row[price_index].value):
            self._handle_error(Exception('Invalid price.'), 'Ціна має бути написана числом.')

        if not is_float(row[distance_index].value) or not is_integer(row[distance_index].value):
            self._handle_error(Exception('Invalid distance.'), 'Відстань має бути написана числом.')

        try:
            row[date_index] = datetime(*xldate_as_tuple(row[date_index].value, self.workbook.datemode))
        except XLDateAmbiguous:
            self._handle_error(Exception('Invalid distance.'), 'Неправильний формат дати.')

    def get_workbook(self, file: InMemoryUploadedFile) -> Book or None:
        """
        Get workbook of excel file.

        :param file: excel file.
        :return: workbook.
        """
        try:
            return open_workbook(file_contents=file.read())
        except Exception as error:
            self._handle_error(error, self._logger.error_patterns['no_excel'])

    def get_sheet(self, sheet_index: Union[int, None] = None, sheet_name: str='') -> Sheet or None:
        """
        Get a sheet from an Excel file by sheet name or sheet index.
        
        :param sheet_index: sheet index. Start from zero.
        :param sheet_name: sheet name.

        :return: sheet.
        """
        result = self.__get_sheet_by_name(sheet_name)
        if result: return result
            
        result = self.__get_sheet_by_index(sheet_index)
        if result: return result
            
    def __get_sheet_by_name(self, sheet_name: str) -> Sheet or None:
        """
        Get sheet by name.

        :param workbook: workbook.
        :param sheet_name: sheet name.
        
        :return: Sheet or None.
        """
        if sheet_name:
            try:
                return self.workbook.sheet_by_name(sheet_name)
            except XLRDError as error:
                return None
            
    def __get_sheet_by_index(self, sheet_index: str) -> Sheet or None:
        """
        Get sheet by index.

        :param workbook: workbook.
        :param sheet_index: sheet index.
        
        :return: Sheet or None.
        """
        if isinstance(sheet_index, int):
            try:
                return self.workbook.sheet_by_index(sheet_index)
            except XLRDError as error:
                return None

    def _handle_error(self, error: Exception, logger_pattern: str) -> None:
        """
        Handle errors and show messages.
        
        :param error: instance of Exception class.
        :param logger_patern: pattern of error from custom logger.

        :return None:
        """
        self._logger.add_error(logger_pattern)

    def to_dict(self, sheet_index: Union[int, None] = None, sheet_name: str='') -> list:
        """
        Get Excel data as a list of dictionaries.

        :param sheet_index: index of excel sheet.
        :param sheet_name: name of excel sheet.
        :return: list of dictionaries with excel data or None if workbook/sheet not found.
        """
        if not self.workbook:
            err_msg = 'Workbook does not exists.'
            self._handle_error(Exception(err_msg), self._logger.error_patterns['no_excel'])
            return []

        sheet = self.get_sheet(sheet_index, sheet_name)

        if not sheet:
            err_msg = 'Sheet does not exists.'
            self._handle_error(Exception(err_msg), self._logger.error_patterns['no_excel'])
            return []

        objects_: list = []

        headers = self.get_headers(sheet)
        rows = self.get_rows(sheet)
        
        for row in rows:
            objects_.append(
                dict(
                    zip([header for header in headers],
                        [cell.value if hasattr(cell, 'value') else cell for cell in row])))
            
        return objects_
