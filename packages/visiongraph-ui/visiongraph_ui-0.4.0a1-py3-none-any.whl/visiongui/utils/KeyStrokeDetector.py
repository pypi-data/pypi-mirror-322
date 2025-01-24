from dataclasses import dataclass
from typing import Set, Callable, List, Union

import wx
from open3d.cpu.pybind.visualization import gui
from visiongraph.util import OSUtils


@dataclass
class KeyHandler:
    keys: Set[int]
    callback: Callable[[], None]


class KeyStrokeDetector:

    def __init__(self):
        self._pressed_keys: Set[int] = set()

        self.key_handlers: List[KeyHandler] = []

    def register(self, callback: Callable[[], None], *keys: Union[int, gui.KeyName]):
        int_keys = [int(k) for k in keys]
        self.key_handlers.append(KeyHandler(set(int_keys), callback))

    def on_key_down(self, event: wx.KeyEvent) -> bool:
        key_handled = False
        self._pressed_keys.add(event.GetKeyCode())

        for handler in self.key_handlers:
            if handler.keys.issubset(self._pressed_keys):
                key_handled = True
                handler.callback()

        return key_handled

    def on_key_up(self, event: wx.KeyEvent):
        key_code = event.GetKeyCode()
        if key_code in self._pressed_keys:
            self._pressed_keys.remove(key_code)

    @property
    def meta_key(self) -> gui.KeyName:
        meta_key = gui.KeyName.LEFT_CONTROL
        if OSUtils.isMacOSX():
            meta_key = gui.KeyName.META

        return meta_key
