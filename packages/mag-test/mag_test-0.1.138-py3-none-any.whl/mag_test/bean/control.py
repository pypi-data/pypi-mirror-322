from typing import Optional

from mag_tools.utils.common.string_utils import StringUtils

from mag_test.model.action_type import ActionType
from mag_test.model.control_type import ControlType
from mag_test.model.menu_type import MenuType
from mag_test.model.init_status import InitStatus


class Control:
    def __init__(self, name: Optional[str] = None, control_type: Optional[ControlType] = None, automation_id: Optional[str] = None,
                 action: Optional[ActionType] = None, class_name: Optional[str] = None,
                 menu_type: Optional[MenuType] = None, init_status: Optional[InitStatus] = None):
        self.name = name
        self.control_type = control_type
        self.automation_id = automation_id
        self.action = action
        self.menu_type = menu_type
        self.class_name = class_name
        self.init_status = init_status

    def get_from_name_path(self, name_path: str):
        if name_path:
            self.name, action_name, _ = StringUtils.split_by_keyword(name_path, '{}')
            if self.control_type in {ControlType.TREE, ControlType.TABLE}:
                self.init_status = InitStatus.of_code(action_name)
            else:
                self.action = ActionType.of_code(action_name) if action_name else ActionType.default_action(self.control_type)

    def get_from_id_path(self, id_path: str):
        if id_path:
            self.automation_id, action_name, _ = StringUtils.split_by_keyword(id_path, '{}')
            if self.control_type in {ControlType.TREE, ControlType.TABLE}:
                self.init_status = InitStatus.of_code(action_name)
            else:
                self.action = ActionType.of_code(action_name) if action_name else ActionType.default_action(self.control_type)

    @property
    def is_composite(self):
        return self.control_type.is_composite

    def __str__(self) -> str:
        attributes = {k: v for k, v in self.__dict__.items() if v is not None}
        return f"Control({', '.join(f'{k}={v}' for k, v in attributes.items())})"