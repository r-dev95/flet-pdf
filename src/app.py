"""This is a module that merges, splits and extracts pages from PDF files.
"""  # noqa: INP001

import argparse
from logging import getLogger
from pathlib import Path
from typing import Any

import flet as ft
import pypdf

from lib.common.file import load_yaml
from lib.common.log import SetLogging
from lib.common.types import ParamKey as K
from lib.common.types import ParamLog
from lib.components.layout import (
    DelButtonText,
    EventName,
    LogType,
    MainLayout,
    PageTopAppBar,
    TextElButton,
)

PARAM_LOG = ParamLog()
LOGGER = getLogger(PARAM_LOG.NAME)


class App:
    """Defines the app process.

    Args:
        page (ft.Page): flet page.
    """

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.on_click_func = {
            TextElButton.SELECT: self.on_select_file,
            TextElButton.DELETE: self.on_delete_file,
            TextElButton.MERGE: self.on_merge_file,
            TextElButton.SPLIT: self.on_split_or_extract_file,
            TextElButton.EXTRACT: self.on_split_or_extract_file,
        }

        page.title = 'PDF App'
        page.adaptive = True
        page.scroll = ft.ScrollMode.AUTO
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.PRIMARY)
        page.appbar = PageTopAppBar(title=ft.Text(value=self.page.title))

        self.file_picker = ft.FilePicker(on_result=self.on_disp_fpath)
        page.overlay.append(self.file_picker)

        layout = MainLayout(on_click=self.on_click_assign)
        page.add(layout)

        self.tf_extract_num = layout.tf_extract_num
        self.c_disp_fpath = layout.c_disp_fpath
        self.c_disp_log = layout.c_disp_log

    def disp_log(self, msgs: list[str], log_type: LogType = LogType.NOT_CLEAR) -> None:
        """Display the processing log.

        Args:
            msgs (list[str]): log massages.
            log_type (LogType): log type.
        """
        match log_type:
            case LogType.CLEAR:
                self.c_disp_log.content.controls = []

        for msg in msgs:
            self.c_disp_log.content.controls.append(ft.Text(value=msg))
        self.c_disp_log.update()

    def get_fpaths(self) -> list[str]:
        """Gets the file paths.

        Returns:
            list[str]: list of file paths.
        """
        # self.c_disp_fpath.content         : ft.Column
        # self.c_disp_fpath.content.controls: list[DelButtonText]
        # c                                 : DelButtonText
        # c.content                         : ft.DragTarget
        # c.content.content                 : ft.Row
        # c.content.content.controls        : list[ft.IconButton, ft.Text]
        controls = self.c_disp_fpath.content.controls
        fpaths = [c.content.content.controls[1].value for c in controls]
        LOGGER.debug(f'{fpaths=}')
        return fpaths

    def on_disp_fpath(self, e: ft.FilePickerResultEvent) -> None:
        """Display the file paths.

        Args:
            e (ft.FilePickerResultEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        LOGGER.debug(f'{e.files=}')
        if e.files:
            fpaths = []
            for fpath in e.files:
                if fpath.path:
                    fpaths.append(fpath.path)
                else:
                    fpaths.append(fpath.name)
            for fpath in fpaths:
                controls = DelButtonText(
                    page=self.page,
                    parent_control=self.c_disp_fpath.content,
                    value=fpath,
                )
                self.c_disp_fpath.content.controls.append(controls)
            self.c_disp_fpath.content.update()

    def on_select_file(self, e: ft.ControlEvent) -> None:
        """Selects the files.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        self.file_picker.pick_files(allow_multiple=True, allowed_extensions=['pdf'])

    def on_merge_file(self, e: ft.ControlEvent) -> None:
        """Merge the files.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        fpaths = self.get_fpaths()
        if not fpaths:
            return

        # e.control: ft.ElevatedButton
        control_kind = e.control.text
        msgs = [f'{control_kind} progressing...']
        self.disp_log(msgs=msgs, log_type=LogType.CLEAR)

        print(f'{fpaths[0]=}')
        wfpath = Path(fpaths[0])
        wfpath = Path(wfpath.parent, wfpath.stem, wfpath.stem + f'_{control_kind}.pdf')
        wfpath.parent.mkdir(parents=True, exist_ok=True)
        writer = pypdf.PdfWriter()
        for fpath in fpaths:
            writer.append(fpath)
        writer.write(wfpath)
        writer.close()

        msgs = ['Done!']
        self.disp_log(msgs=msgs)

    def on_split_or_extract_file(self, e: ft.ControlEvent) -> None:
        """Split or Extract the page from files.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        fpaths = self.get_fpaths()
        if not fpaths:
            return

        # e.control: ft.ElevatedButton
        control_kind = e.control.text
        if control_kind == TextElButton.EXTRACT:
            self.tf_extract_num.on_check_extract_num(e=None)
            num_pages = self.tf_extract_num.num_pages
            if not self.tf_extract_num.valid:
                return

        msgs = [f'{control_kind} progressing...']
        self.disp_log(msgs=msgs, log_type=LogType.CLEAR)

        for fpath in fpaths:
            reader = pypdf.PdfReader(fpath)
            if control_kind == TextElButton.SPLIT:
                num_pages = list(range(len(reader.pages) + 1))
            for i in range(len(reader.pages)):
                wfpath = Path(fpath)
                wfpath = Path(
                    wfpath.parent,
                    wfpath.stem,
                    wfpath.stem + f'_{i + 1:05}.pdf',
                )
                if i + 1 in num_pages:
                    wfpath.parent.mkdir(parents=True, exist_ok=True)
                    n_page = reader.pages[i]
                    writer = pypdf.PdfWriter()
                    writer.add_page(n_page)
                    writer.write(wfpath)
                    writer.close()
                    msgs = [f'+ {wfpath}']
                    self.disp_log(msgs=msgs)
            reader.close()

        msgs = ['Done!']
        self.disp_log(msgs=msgs)

    def on_delete_file(self, e: ft.ControlEvent) -> None:
        """Deletes the all files.

        Args:
            e (ft.ControlEvent): event class.
        """
        LOGGER.debug(f'{e=}')
        LOGGER.debug(f'{e.control.text=}')
        if self.c_disp_fpath.content.controls:
            self.c_disp_fpath.content.controls = []
            self.c_disp_fpath.update()

    def on_click_assign(self, e: ft.FilePickerResultEvent | ft.ControlEvent) -> None:
        """Assigns the process function.

        Args:
            e (ft.FilePickerResultEvent | ft.ControlEvent): event class.
        """
        if e.name == EventName.FILE_PICKER:
            self.on_disp_fpath(e=e)
        elif e.name == EventName.BUTTON:
            # e.control: ft.ElevatedButton
            self.on_click_func[e.control.text](e=e)
        else:
            LOGGER.info(f'{e.name} is not exist.')
            raise ValueError


