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

import os
import sys
from typing import Optional, List

from pixelbox.resource import get_resource

# This has to be set, I think, before importing QApplication
if sys.platform.startswith("linux"):
    os.environ["QT_QPA_PLATFORM"] = "xcb"

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QMenu,
    QFileDialog,
    QMessageBox,
    QTextEdit,
)
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QScreen,
    QCursor,
    QPixmap,
    QGuiApplication,
    QKeyEvent,
    QPaintEvent,
    QContextMenuEvent,
    QMouseEvent,
    QFont,
    QShowEvent,
    QAction,
    QFontMetrics,
)
from PySide6.QtCore import Qt, QRect, QEvent, QPoint


def create_yellow_hand_cursor():
    pixmap = QPixmap(get_resource("yellow_hand_cursor.png"))
    if pixmap.isNull():
        # Failed to load 'yellow_hand_cursor.png'. Using default cursor.
        return QCursor(Qt.CursorShape.PointingHandCursor)
    normal_size = 32
    pixmap = pixmap.scaled(
        normal_size,
        normal_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    # Adjust cursor hotspot. Here we set it to location of index fingertip.
    hotspot_x = 11
    hotspot_y = 0
    return QCursor(pixmap, hotspot_x, hotspot_y)


class OverlayWindow(QWidget):
    def __init__(self, tool_window):
        super().__init__()
        self.tool_window: ToolWindow = tool_window
        self.tool_window_location: int = 1  # in (1,2,3,4)
        # Set up a frameless, transparent window that stays on top.
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Initially, set geometry to the current screen's geometry.
        self.current_screen: QScreen = QGuiApplication.screenAt(QCursor.pos())
        if self.current_screen:
            self.setGeometry(self.current_screen.geometry())
        else:
            self.setGeometry(QApplication.primaryScreen().geometry())
        self.rectangles: list = []
        self.drawing: bool = False
        self.start_point: Optional[QPoint] = None
        self.current_point: Optional[QPoint] = None
        self.displays: List[QScreen] = QScreen.virtualSiblings(self.screen())
        self.display_number: int = 0

        self.setMouseTracking(True)  # For mouseMoveEvents even when no buttons are pressed.
        self.show()

    @staticmethod
    def display_boxes(current_display: int, total_displays: int) -> str:
        return "".join("▣" if i == current_display else "□" for i in range(total_displays))

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.move_to_display(self.display_number)

    def move_tool_window(self, quadrant: int):
        if 1 <= quadrant <= 4:
            display: QRect = self.displays[self.display_number].availableGeometry()
            if quadrant == 1:
                self.tool_window.move(display.left(), display.top())
            elif quadrant == 2:
                self.tool_window.move(display.right() - self.tool_window.width(), display.top())
            elif quadrant == 3:
                self.tool_window.move(display.left(), display.bottom())
            elif quadrant == 4:
                self.tool_window.move(display.right() - self.tool_window.width(), display.bottom())

    def move_to_display(self, delta: int):
        new_display_number: int = self.display_number + delta
        if 0 <= new_display_number < len(self.displays):
            self.display_number = new_display_number
            display: QRect = self.displays[new_display_number].availableGeometry()
            self.move_tool_window(self.tool_window_location)
            self.move(display.left(), display.top())
            self.raise_()
            self.clear_all_boxes()
            if not self.isFullScreen():
                self.showFullScreen()
            self.tool_window.edit.setHtml(
                f"""
                <p style='text-align: center;'>
                  <h3>PixelBox Ruler v1.0<br>{self.display_boxes(self.display_number, len(self.displays))}</h3>
                  <h4>
                  Display: {self.display_number + 1}/{len(self.displays)}<br>
                  Change Display: 🠊, 🠈<br>
                  Move This Window: 1, 2, 3, 4
                  </h4>
                </p>
                """
            )
        else:
            print(f"Cannot move to monitor number {new_display_number}")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        # Start drawing immediately on left-button press.
        point: QPoint = event.position().toPoint()
        self.start_point = point
        self.current_point = point
        self.drawing = True
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            # Update the current endpoint as the mouse moves.
            self.current_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if self.drawing:
            # Finalize the rectangle when the left mouse button is released.
            self.current_point = event.position().toPoint()
            rect: QRect = QRect(self.start_point, self.current_point).normalized()
            if rect.width() > 0 and rect.height() > 0:
                self.rectangles.append(rect)
            self.drawing = False
            self.start_point = None
            self.current_point = None
            self.update()

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu: QMenu = QMenu(self)
        save_action: QAction = menu.addAction("Save To Image")
        clear_last_action: QAction = menu.addAction("Clear Last Box")
        clear_all_action: QAction = menu.addAction("Clear All Boxes")
        quit_action: QAction = menu.addAction("Quit")
        action: QAction = menu.exec(event.globalPos())
        if action == save_action:
            self.save_to_image()
        elif action == clear_last_action:
            self.clear_last_box()
        elif action == clear_all_action:
            self.clear_all_boxes()
        elif action == quit_action:
            QApplication.quit()

    def save_to_image(self):
        # Open a file dialog defaulting to 'selected_regions.png'
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Overlay Image", "selected_regions.png", "PNG Files (*.png)"
        )
        if file_name:
            pixmap = self.grab()
            if not pixmap.save(file_name, "PNG"):
                QMessageBox.critical(self, "Save Error", "Failed to save the image!")

    def clear_all_boxes(self):
        self.rectangles.clear()
        self.update()

    def clear_last_box(self):
        if self.rectangles:
            self.rectangles.pop()
            self.update()

    def enterEvent(self, event: QEvent):
        # Set our custom yellow hand cursor when the mouse enters the overlay.
        self.setCursor(create_yellow_hand_cursor())

    def leaveEvent(self, event: QEvent):
        # Revert to the default cursor when the mouse leaves the overlay.
        self.unsetCursor()

    def draw_dimension_text(self, painter: QPainter, rect: QRect, text: str):
        """Draws text just above the top-left corner of the rectangle with a correctly positioned yellow background."""

        # Get text size using QFontMetrics
        font_metrics = QFontMetrics(painter.font())
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()

        # Calculate text position (above top-left of rect)
        text_x = rect.left()
        text_y = rect.top() - text_height - 2  # Move text above the rectangle with some padding

        # Ensure background box aligns correctly behind text
        background_rect = QRect(text_x - 3, text_y, text_width + 6, text_height + 2)  # Add padding

        # Draw the yellow background
        painter.setBrush(QColor("yellow"))
        painter.setPen(Qt.PenStyle.NoPen)  # No border for background
        painter.drawRect(background_rect)

        # Draw the black text on top
        painter.setPen(QColor("black"))
        painter.drawText(text_x, text_y + font_metrics.ascent(), text)

        painter.setBrush(Qt.BrushStyle.NoBrush)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        # First, draw a solid black rectangle for visibility
        black_pen = QPen(QColor("black"), 2)
        black_pen.setStyle(Qt.PenStyle.SolidLine)

        # Then, draw a dashed yellow rectangle on top
        yellow_pen = QPen(QColor("yellow"), 2)
        yellow_pen.setStyle(Qt.PenStyle.DashLine)

        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw finalized rectangles
        for rect in self.rectangles:
            # Draw black solid outline first
            painter.setPen(black_pen)
            painter.drawRect(rect)

            # Draw yellow dashed outline on top
            painter.setPen(yellow_pen)
            painter.drawRect(rect)

            text = f"{rect.width()} x {rect.height()}"
            self.draw_dimension_text(painter, rect, text)

        # Draw current rectangle if in progress
        if self.drawing and self.start_point and self.current_point:
            rect = QRect(self.start_point, self.current_point).normalized()

            # Draw black solid outline first
            painter.setPen(black_pen)
            painter.drawRect(rect)

            # Draw yellow dashed outline on top
            painter.setPen(yellow_pen)
            painter.drawRect(rect)

            text = f"{rect.width()} x {rect.height()}"
            self.draw_dimension_text(painter, rect, text)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in {Qt.Key.Key_1, Qt.KeyboardModifier.KeypadModifier | Qt.Key_1}:
            self.move_tool_window(1)
        elif event.key() in {Qt.Key.Key_2, Qt.KeyboardModifier.KeypadModifier | Qt.Key_2}:
            self.move_tool_window(2)
        elif event.key() in {Qt.Key.Key_3, Qt.KeyboardModifier.KeypadModifier | Qt.Key_3}:
            self.move_tool_window(3)
        elif event.key() in {Qt.Key.Key_4, Qt.KeyboardModifier.KeypadModifier | Qt.Key_4}:
            self.move_tool_window(4)
        elif event.key() == Qt.Key.Key_Left:
            self.move_to_display(-1)
        elif event.key() == Qt.Key.Key_Right:
            self.move_to_display(1)
        else:
            super().keyPressEvent(event)


class ToolWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Frameless tool panel with no title bar or close buttons.
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: yellow;")
        self.edit = QTextEdit()
        self.edit.setHtml("<p style='text-align: center;'><h3>PixelBox Ruler v1.0</h3></p>")
        self.edit.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.setLayout(layout)
        self.setFixedSize(450, 190)
        self.overlay_window = OverlayWindow(self)
        QApplication.instance().installEventFilter(self)
        self.show()

    def contextMenuEvent(self, event):
        menu: QMenu = QMenu(self)
        quit_action: QAction = menu.addAction("Quit")
        action: QAction = menu.exec(event.globalPos())
        if action == quit_action:
            QApplication.quit()

    def closeEvent(self, event):
        self.overlay_window.close()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    # print(QGuiApplication.platformName())  # Should print 'wayland' or 'xcb'

    QApplication.instance().setFont(QFont("Sans-serif", 14))

    _ = ToolWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
