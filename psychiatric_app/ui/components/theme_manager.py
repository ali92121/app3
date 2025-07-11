"""
Theme Manager for the Psychiatric Records System.
Provides comprehensive dark/light theme management with Material Design styling.
"""

from typing import Dict, Any, Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette, QColor

class ThemeManager(QObject):
    """
    Manages application themes with Material Design principles.
    Supports dark and light themes with consistent color schemes.
    """
    
    theme_changed = pyqtSignal(str)  # Signal emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.themes = self._initialize_themes()
    
    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize theme configurations with Material Design colors."""
        return {
            "dark": {
                "name": "Dark Theme",
                "colors": {
                    "primary": "#2196F3",
                    "primary_variant": "#1976D2", 
                    "secondary": "#FF9800",
                    "secondary_variant": "#F57C00",
                    "background": "#121212",
                    "surface": "#1E1E1E",
                    "surface_variant": "#2C2C2C",
                    "error": "#F44336",
                    "warning": "#FF9800",
                    "success": "#4CAF50",
                    "info": "#2196F3",
                    "on_primary": "#FFFFFF",
                    "on_secondary": "#000000",
                    "on_background": "#FFFFFF",
                    "on_surface": "#FFFFFF",
                    "on_error": "#FFFFFF",
                    "text_primary": "#FFFFFF",
                    "text_secondary": "#B0BEC5",
                    "text_disabled": "#546E7A",
                    "divider": "#37474F",
                    "border": "#455A64",
                    "hover": "#263238",
                    "selected": "#1565C0",
                    "pressed": "#0D47A1"
                },
                "stylesheet": self._get_dark_stylesheet()
            },
            "light": {
                "name": "Light Theme",
                "colors": {
                    "primary": "#1976D2",
                    "primary_variant": "#1565C0",
                    "secondary": "#F57C00", 
                    "secondary_variant": "#EF6C00",
                    "background": "#FAFAFA",
                    "surface": "#FFFFFF",
                    "surface_variant": "#F5F5F5",
                    "error": "#D32F2F",
                    "warning": "#F57C00",
                    "success": "#388E3C",
                    "info": "#1976D2",
                    "on_primary": "#FFFFFF",
                    "on_secondary": "#FFFFFF",
                    "on_background": "#212121",
                    "on_surface": "#212121",
                    "on_error": "#FFFFFF",
                    "text_primary": "#212121",
                    "text_secondary": "#757575",
                    "text_disabled": "#BDBDBD",
                    "divider": "#E0E0E0",
                    "border": "#E0E0E0",
                    "hover": "#F5F5F5",
                    "selected": "#E3F2FD",
                    "pressed": "#BBDEFB"
                },
                "stylesheet": self._get_light_stylesheet()
            }
        }
    
    def _get_dark_stylesheet(self) -> str:
        """Get comprehensive dark theme stylesheet."""
        return """
        /* Main Window and Base Styling */
        QMainWindow {
            background-color: #121212;
            color: #FFFFFF;
        }
        
        QWidget {
            background-color: #121212;
            color: #FFFFFF;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 9pt;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #2196F3;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-width: 120px;
            min-height: 36px;
        }
        
        QPushButton:hover {
            background-color: #1976D2;
        }
        
        QPushButton:pressed {
            background-color: #1565C0;
        }
        
        QPushButton:disabled {
            background-color: #546E7A;
            color: #B0BEC5;
        }
        
        QPushButton[buttonType="secondary"] {
            background-color: transparent;
            color: #2196F3;
            border: 2px solid #2196F3;
        }
        
        QPushButton[buttonType="secondary"]:hover {
            background-color: #1565C0;
            color: #FFFFFF;
        }
        
        QPushButton[buttonType="danger"] {
            background-color: #F44336;
        }
        
        QPushButton[buttonType="danger"]:hover {
            background-color: #D32F2F;
        }
        
        /* Text Inputs */
        QLineEdit {
            background-color: #1E1E1E;
            border: 2px solid #455A64;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #FFFFFF;
            min-height: 20px;
        }
        
        QLineEdit:focus {
            border-color: #2196F3;
            background-color: #2C2C2C;
        }
        
        QLineEdit:hover {
            border-color: #546E7A;
        }
        
        QLineEdit:disabled {
            background-color: #263238;
            border-color: #37474F;
            color: #546E7A;
        }
        
        QTextEdit {
            background-color: #1E1E1E;
            border: 2px solid #455A64;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: #FFFFFF;
        }
        
        QTextEdit:focus {
            border-color: #2196F3;
        }
        
        /* Combo Boxes */
        QComboBox {
            background-color: #1E1E1E;
            border: 2px solid #455A64;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #FFFFFF;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border-color: #546E7A;
        }
        
        QComboBox:focus {
            border-color: #2196F3;
        }
        
        QComboBox::drop-down {
            border: none;
            background: transparent;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border: none;
            width: 0px;
            height: 0px;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid #B0BEC5;
        }
        
        QComboBox QAbstractItemView {
            background-color: #1E1E1E;
            border: 1px solid #455A64;
            border-radius: 8px;
            padding: 4px;
            selection-background-color: #1565C0;
            selection-color: #FFFFFF;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border: none;
            border-radius: 4px;
            margin: 1px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #263238;
        }
        
        /* Check Boxes */
        QCheckBox {
            font-size: 14px;
            color: #FFFFFF;
            spacing: 12px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #546E7A;
            border-radius: 4px;
            background-color: #1E1E1E;
        }
        
        QCheckBox::indicator:hover {
            border-color: #2196F3;
            background-color: #263238;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2196F3;
            border-color: #2196F3;
        }
        
        QCheckBox::indicator:checked:hover {
            background-color: #1976D2;
        }
        
        /* Radio Buttons */
        QRadioButton {
            font-size: 14px;
            color: #FFFFFF;
            spacing: 12px;
        }
        
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #546E7A;
            border-radius: 10px;
            background-color: #1E1E1E;
        }
        
        QRadioButton::indicator:hover {
            border-color: #2196F3;
            background-color: #263238;
        }
        
        QRadioButton::indicator:checked {
            background-color: #2196F3;
            border-color: #2196F3;
        }
        
        /* Sliders */
        QSlider::groove:horizontal {
            background: #455A64;
            height: 6px;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background: #2196F3;
            border: 2px solid #2196F3;
            width: 20px;
            height: 20px;
            margin: -7px 0;
            border-radius: 10px;
        }
        
        QSlider::handle:horizontal:hover {
            background: #1976D2;
            border-color: #1976D2;
        }
        
        QSlider::sub-page:horizontal {
            background: #2196F3;
            border-radius: 3px;
        }
        
        /* Progress Bars */
        QProgressBar {
            background-color: #455A64;
            border-radius: 4px;
            height: 8px;
            text-align: center;
            font-size: 12px;
            color: #FFFFFF;
        }
        
        QProgressBar::chunk {
            background-color: #2196F3;
            border-radius: 4px;
        }
        
        /* Tab Widgets */
        QTabWidget::pane {
            border: 1px solid #455A64;
            border-radius: 8px;
            background-color: #1E1E1E;
            padding: 16px;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: transparent;
            padding: 12px 24px;
            margin: 0 2px;
            border-bottom: 3px solid transparent;
            color: #B0BEC5;
            font-size: 14px;
            font-weight: 500;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        
        QTabBar::tab:selected {
            color: #2196F3;
            border-bottom-color: #2196F3;
            background-color: #263238;
        }
        
        QTabBar::tab:hover {
            color: #1976D2;
            background-color: #37474F;
        }
        
        /* Tables */
        QTableWidget {
            background-color: #1E1E1E;
            border: 1px solid #455A64;
            border-radius: 8px;
            gridline-color: #37474F;
            selection-background-color: #1565C0;
            selection-color: #FFFFFF;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
            color: #FFFFFF;
        }
        
        QTableWidget::item:selected {
            background-color: #1565C0;
            color: #FFFFFF;
        }
        
        QTableWidget::item:hover {
            background-color: #263238;
        }
        
        QHeaderView::section {
            background-color: #263238;
            border: none;
            padding: 12px 8px;
            font-weight: 600;
            color: #B0BEC5;
            border-bottom: 1px solid #455A64;
        }
        
        /* Tree Widgets */
        QTreeWidget {
            background-color: #1E1E1E;
            border: 1px solid #455A64;
            border-radius: 8px;
            selection-background-color: #1565C0;
            selection-color: #FFFFFF;
        }
        
        QTreeWidget::item {
            padding: 4px;
            border: none;
            color: #FFFFFF;
            min-height: 24px;
        }
        
        QTreeWidget::item:selected {
            background-color: #1565C0;
        }
        
        QTreeWidget::item:hover {
            background-color: #263238;
        }
        
        QTreeWidget::branch:closed:has-children {
            image: none;
            border: none;
        }
        
        QTreeWidget::branch:open:has-children {
            image: none;
            border: none;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background: #263238;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #546E7A;
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #607D8B;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QScrollBar:horizontal {
            background: #263238;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background: #546E7A;
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #607D8B;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-size: 14px;
            font-weight: 600;
            color: #FFFFFF;
            border: 2px solid #455A64;
            border-radius: 8px;
            margin: 12px 0px;
            padding-top: 12px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            background-color: #121212;
        }
        
        /* Menu Bar */
        QMenuBar {
            background-color: #1E1E1E;
            color: #FFFFFF;
            border-bottom: 1px solid #455A64;
        }
        
        QMenuBar::item {
            padding: 8px 12px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #263238;
        }
        
        QMenu {
            background-color: #1E1E1E;
            border: 1px solid #455A64;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 24px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #1565C0;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #1E1E1E;
            color: #B0BEC5;
            border-top: 1px solid #455A64;
        }
        
        /* Tool Tips */
        QToolTip {
            background-color: #263238;
            color: #FFFFFF;
            border: 1px solid #455A64;
            border-radius: 4px;
            padding: 8px;
            font-size: 12px;
        }
        
        /* Splitters */
        QSplitter::handle {
            background-color: #455A64;
        }
        
        QSplitter::handle:horizontal {
            width: 4px;
        }
        
        QSplitter::handle:vertical {
            height: 4px;
        }
        """
    
    def _get_light_stylesheet(self) -> str:
        """Get comprehensive light theme stylesheet."""
        return """
        /* Main Window and Base Styling */
        QMainWindow {
            background-color: #FAFAFA;
            color: #212121;
        }
        
        QWidget {
            background-color: #FAFAFA;
            color: #212121;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 9pt;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #1976D2;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-width: 120px;
            min-height: 36px;
        }
        
        QPushButton:hover {
            background-color: #1565C0;
        }
        
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        
        QPushButton:disabled {
            background-color: #BDBDBD;
            color: #9E9E9E;
        }
        
        QPushButton[buttonType="secondary"] {
            background-color: transparent;
            color: #1976D2;
            border: 2px solid #1976D2;
        }
        
        QPushButton[buttonType="secondary"]:hover {
            background-color: #E3F2FD;
            border-color: #1565C0;
        }
        
        QPushButton[buttonType="danger"] {
            background-color: #D32F2F;
        }
        
        QPushButton[buttonType="danger"]:hover {
            background-color: #C62828;
        }
        
        /* Text Inputs */
        QLineEdit {
            background-color: #FFFFFF;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #212121;
            min-height: 20px;
        }
        
        QLineEdit:focus {
            border-color: #1976D2;
            background-color: #FFFFFF;
        }
        
        QLineEdit:hover {
            border-color: #BDBDBD;
        }
        
        QLineEdit:disabled {
            background-color: #F5F5F5;
            border-color: #E0E0E0;
            color: #BDBDBD;
        }
        
        QTextEdit {
            background-color: #FFFFFF;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: #212121;
        }
        
        QTextEdit:focus {
            border-color: #1976D2;
        }
        
        /* Combo Boxes */
        QComboBox {
            background-color: #FFFFFF;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #212121;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border-color: #BDBDBD;
        }
        
        QComboBox:focus {
            border-color: #1976D2;
        }
        
        QComboBox::drop-down {
            border: none;
            background: transparent;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border: none;
            width: 0px;
            height: 0px;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid #757575;
        }
        
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 4px;
            selection-background-color: #E3F2FD;
            selection-color: #1976D2;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border: none;
            border-radius: 4px;
            margin: 1px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #F5F5F5;
        }
        
        /* Check Boxes */
        QCheckBox {
            font-size: 14px;
            color: #212121;
            spacing: 12px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #757575;
            border-radius: 4px;
            background-color: #FFFFFF;
        }
        
        QCheckBox::indicator:hover {
            border-color: #1976D2;
            background-color: #E3F2FD;
        }
        
        QCheckBox::indicator:checked {
            background-color: #1976D2;
            border-color: #1976D2;
        }
        
        QCheckBox::indicator:checked:hover {
            background-color: #1565C0;
        }
        
        /* Radio Buttons */
        QRadioButton {
            font-size: 14px;
            color: #212121;
            spacing: 12px;
        }
        
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #757575;
            border-radius: 10px;
            background-color: #FFFFFF;
        }
        
        QRadioButton::indicator:hover {
            border-color: #1976D2;
            background-color: #E3F2FD;
        }
        
        QRadioButton::indicator:checked {
            background-color: #1976D2;
            border-color: #1976D2;
        }
        
        /* Sliders */
        QSlider::groove:horizontal {
            background: #E0E0E0;
            height: 6px;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background: #1976D2;
            border: 2px solid #1976D2;
            width: 20px;
            height: 20px;
            margin: -7px 0;
            border-radius: 10px;
        }
        
        QSlider::handle:horizontal:hover {
            background: #1565C0;
            border-color: #1565C0;
        }
        
        QSlider::sub-page:horizontal {
            background: #1976D2;
            border-radius: 3px;
        }
        
        /* Progress Bars */
        QProgressBar {
            background-color: #E0E0E0;
            border-radius: 4px;
            height: 8px;
            text-align: center;
            font-size: 12px;
            color: #212121;
        }
        
        QProgressBar::chunk {
            background-color: #1976D2;
            border-radius: 4px;
        }
        
        /* Tab Widgets */
        QTabWidget::pane {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            background-color: #FFFFFF;
            padding: 16px;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: transparent;
            padding: 12px 24px;
            margin: 0 2px;
            border-bottom: 3px solid transparent;
            color: #757575;
            font-size: 14px;
            font-weight: 500;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        
        QTabBar::tab:selected {
            color: #1976D2;
            border-bottom-color: #1976D2;
            background-color: #F5F5F5;
        }
        
        QTabBar::tab:hover {
            color: #1565C0;
            background-color: #E3F2FD;
        }
        
        /* Tables */
        QTableWidget {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            gridline-color: #F5F5F5;
            selection-background-color: #E3F2FD;
            selection-color: #1976D2;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
            color: #212121;
        }
        
        QTableWidget::item:selected {
            background-color: #E3F2FD;
            color: #1976D2;
        }
        
        QTableWidget::item:hover {
            background-color: #F5F5F5;
        }
        
        QHeaderView::section {
            background-color: #F5F5F5;
            border: none;
            padding: 12px 8px;
            font-weight: 600;
            color: #424242;
            border-bottom: 1px solid #E0E0E0;
        }
        
        /* Tree Widgets */
        QTreeWidget {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            selection-background-color: #E3F2FD;
            selection-color: #1976D2;
        }
        
        QTreeWidget::item {
            padding: 4px;
            border: none;
            color: #212121;
            min-height: 24px;
        }
        
        QTreeWidget::item:selected {
            background-color: #E3F2FD;
        }
        
        QTreeWidget::item:hover {
            background-color: #F5F5F5;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background: #F5F5F5;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background: #BDBDBD;
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #9E9E9E;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QScrollBar:horizontal {
            background: #F5F5F5;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background: #BDBDBD;
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: #9E9E9E;
        }
        
        /* Group Boxes */
        QGroupBox {
            font-size: 14px;
            font-weight: 600;
            color: #212121;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin: 12px 0px;
            padding-top: 12px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            background-color: #FAFAFA;
        }
        
        /* Menu Bar */
        QMenuBar {
            background-color: #FFFFFF;
            color: #212121;
            border-bottom: 1px solid #E0E0E0;
        }
        
        QMenuBar::item {
            padding: 8px 12px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #F5F5F5;
        }
        
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 24px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #E3F2FD;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #FFFFFF;
            color: #757575;
            border-top: 1px solid #E0E0E0;
        }
        
        /* Tool Tips */
        QToolTip {
            background-color: #FFFFFF;
            color: #212121;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 8px;
            font-size: 12px;
        }
        
        /* Splitters */
        QSplitter::handle {
            background-color: #E0E0E0;
        }
        
        QSplitter::handle:horizontal {
            width: 4px;
        }
        
        QSplitter::handle:vertical {
            height: 4px;
        }
        """
    
    def get_current_theme(self) -> str:
        """Get the currently active theme name."""
        return self.current_theme
    
    def get_available_themes(self) -> list[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())
    
    def get_theme_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Get color palette for specified theme (or current theme)."""
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, {}).get("colors", {})
    
    def apply_theme(self, theme_name: str) -> bool:
        """
        Apply the specified theme to the application.
        
        Args:
            theme_name: Name of the theme to apply
            
        Returns:
            True if theme was applied successfully, False otherwise
        """
        if theme_name not in self.themes:
            return False
        
        app = QApplication.instance()
        if not app:
            return False
        
        # Apply stylesheet
        stylesheet = self.themes[theme_name]["stylesheet"]
        app.setStyleSheet(stylesheet)
        
        # Set palette for additional styling
        self._apply_palette(theme_name)
        
        # Update current theme
        old_theme = self.current_theme
        self.current_theme = theme_name
        
        # Emit theme changed signal
        if old_theme != theme_name:
            self.theme_changed.emit(theme_name)
        
        return True
    
    def _apply_palette(self, theme_name: str):
        """Apply color palette to the application."""
        app = QApplication.instance()
        if not app:
            return
        
        colors = self.get_theme_colors(theme_name)
        palette = QPalette()
        
        # Set palette colors based on theme
        if theme_name == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface_variant"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface_variant"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["selected"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["on_primary"]))
        else:  # light theme
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface_variant"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["selected"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["primary"]))
        
        app.setPalette(palette)
    
    def toggle_theme(self) -> str:
        """
        Toggle between dark and light themes.
        
        Returns:
            Name of the newly applied theme
        """
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        return new_theme
    
    def get_color(self, color_name: str, theme_name: Optional[str] = None) -> str:
        """
        Get a specific color from the theme palette.
        
        Args:
            color_name: Name of the color to retrieve
            theme_name: Theme to get color from (defaults to current theme)
            
        Returns:
            Hex color string or empty string if color not found
        """
        theme_name = theme_name or self.current_theme
        colors = self.get_theme_colors(theme_name)
        return colors.get(color_name, "")
    
    def is_dark_theme(self) -> bool:
        """Check if the current theme is a dark theme."""
        return self.current_theme == "dark"
    
    def get_theme_info(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get complete theme information.
        
        Args:
            theme_name: Theme to get info for (defaults to current theme)
            
        Returns:
            Dictionary containing theme information
        """
        theme_name = theme_name or self.current_theme
        theme_data = self.themes.get(theme_name, {})
        
        return {
            "name": theme_data.get("name", theme_name),
            "colors": theme_data.get("colors", {}),
            "is_dark": theme_name == "dark",
            "is_current": theme_name == self.current_theme
        }

# Global theme manager instance
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager