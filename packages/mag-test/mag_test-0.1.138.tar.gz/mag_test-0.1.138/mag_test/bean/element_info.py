import os
from typing import Any, Optional

from mag_tools.utils.common.string_utils import StringUtils

from mag_test.bean.control import Control
from mag_test.model.control_type import ControlType
from mag_test.model.action_type import ActionType
from mag_test.model.menu_type import MenuType


class ElementInfo:
    """
    控件信息，用于查询条件
    """
    def __init__(self, element_type:ControlType, name_path:Optional[str]=None, id_path:Optional[str]=None,
                 class_name:Optional[str]=None, parent_name:Optional[str] = None,parent_type:Optional[ControlType]=None,
                 parent_id:Optional[str]=None, parent_class:Optional[str]=None, value:Optional[Any]=None,
                 pop_window:Optional[str]=None, home_dir:Optional[str]=None,):
        """
        控件信息，用于查询条件
        :param name_path: 控件路径，格式：主控件名{动作}/子控件名{动作}/菜单项名{动作}
        :param id_path: 控件标识路径，格式：主控件ID{动作}/子控件名{动作}/菜单项名{动作}
        :param element_type: 控件类型,不能为空
        :param class_name: 控件类名
        :param parent_name: 父控件名，父控件通常为容器
        :param parent_id: 父控件标识，AutomationId（AccessibilityId）
        :param parent_type: 父控件类型
        :param parent_class: 父控件类名
        """
        self.__main_element = Control(control_type=element_type, class_name=class_name)
        self.__parent: Optional[Control] = None
        self.__child: Optional[Control] = None
        self.pop_menu: Optional[Control] = None
        self.__home_dir = home_dir

        if parent_id or parent_name or parent_type or parent_class:
            self.__parent = Control(name=parent_name, automation_id=parent_id, control_type=parent_type, class_name=parent_class)

        self.value = value
        if value and self.main_type == ControlType.TABLE and '.json' in value:
            self.value = os.path.join(os.path.join(self.__home_dir, 'attachment'), value)

        self.pop_window = pop_window

        if element_type == ControlType.MENU:
            self.menu_items = name_path.split('/') if name_path else id_path.split('/') if id_path else []
        else:
            self.__parse_name_path(name_path)
            self.__parse_id_path(id_path)

    @property
    def main_info(self):
        return self.__main_element

    @property
    def main_name(self):
        return self.__main_element.name

    @property
    def main_id(self):
        return self.__main_element.automation_id

    @property
    def main_type(self):
        return self.__main_element.control_type

    @property
    def main_action(self):
        return self.__main_element.action

    @property
    def init_status(self):
        return

    @property
    def parent_info(self):
        return self.__parent

    @property
    def parent_name(self):
        return self.__parent.name if self.__parent else None

    @property
    def parent_id(self):
        return self.__parent.automation_id if self.__parent else None

    @property
    def parent_type(self):
        return self.__parent.control_type if self.__parent else None

    @property
    def child_info(self):
        return self.__child

    @property
    def child_name(self):
        return self.__child.name if self.__child else None

    @property
    def child_id(self):
        return self.__child.automation_id if self.__child else None

    @property
    def child_type(self):
        return ControlType.of_code(self.__main_element.control_type.child) if self.__child else None

    @property
    def child_action(self):
        return self.__child.action if self.__child else None

    @property
    def is_virtual_control(self) -> bool:
        return self.__main_element.control_type.is_virtual

    # @property
    # def name(self)->Optional[str]:
    #     items = self.__name_path.split('/') if self.__name_path else None
    #     name_item = items[0] if items and len(items) > 0 else None
    #     name, _, _ = StringUtils.split_by_keyword(name_item, '{}')
    #     return name
    #
    # @property
    # def automation_id(self)->Optional[str]:
    #     items = self.__id_path.split('/') if self.__id_path else None
    #     id_item = items[0] if items and len(items) > 0 else None
    #     automation_id, _, _ = StringUtils.split_by_keyword(id_item, '{}')
    #
    #     return automation_id

    # @property
    # def init_status(self)->InitStatus:
    #     items = self.__name_path.split('/') if self.__name_path else self.__id_path.split('/') if self.__id_path else None
    #     _item = items[0] if items and len(items) > 0 else None
    #     _, init_status, _ = StringUtils.split_by_keyword(_item, '{}')
    #     return InitStatus.of_code(init_status)

    # @property
    # def child_name(self)->Optional[str]:
    #     items = self.__name_path.split('/') if self.__name_path else self.__id_path.split('/') if self.__id_path else None
    #
    #     child_name = items[1] if items and len(items) == 3 else None
    #     return child_name

    # @property
    # def action(self) -> Optional[ActionType]:
    #     """
    #     操作类型
    #     """
    #     items = self.__name_path.split('/') if self.__name_path else self.__id_path.split(
    #         '/') if self.__id_path else None
    #     item = items[2] if items and len(items) == 3 else None
    #     _, action_name, _ = StringUtils.split_by_keyword(item, '{}')
    #     return ActionType.of_code(action_name) if action_name else ActionType.default_action(self.control_type)
    #
    # @property
    # def menu_item(self) -> Optional[str]:
    #     """
    #     菜单项名
    #     """
    #     items = self.__name_path.split('/') if self.__name_path else self.__id_path.split(
    #         '/') if self.__id_path else None
    #     item = items[2] if items and len(items) == 3 else None
    #     menu_name, _, _ = StringUtils.split_by_keyword(item, '{}')
    #
    #     return menu_name

    # @property
    # def menu_type(self)->Optional[MenuType]:
    #     items = self.__name_path.split('/') if self.__name_path else self.__id_path.split(
    #         '/') if self.__id_path else None
    #     item = items[2] if items and len(items) == 3 else None
    #
    #     if item and '{' in item:
    #         _, type_name, _ = StringUtils.split_by_keyword(item, '{}')
    #         menu_type = MenuType.of_code(type_name) if type_name else None
    #     else:
    #         menu_type = MenuType.CONTEXT if item else None
    #     return menu_type

    # @property
    # def menu_items(self)->List[str]:
    #     return self.__name_path.split('/') if self.__name_path else []

    # @property
    # def need_to_find_parent(self)->bool:
    #     return self.__main_element and self.is_composite and self.__parent

    # def get_offset(self, default_width=0, default_height=0)->Optional[tuple[int, int]]:
    #     if not self.value:
    #         return None
    #
    #     value_map = json.loads(self.value)
    #     offset_x = value_map.get('offset_x', default_width // 2)
    #     offset_y = value_map.get('offset_y', default_height // 2)
    #     return offset_x, offset_y
    #
    # def get_parent_offset(self, default_width=0, default_height=0)->Optional[tuple[int, int]]:
    #     if not self.value:
    #         return None
    #
    #     value_map = json.loads(self.value)
    #     offset_x = value_map.get('offset_X', default_width // 2)
    #     offset_y = value_map.get('offset_Y', default_height // 2)
    #     return offset_x, offset_y

    def __str__(self) -> str:
        attributes = {k: v for k, v in self.__dict__.items() if v is not None}
        return f"ElementInfo({', '.join(f'{k}={v}' for k, v in attributes.items())})"

    def __parse_name_path(self, name_path:Optional[str]) -> None:
        if name_path:
            if name_path.count('/') == 2:
                main_item, child_item, menu_item = tuple(name_path.split('/'))

                self.__main_element.get_from_name_path(main_item)

                if child_item:
                    child_name, child_action, _ = StringUtils.split_by_keyword(child_item, '{}')
                    self.__child = Control(child_name, action=ActionType.of_code(child_action))

                if menu_item:
                    menu_item_name, menu_item_type, _ = StringUtils.split_by_keyword(menu_item, '{}')
                    menu_type = MenuType.of_code(menu_item_type) if menu_item_type else MenuType.CONTEXT
                    self.pop_menu = Control(menu_item_name, menu_type=menu_type)
            elif '/' not in name_path:
                self.__main_element.get_from_name_path(name_path)

    def __parse_id_path(self, id_path:Optional[str]) -> None:
        if id_path:
            if id_path.count('/') == 2:
                main_item, child_item, menu_item = tuple(id_path.split('/'))

                self.__main_element.get_from_id_path(main_item)

                if child_item:
                    child_name, child_action, _ = StringUtils.split_by_keyword(child_item, '{}')
                    self.__child = Control(child_name, action=ActionType.of_code(child_action))

                if menu_item:
                    menu_item_name, menu_item_action, _ = StringUtils.split_by_keyword(menu_item, '{}')
                    self.pop_menu = Control(menu_item_name, action=ActionType.of_code(menu_item_action))
            elif '/' not in id_path:
                self.__main_element.get_from_id_path(id_path)