def main(page: ft.Page) -> None:
    """Main.

    Args:
        page (ft.Page): flet page.
    """
    App(page=page)


def set_params() -> dict[str, Any]:
    """Sets the command line arguments and file parameters.

    *   Set only common parameters as command line arguments.
    *   Other necessary parameters are set in the file parameters.
    *   Use a yaml file. (:func:`lib.common.file.load_yaml`)

    Returns:
        dict[str, Any]: parameters.

    .. attention::

        Command line arguments are overridden by file parameters.
        This means that if you want to set everything using file parameters,
        you don't necessarily need to use command line arguments.
    """
    # set the command line arguments.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        f'--{K.HANDLER}',
        default=[True, True], type=bool, nargs=2,
        help=(
            f'The log handler flag to use.\n'
            f'True: set handler, False: not set handler\n'
            f'ex) --{K.HANDLER} arg1 arg2 (arg1: stream handler, arg2: file handler)'
        ),
    )
    parser.add_argument(
        f'--{K.LEVEL}',
        default=[20, 20], type=int, nargs=2, choices=[10, 20, 30, 40, 50],
        help=(
            f'The log level.\n'
            f'DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50\n'
            f'ex) --{K.LEVEL} arg1 arg2 (arg1: stream handler, arg2: file handler)'
        ),
    )
    parser.add_argument(
        f'--{K.PARAM}',
        default='param/param.yaml', type=str,
        help=('The parameter file path.'),
    )
    parser.add_argument(
        f'--{K.RESULT}',
        default='result', type=str,
        help=('The directory path to save the results.'),
    )

    params = vars(parser.parse_args())

    # set the file parameters.
    if params.get(K.PARAM):
        fpath = Path(params[K.PARAM])
        if fpath.is_file():
            params.update(load_yaml(fpath=fpath))

    return params


if __name__ == '__main__':
    # set the parameters.
    params = set_params()
    # set the logging configuration.
    PARAM_LOG.HANDLER[PARAM_LOG.SH] = params[K.HANDLER][0]
    PARAM_LOG.HANDLER[PARAM_LOG.FH] = params[K.HANDLER][1]
    PARAM_LOG.LEVEL[PARAM_LOG.SH] = params[K.LEVEL][0]
    PARAM_LOG.LEVEL[PARAM_LOG.FH] = params[K.LEVEL][1]
    SetLogging(logger=LOGGER, param=PARAM_LOG)

    if params.get(K.RESULT):
        Path(params[K.RESULT]).mkdir(parents=True, exist_ok=True)

    ft.app(target=main)
