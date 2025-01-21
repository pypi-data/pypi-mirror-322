import json
from typing import Optional

from selenium.webdriver.remote.webelement import WebElement


class ElementUtils:
    @staticmethod
    def get_offset(value: str, element: Optional[WebElement] = None) -> Optional[tuple[int, int]]:
        if not value:
            return None

        default_x = element.size['width'] if element else 0
        default_y = element.size['height'] if element else 0

        value_map = json.loads(value)
        offset_x = value_map.get('offset_x', default_x)
        offset_y = value_map.get('offset_y', default_y)
        return offset_x, offset_y


    @staticmethod
    def get_parent_offset(value: str, element: Optional[WebElement] = None) -> Optional[tuple[int, int]]:
        if not value:
            return None

        default_x = element.size['width'] if element else 0
        default_y = element.size['height'] if element else 0

        value_map = json.loads(value)
        offset_x = value_map.get('offset_X', default_x)
        offset_y = value_map.get('offset_Y', default_y)
        return offset_x, offset_y