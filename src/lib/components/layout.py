"""This is a module that defines app layout.
"""  # noqa: INP001

import enum
import re
from collections.abc import Callable
from logging import getLogger

import flet as ft

from lib.common.types import ParamKey as K
from lib.common.types import ParamLog

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


def check_comma_separated_num(value: str) -> tuple[list[int], bool]:
    """Check comma separated numbers.

    Args:
        value (str): comma separated numbers.

    Returns:
        list[int]: list of numbers.
        bool: check result for comma separated numbers.
    """
    valid_pattern: re.Pattern = re.compile(r'^\d+(?:[,|-]\d+)*$')
    valid = bool(re.match(valid_pattern, value))
    LOGGER.debug(f'{value=}')
    LOGGER.debug(f'{re.match(valid_pattern, value)=}')

    num_pages = []
    if valid:
        pages = value.split(',')
        for num in pages:
            try:
                num_pages.append(int(num))
            except ValueError:
                try:
                    nums = [int(n) for n in num.split('-')]
                    num_min = min(nums)
                    num_max = max(nums)
                    if num_min == num_max:
                        num_pages.append(num_min)
                    else:
                        num_pages.extend(range(num_min, num_max + 1))
                except ValueError:
                    valid = False

    LOGGER.debug(f'{num_pages=}')
    return num_pages, valid


class LogType(enum.IntEnum):
    """Defines :class:`App` log type.
    """
    CLEAR = enum.auto()
    NOT_CLEAR = enum.auto()


class EventName(enum.StrEnum):
    """Defines event name for the following items.

    *   ``ft.FilePickerResultEvent``
    *   ``ft.ControlEvent``
    """
    FILE_PICKER = 'result'
    BUTTON = 'click'


class TextElButton(enum.StrEnum):
    """Defines ``ft.ElevatedButton`` text value.
    """
    SELECT = 'Select'
    DELETE = 'Delete'
    MERGE = 'Merge'
    SPLIT = 'Split'
    EXTRACT = 'Extract'


class IconElButton(enum.StrEnum):
    """Defines ``ft.ElevatedButton`` icon value.
    """
    SELECT = ft.Icons.FILE_OPEN
    DELETE = ft.Icons.DELETE
    MERGE = ft.Icons.FILE_UPLOAD
    SPLIT = ft.Icons.FILE_UPLOAD
    EXTRACT = ft.Icons.FILE_UPLOAD


class ProcElButton(ft.ElevatedButton):
    """Sets the common settings for ``ft.ElevatedButton`` of the following items:

    *   :class:`SelectElButton`
    *   :class:`DeleteElButton`
    *   :class:`MergeElButton`
    *   :class:`SplitElButton`
    *   :class:`ExtractElButton`

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__()

        self.on_click = on_click
        self.col = {'sm': 6, 'md': 4, 'xxl': 1}


class SelectElButton(ProcElButton):
    """Sets :class:`ProcElButton` to select files.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__(on_click=on_click)

        self.text = TextElButton.SELECT
        self.icon = IconElButton.SELECT


class DeleteElButton(ProcElButton):
    """Sets :class:`ProcElButton` to delete all files.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__(on_click=on_click)

        self.text = TextElButton.DELETE
        self.icon = IconElButton.DELETE


class MergeElButton(ProcElButton):
    """Sets :class:`ProcElButton` to merge files.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__(on_click=on_click)

        self.text = TextElButton.MERGE
        self.icon = IconElButton.MERGE


class SplitElButton(ProcElButton):
    """Sets :class:`ProcElButton` to split the page from files.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__(on_click=on_click)

        self.text = TextElButton.SPLIT
        self.icon = IconElButton.SPLIT


class ExtractElButton(ProcElButton):
    """Sets :class:`ProcElButton` to extract the page from files.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__(on_click=on_click)

        self.text = TextElButton.EXTRACT
        self.icon = IconElButton.EXTRACT


class PageTopAppBar(ft.AppBar):
    """Sets ``ft.AppBar`` at the top of the page.

    Args:
        title (ft.Text): title value.
    """
    def __init__(self, title: ft.Text) -> None:
        super().__init__()

        self.title = title
        self.bgcolor = ft.Colors.BLUE_ACCENT
        self.color = ft.Colors.WHITE
        self.leading = ft.Icon(name=ft.Icons.DATASET)


