import signal
from abc import ABC, abstractmethod
from functools import partial
from pathlib import Path
from typing import TypeVar, Any, Generic, Callable, Optional

import wx
from duit.event.Event import Event

from visiongui.utils.KeyStrokeDetector import KeyStrokeDetector
from visiongui.widgets.menu.BaseApplicationMenuBar import Menu, TextMenuItem, BaseApplicationMenuBar, SeparatorMenuItem, \
    ButtonMenuItem
from visiongui.widgets.menu.WxApplicationMenuBar import WxApplicationMenuBar

T = TypeVar("T", bound=Any)


class BaseUserInterface(Generic[T], ABC):

    def __init__(self, config: T, title: str, width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False):
        self.config = config
        self.title = title

        # setup ui and menu
        self.frame = wx.Frame(None, title=title, size=(width, height))

        # settings events
        self.settings_file: Optional[Path] = None
        self.on_open_settings: Event[Path] = Event()
        self.on_save_settings: Event[Path] = Event()

        self.menu_bar: BaseApplicationMenuBar = WxApplicationMenuBar(title, self.frame)
        self.app_menu = Menu(title, items=[
            ButtonMenuItem("About", "Show about dialog", on_action=self._on_menu_about),
            SeparatorMenuItem(),
            ButtonMenuItem("Quit", "Quit the application", on_action=lambda _: self.frame.Close(True)),
        ], is_app_menu=True)

        self.settings_menu = Menu("Settings", items=[
            ButtonMenuItem("Open", "Open Settings", on_action=self._on_menu_open),
            SeparatorMenuItem(),
            ButtonMenuItem("Save", "Save Settings", on_action=self._on_menu_save),
            ButtonMenuItem("Save As...", "Save Settings as new File", on_action=self._on_menu_save_as),
        ])

        self.menu_bar.add_menu(self.app_menu)
        self.menu_bar.add_menu(self.settings_menu)

        # setup ui hooks
        self.frame.Bind(wx.EVT_CLOSE, self._on_window_close_event)

        # setup panel
        self.panel = wx.Panel(self.frame, wx.ID_ANY)

        # setup hot keys
        self.key_detector = KeyStrokeDetector()
        # self._setup_hotkeys(self.key_detector)

        # add key bindings
        self.panel.Bind(wx.EVT_KEY_DOWN, self.key_detector.on_key_down)
        self.panel.Bind(wx.EVT_KEY_UP, self.key_detector.on_key_up)

        # attach signal handler
        if attach_interrupt_handler:
            signal.signal(signal.SIGINT, self._signal_handler)

    def display(self):
        self.menu_bar.attach()

        main_sizer = self._create_ui_layout()

        # Set the sizer for the main panel
        self.panel.SetSizer(main_sizer)
        self.panel.Centre()

        self.frame.Show(True)
        self.panel.SetFocus()

    @abstractmethod
    def _create_ui_layout(self) -> wx.Sizer:
        pass

    def _on_window_close_event(self, event):
        self._on_close()
        event.Skip()

    def _on_close(self):
        pass

    def _signal_handler(self, signal_type: signal, frame: Any):
        self._on_close()

    def _setup_hotkeys(self, key_detector: KeyStrokeDetector):
        self.window.set_on_key(key_detector.on_key_pressed)

        meta_key = key_detector.meta_key
        key_detector.register(partial(self.invoke_on_gui, self.menu._on_menu_open), meta_key, gui.KeyName.O)
        key_detector.register(partial(self.invoke_on_gui, self.menu._on_menu_save), meta_key, gui.KeyName.S)
        key_detector.register(partial(self.invoke_on_gui, self.window.close), meta_key, gui.KeyName.Q)

    @staticmethod
    def invoke_on_gui(callback: Callable[[], None]):
        wx.CallAfter(callback)

    def _on_menu_about(self, sender: TextMenuItem):
        _ = wx.MessageBox(self.about_text, "About")

    def _on_menu_open(self, event):
        with wx.FileDialog(
                self.frame, "Open Settings", wildcard="JSON files (*.json)|*.json",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            path = dialog.GetPath()
            self.settings_file = Path(path)
            self.on_open_settings(self.settings_file)

    def _on_menu_save(self, event):
        if self.settings_file is None:
            self._on_menu_save_as(event)
            return

        self.on_save_settings(self.settings_file)

    def _on_menu_save_as(self, event):
        with wx.FileDialog(
                self.frame, "Save Settings", wildcard="JSON files (*.json)|*.json",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return  # User cancelled the dialog

            path = dialog.GetPath()
            self.settings_file = Path(path)
            self.on_save_settings(self.settings_file)

    @property
    def about_text(self):
        return f"Hello from {self.title}"
