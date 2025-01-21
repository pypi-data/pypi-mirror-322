from time import sleep
from typing import Optional

from appium import webdriver
from appium.webdriver import WebElement
from mag_tools.exception.app_exception import AppException
from mag_tools.model.data_type import DataType
from mag_tools.utils.common.string_utils import StringUtils
from mag_tools.utils.file.file_utils import FileUtils
from mag_tools.utils.file.json_file_utils import JsonFileUtils
from selenium.webdriver import ActionChains

from mag_test.core.app_driver import AppDriver
from mag_test.model.action_type import ActionType
from mag_test.model.control_type import ControlType
from mag_test.utils.table_utils import TableUtils
from mag_test.model.init_status import InitStatus
from mag_test.utils.element_utils import ElementUtils


class EventUtils:
    @staticmethod
    def process(driver: AppDriver, element: WebElement, action: ActionType, value: Optional[str] = None, init_status: Optional[InitStatus] = None):
        control_type = ControlType.get_by_element(element)
        # 按钮、菜单项、标签、文本框、文档、组合框
        if control_type in {ControlType.BUTTON, ControlType.SPLIT_BUTTON, ControlType.MENU_ITEM, ControlType.LABEL, ControlType.EDIT, ControlType.DOC, ControlType.COMBO_BOX}:
            EventUtils.__process_simple(element, action, value)
        # 树项
        elif control_type in {ControlType.TREE_ITEM}:
            EventUtils.__process_tree(driver, element, action, value)
        # TAB项、列表项
        elif control_type in {ControlType.TAB_ITEM, ControlType.LIST_ITEM}:
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
        # 表格
        elif control_type == ControlType.TABLE:
            if value:
                value_array = JsonFileUtils.load_json(value)
                TableUtils.set_table(element, value_array, init_status)
        # 复选按钮、单选按钮
        elif control_type in {ControlType.CHECKBOX, ControlType.RADIO}:  # 复选按钮选择
            value = StringUtils.to_value(value, DataType.BOOLEAN)

            if (value and not element.is_selected()) or (not value and element.is_selected()):
                element.click()
        # PANE
        elif control_type == ControlType.PANE:
            if control_type == ControlType.DATETIME:
                element.send_keys(value)
            else:
                element.clear()
        # 窗口
        elif control_type == ControlType.WINDOW:
            EventUtils.__click_window(driver, value)
        # 工具栏
        elif control_type == ControlType.TOOL:
            EventUtils.__fling(driver, element)
        else:
            raise AppException(f"Unsupported type or action: {control_type}/{action}")

    # @staticmethod
    # def process_event(driver:AppDriver, element:WebElement, element_info : ElementInfo):
    #     if element is None:
    #         raise AppException(f'未找到指定的控件 {element_info}')
    #
    #     return_type = ControlType.get_by_element(element)
    #     # 按钮、菜单项、标签
    #     if return_type in {ControlType.BUTTON, ControlType.SPLIT_BUTTON, ControlType.MENU_ITEM, ControlType.LABEL}:
    #         EventUtils.__process_simple(element, element_info.main_action)
    #     # 文本框、文档、组合框
    #     elif return_type in {ControlType.EDIT, ControlType.DOC, ControlType.COMBO_BOX}:  # 可编辑控件
    #         EventUtils.__process_simple(element, element_info.main_action, element_info.value)
    #     # 树项
    #     elif return_type in {ControlType.TREE_ITEM}:
    #         EventUtils.__process_tree(driver, element, element_info.main_action, element_info.value)
    #     # TAB项、列表项
    #     elif return_type in {ControlType.TAB_ITEM, ControlType.LIST_ITEM}:
    #         actions = ActionChains(driver)
    #         actions.move_to_element(element).click().perform()
    #     # 表格
    #     elif return_type == ControlType.TABLE:
    #         if element_info.attachment:
    #             value_array = JsonFileUtils.load_json(element_info.attachment)
    #             TableUtils.set_table(element, value_array, element_info.main_action)
    #     # 复选按钮、单选按钮
    #     elif return_type in {ControlType.CHECKBOX, ControlType.RADIO}:  # 复选按钮选择
    #         value = StringUtils.to_value(element_info.value, DataType.BOOLEAN)
    #
    #         if (value and not element.is_selected()) or (not value and element.is_selected()):
    #             element.click()
    #     # PANE
    #     elif return_type == ControlType.PANE:
    #         if element_info.main_type == ControlType.DATETIME:
    #             element.send_keys(element_info.value)
    #         else:
    #             element.clear()
    #     # 窗口
    #     elif return_type == ControlType.WINDOW:
    #         EventUtils.__click_window(driver, element_info.value)
    #     # 工具栏
    #     elif return_type == ControlType.TOOL:
    #         EventUtils.__fling(driver, element)
    #     else:
    #         raise AppException(f"Unsupported type or action: {element_info.main_type}/{return_type}")

    @staticmethod
    def click_offset(driver: webdriver.Remote, element: WebElement, offset: tuple[int, int] = None):
        if offset:
            offset_x, offset_y = offset
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(element, offset_x, offset_y).click().perform()
            sleep(1)
        else:
            element.click()

    @staticmethod
    def process_virtual(control_type: ControlType, action: ActionType, value: str):
        if control_type == ControlType.FILE:
            if action == ActionType.CLEAR_DIR:
                FileUtils.clear_dir(value)
            elif action == ActionType.DELETE_DIR:
                FileUtils.delete_dir(value)
            elif action == ActionType.DELETE_FILE:
                FileUtils.delete_file(value)

    @staticmethod
    def __click_window(driver: AppDriver, value: str):
        if value == 'close':
            driver.close()
            driver.quit_app()
        elif value == 'max':
            driver.maximize_window()
        elif value == 'min':
            driver.minimize_window()

    @staticmethod
    def __process_simple(element: WebElement, action: ActionType, value: str = None):
        element.click()
        if action == ActionType.SEND_KEYS:
            element.send_keys(value)
        elif action == ActionType.CLEAR:
            element.clear()
        elif action == ActionType.SET_TEXT:
            element.clear()
            element.send_keys(value)

    @staticmethod
    def __fling(driver:AppDriver, element: WebElement):
        actions = ActionChains(driver)
        actions.move_to_element(element).release().perform()

    @staticmethod
    def __process_tree(driver:AppDriver, element: WebElement, action:ActionType, value: Optional[str] = None):
        if action == ActionType.SELECT:
            offset = ElementUtils.get_offset(value) if value else (-20, 8)
            EventUtils.click_offset(driver, element, offset)
        elif action == ActionType.CLICK:
            element.click()