class ExtractPageTextField(ft.TextField):
    """Sets ``ft.TextField`` to input the page to be extracted.
    """
    def __init__(self) -> None:
        super().__init__()

        self.label = 'Number of Pages to Extract'
        self.hint_text = 'Separated by commas, e.g. 1,2,5-10,20,30.'
        self.col = {'sm': 6, 'md': 4, 'xxl': 3}
        self.on_blur = self.on_check_extract_num

        self.valid = True
        self.num_pages: list[int] = []

    def on_check_extract_num(self, e: ft.ControlEvent) -> None:
        """Check comma separated numbers to be extracted.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        bgcolor = ft.Colors.WHITE
        self.num_pages, self.valid = check_comma_separated_num(value=self.value)
        if not self.valid:
            bgcolor = ft.Colors.RED
        self.bgcolor = bgcolor
        self.update()


class DispContainer(ft.Container):
    """Sets ``ft.Container`` to display ``ft.ListView``.
    """
    def __init__(self) -> None:
        super().__init__()

        self.padding = 10
        self.expand = True
        self.height = 200
        self.bgcolor = ft.Colors.WHITE
        self.border = ft.border.all(1, ft.Colors.BLACK)
        self.border_radius = 5
        self.content = ft.ListView(
            spacing=0,
            auto_scroll=True,
            expand=True,
        )


class MainLayout(ft.Column):
    """Sets ``ft.Column`` to define the main layout.

    Args:
        on_click (Callable): function for `on_click`.
    """
    def __init__(self, on_click: Callable) -> None:
        super().__init__()

        self.tf_extract_num = ExtractPageTextField()
        self.c_disp_fpath = DispContainer()
        self.c_disp_log = DispContainer()

        self.expand = True
        self.controls = [
            ft.ResponsiveRow(
                spacing=20,
                controls=[
                    SelectElButton(on_click=on_click),
                    DeleteElButton(on_click=on_click),
                    MergeElButton(on_click=on_click),
                    SplitElButton(on_click=on_click),
                    ExtractElButton(on_click=on_click),
                    self.tf_extract_num,
                ],
            ),
            ft.Text(
                value='File Path List:',
                color=ft.Colors.BLACK,
                size=20,
            ),
            self.c_disp_fpath,
            ft.Text(
                value='Log:',
                color=ft.Colors.BLACK,
                size=20,
            ),
            self.c_disp_log,
        ]


class DelButtonText(ft.Draggable):
    """Sets ``ft.Draggable`` to display the Delete button and Text.

    *   When you press the Delete button displayed in this class, the class will be
        deleted from its parent control.
    *   If a parent control has multiple instances of this class, they can be reordered
        using drag and drop.

    Args:
        page (ft.Page): flet page.
        parent_control (ft.Column): parent control of this class.
        value (str): display value (``ft.Text``).
    """
    def __init__(self, page: ft.Page, parent_control: ft.Column, value: str) -> None:
        self.page = page
        self.parent_control = parent_control

        group = 'fpath'
        content = ft.DragTarget(
            group=group,
            on_accept=self.on_accept,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=self.on_delete,
                    ),
                    ft.Text(
                        value=value,
                        color=ft.Colors.BLACK,
                        size=15,
                    ),
                ],
            ),
        )
        super().__init__(content=content, group=group)

    def on_delete(self, e: ft.ControlEvent) -> None:
        """Removes an instance of this class from its parent control.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        LOGGER.debug(f'{e.control=}')
        self.parent_control.controls.remove(self)
        self.parent_control.update()

    def on_accept(self, e: ft.DragTargetEvent) -> None:
        """Reorder instances of this class in the parent control using drag and drop.

        Args:
            e (ft.DragTargetAcceptEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        target = self.page.get_control(e.target)
        drop_item = target.parent
        drag_item = self.page.get_control(e.src_id)
        drop_item_idx = self.parent_control.controls.index(drop_item)
        drag_item_idx = self.parent_control.controls.index(drag_item)
        self.parent_control.controls.insert(drop_item_idx, drag_item)
        self.parent_control.controls.pop(drop_item_idx + 1)
        self.parent_control.controls.insert(drag_item_idx, drop_item)
        self.parent_control.controls.pop(drag_item_idx + 1)
        self.parent_control.update()
