"""
PixelBox
Copyright (C) 2025 Travis L. Seymour, PhD

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import qdarkstyle
from PySide6.QtCore import QSize
from PySide6.QtGui import QPalette, QColor, QGuiApplication
from typing import Literal
from qtpy.QtGui import QFont


def set_light_style(app_instance):
    app_instance.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(233, 231, 227))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    app_instance.setPalette(palette)
    # Clear any style sheet that might conflict.
    app_instance.setStyleSheet("")


def set_dark_style(app_instance):
    app_instance.setStyleSheet(qdarkstyle.load_stylesheet())


def get_default_font(family: Literal["sans-serif", "serif", "monospace"] = "monospace", size: int = 14) -> QFont:
    """Returns a cross-platform QFont object with fallbacks."""
    font_families = {
        "sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Sans-serif"],
        "serif": ["Times New Roman", "Times", "Liberation Serif", "Serif"],
        "monospace": ["Courier New", "Courier", "DejaVu Sans Mono", "Monospace"],
    }

    font = QFont()
    for fam in font_families[family]:  # family is guaranteed to be a valid key
        font.setFamily(fam)
        if QFont(fam).exactMatch():  # Ensures the font exists on the system
            break

    font.setPointSize(size)
    return font


def size_fits(desired_size: QSize) -> bool:
    """Return True if desired_size fits within the available desktop area, otherwise False."""
    screen = QGuiApplication.primaryScreen()
    if not screen:
        return False  # if no screen available, return False
    available = screen.availableGeometry()
    return desired_size.width() <= available.width() and desired_size.height() <= available.height()


def get_app_size(kind: str) -> QSize:
    """
    https://www.browserstack.com/guide/common-screen-resolutions
    """
    x, y = 0, 0
    if kind == "main_window":
        ...
    elif kind == "view_window":
        ...
    else:
        raise ValueError('In get_app_size, kind should be "main_window" or "view_window".')

    return QSize(x, y)
