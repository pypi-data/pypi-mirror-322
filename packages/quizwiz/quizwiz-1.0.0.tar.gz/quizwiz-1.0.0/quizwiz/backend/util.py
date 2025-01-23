"""
util.py

This module contains utility functions and classes that provide common and reusable 
operations for the application. The utilities include functionality to extract 
non-None fields from objects, among other potential helper methods.

Main Classes:
    - Util: A utility class for common helper methods.

Main Functions:
    - extract_non_none_fields: A method to extract non-None fields from an object 
      and return them in a formatted string.

This module is intended to be used across different parts of the application where 
common utility functions are needed, providing reusable and easy-to-understand solutions.

Example:
    >>> from util import Util
    >>> obj = SomeObject(admin_id=1, admin_knox_id=None)
    >>> Util.extract_non_none_fields(obj, ["admin_knox_id", "admin_id"])
    'admin_id=1'
"""


class Util:
    """
    A utility class that provides helpful methods for various common tasks.
    This class includes methods for extracting non-None fields from objects
    and can be extended to include other utility functions.
    """

    @classmethod
    def extract_non_none_fields(cls, obj, fields):
        """
        Extracts specified fields from the given object and returns a formatted
        string containing only the fields with non-None values.

        Args:
            obj: The object from which fields will be extracted.
            fields (list): A list of field names (as strings) to be checked
                           in the given object.

        Returns:
            str: A formatted string containing field names and their corresponding
                 non-None values in the form "field_name=value". Fields with
                 None values are omitted.

        Example:
            >>> query_data = QueryData(admin_knox_id=None, admin_id=2)
            >>> Util.extract_non_none_fields(query_data, ["admin_knox_id", "admin_id"])
            'admin_id=2'

        KOR:
            주어진 객체에서 특정 필드 값을 추출하여 None이 아닌 항목만 문자열로 반환.
        """
        return " ".join(
            f"{field}={value}"
            for field in fields
            if (value := getattr(obj, field, None)) is not None
        )
