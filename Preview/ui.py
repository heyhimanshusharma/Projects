"""
PDF Viewer UI Module
Contains UI components and styling for the PDF viewer
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                           QLineEdit, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PDFViewerUI:
    """UI component factory and styling for PDF viewer"""
    
    @staticmethod
    def create_toolbar_container():
        """Create the main toolbar container"""
        toolbar_container = QWidget()
        toolbar_container.setStyleSheet(
            "background-color: #3c3c3c; border-bottom: 1px solid #4a4a4a;"
        )
        return toolbar_container
    
    @staticmethod
    def create_toolbar_layout(container):
        """Create and configure toolbar layout"""
        toolbar_layout = QHBoxLayout(container)
        toolbar_layout.setContentsMargins(15, 8, 15, 8)
        toolbar_layout.setSpacing(8)
        return toolbar_layout
    
    @staticmethod
    def create_button(text, tooltip, fixed_width=None):
        """Create a styled toolbar button"""
        button = QPushButton(text)
        button.setToolTip(tooltip)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #4a4a4a;
                border-radius: 6px;
                padding: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        if fixed_width:
            button.setFixedSize(fixed_width, 40)
        else:
            button.setFixedSize(40, 40)
        return button
    
    @staticmethod
    def create_page_input():
        """Create the page number input field"""
        page_input = QLineEdit("0")
        page_input.setFixedSize(50, 40)
        page_input.setAlignment(Qt.AlignCenter)
        page_input.setStyleSheet("""
            QLineEdit {
                background-color: #5a5a5a;
                color: white;
                border: 1px solid #6a6a6a;
                border-radius: 5px;
                padding: 2px;
                font-size: 16px;
            }
        """)
        return page_input
    
    @staticmethod
    def create_page_label():
        """Create the total pages label"""
        label = QLabel("of 0")
        label.setStyleSheet("color: white; font-size: 16px;")
        return label
    
    @staticmethod
    def create_content_label():
        """Create the main content display label"""
        label = QLabel("Please open a PDF file.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #aaaaaa; font-size: 24px;")
        label.setWordWrap(True)
        return label
    
    @staticmethod
    def create_scroll_area():
        """Create the main scroll area"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #1e1e1e; border: none;")
        return scroll_area
    
    @staticmethod
    def create_main_layout():
        """Create the main application layout"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        return central_widget, main_layout
    
    @staticmethod
    def create_content_widget_layout():
        """Create layout for PDF content widget"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        return layout


class ToolbarBuilder:
    """Builder class for creating toolbar with buttons"""
    
    def __init__(self, layout):
        self.layout = layout
        self.buttons = {}
    
    def add_button(self, key, text, tooltip, fixed_width=None):
        """Add a button to the toolbar"""
        button = PDFViewerUI.create_button(text, tooltip, fixed_width)
        self.layout.addWidget(button)
        self.buttons[key] = button
        return button
    
    def add_spacing(self, width):
        """Add spacing to the toolbar"""
        self.layout.addSpacing(width)
        return self
    
    def add_stretch(self):
        """Add stretch to the toolbar"""
        self.layout.addStretch(1)
        return self
    
    def add_widget(self, widget):
        """Add a custom widget to the toolbar"""
        self.layout.addWidget(widget)
        return self
    
    def get_button(self, key):
        """Get a button by key"""
        return self.buttons.get(key)
    
    def get_all_buttons(self):
        """Get all buttons"""
        return self.buttons
