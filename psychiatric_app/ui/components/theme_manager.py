"""
Theme manager for dark/light theme switching and styling
"""

import qdarktheme
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

class ThemeManager(QObject):
    """Theme manager for handling dark/light theme switching"""
    
    theme_changed = pyqtSignal(str)  # Signal emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "primary": "#2196F3",
                "secondary": "#FF9800", 
                "success": "#4CAF50",
                "warning": "#FF9800",
                "error": "#F44336",
                "background": "#121212",
                "surface": "#1E1E1E",
                "surface_variant": "#2C2C2C",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B0B0B0",
                "border": "#404040",
                "shadow": "rgba(0, 0, 0, 0.5)"
            },
            "light": {
                "primary": "#1976D2",
                "secondary": "#F57C00",
                "success": "#388E3C", 
                "warning": "#F57C00",
                "error": "#D32F2F",
                "background": "#FAFAFA",
                "surface": "#FFFFFF",
                "surface_variant": "#F5F5F5",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "border": "#E0E0E0",
                "shadow": "rgba(0, 0, 0, 0.15)"
            }
        }
    
    def apply_theme(self, theme_name="dark"):
        """Apply the specified theme to the application"""
        if theme_name not in self.themes:
            theme_name = "dark"
        
        self.current_theme = theme_name
        
        # Apply qdarktheme
        if theme_name == "dark":
            qdarktheme.setup_theme("dark")
        else:
            qdarktheme.setup_theme("light")
        
        # Apply custom styles
        app = QApplication.instance()
        if app:
            app.setStyleSheet(self.get_custom_styles())
        
        # Emit signal
        self.theme_changed.emit(theme_name)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
    
    def get_theme_colors(self):
        """Get current theme color palette"""
        return self.themes[self.current_theme]
    
    def get_color(self, color_name):
        """Get specific color from current theme"""
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    def get_custom_styles(self):
        """Get custom stylesheet for the current theme"""
        colors = self.get_theme_colors()
        
        return f"""
        /* Main Window Styles */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
        }}
        
        /* Card Styles */
        .ModernCard {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 16px;
        }}
        
        /* Button Styles */
        QPushButton {{
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-width: 120px;
        }}
        
        QPushButton.primary {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        QPushButton.primary:hover {{
            background-color: {colors['primary']};
            filter: brightness(1.1);
        }}
        
        QPushButton.secondary {{
            background-color: transparent;
            color: {colors['primary']};
            border: 2px solid {colors['primary']};
        }}
        
        QPushButton.secondary:hover {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        QPushButton.danger {{
            background-color: {colors['error']};
            color: white;
        }}
        
        QPushButton.danger:hover {{
            background-color: {colors['error']};
            filter: brightness(1.1);
        }}
        
        /* Input Field Styles */
        QLineEdit {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {colors['text_primary']};
        }}
        
        QLineEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        QTextEdit {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: {colors['text_primary']};
        }}
        
        QTextEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        /* ComboBox Styles */
        QComboBox {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: {colors['text_primary']};
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {colors['primary']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 4px;
            selection-background-color: {colors['primary']};
            selection-color: white;
        }}
        
        /* Table Styles */
        QTableWidget {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            gridline-color: {colors['border']};
            selection-background-color: {colors['primary']};
            selection-color: white;
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}
        
        QHeaderView::section {{
            background-color: {colors['surface_variant']};
            border: none;
            padding: 12px 8px;
            font-weight: 600;
            color: {colors['text_primary']};
        }}
        
        /* Tab Widget Styles */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['surface']};
            padding: 16px;
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            padding: 12px 24px;
            margin: 0 2px;
            border-bottom: 3px solid transparent;
            color: {colors['text_secondary']};
            font-size: 14px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            color: {colors['primary']};
            border-bottom-color: {colors['primary']};
        }}
        
        QTabBar::tab:hover {{
            color: {colors['primary']};
            background-color: {colors['surface_variant']};
        }}
        
        /* Tree Widget Styles */
        QTreeWidget {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            selection-background-color: {colors['primary']};
            selection-color: white;
        }}
        
        QTreeWidget::item {{
            padding: 4px;
            border: none;
        }}
        
        /* CheckBox Styles */
        QCheckBox {{
            font-size: 14px;
            color: {colors['text_primary']};
            spacing: 12px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['surface']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {colors['primary']};
            background-color: {colors['surface_variant']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
        }}
        
        /* Progress Bar Styles */
        QProgressBar {{
            background-color: {colors['surface_variant']};
            border-radius: 4px;
            height: 8px;
            text-align: center;
            font-size: 12px;
            color: {colors['text_primary']};
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: 4px;
        }}
        
        /* Slider Styles */
        QSlider::groove:horizontal {{
            background: {colors['surface_variant']};
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background: {colors['primary']};
            border: 2px solid {colors['primary']};
            width: 20px;
            height: 20px;
            margin: -7px 0;
            border-radius: 10px;
        }}
        
        QSlider::sub-page:horizontal {{
            background: {colors['primary']};
            border-radius: 3px;
        }}
        
        /* Label Styles */
        QLabel {{
            color: {colors['text_primary']};
        }}
        
        QLabel.title {{
            font-size: 24px;
            font-weight: 600;
            color: {colors['text_primary']};
        }}
        
        QLabel.subtitle {{
            font-size: 18px;
            font-weight: 500;
            color: {colors['text_secondary']};
        }}
        
        /* Menu and Status Bar */
        QMenuBar {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border']};
        }}
        
        QStatusBar {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
            border-top: 1px solid {colors['border']};
        }}
        
        /* Scrollbar Styles */
        QScrollBar:vertical {{
            background: {colors['surface_variant']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {colors['primary']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {colors['primary']};
            filter: brightness(1.1);
        }}
        """