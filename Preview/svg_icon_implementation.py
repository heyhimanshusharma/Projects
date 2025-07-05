"""
SVG Icon Implementation for PDF Viewer
This module shows how to integrate SVG icons into your PyQt5 PDF viewer
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QSize, Qt


class IconManager:
    """Manager for handling SVG icons in the PDF viewer"""
    
    def __init__(self):
        self.icon_cache = {}
        self.default_icon_size = (24, 24)
    
    def svg_to_qicon(self, svg_path, size=None):
        """Convert SVG file to QIcon with optional caching"""
        if size is None:
            size = self.default_icon_size
        
        # Create cache key
        cache_key = f"{svg_path}_{size[0]}x{size[1]}"
        
        # Return cached icon if available
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        
        # Create new icon
        try:
            # Load SVG
            svg_renderer = QSvgRenderer(svg_path)
            
            # Create pixmap
            pixmap = QPixmap(QSize(size[0], size[1]))
            pixmap.fill(Qt.transparent)
            
            # Render SVG to pixmap
            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
            
            # Create icon
            icon = QIcon(pixmap)
            
            # Cache the icon
            self.icon_cache[cache_key] = icon
            
            return icon
            
        except Exception as e:
            print(f"Error loading SVG icon from {svg_path}: {e}")
            return QIcon()  # Return empty icon as fallback
    
    def svg_string_to_qicon(self, svg_string, size=None):
        """Convert SVG string content to QIcon"""
        if size is None:
            size = self.default_icon_size
        
        try:
            # Create SVG renderer from string
            svg_renderer = QSvgRenderer()
            svg_renderer.load(svg_string.encode('utf-8'))
            
            # Create pixmap
            pixmap = QPixmap(QSize(size[0], size[1]))
            pixmap.fill(Qt.transparent)
            
            # Render SVG to pixmap
            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
            
            # Create and return icon
            return QIcon(pixmap)
            
        except Exception as e:
            print(f"Error creating icon from SVG string: {e}")
            return QIcon()
    
    def create_colored_icon(self, svg_path, color="#ffffff", size=None):
        """Create a colored version of an SVG icon"""
        if size is None:
            size = self.default_icon_size
        
        try:
            # Read SVG file
            with open(svg_path, 'r') as f:
                svg_content = f.read()
            
            # Replace stroke/fill colors (basic implementation)
            # You might need to adjust this based on your SVG structure
            svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
            svg_content = svg_content.replace('fill="currentColor"', f'fill="{color}"')
            svg_content = svg_content.replace('stroke="#000"', f'stroke="{color}"')
            svg_content = svg_content.replace('fill="#000"', f'fill="{color}"')
            
            return self.svg_string_to_qicon(svg_content, size)
            
        except Exception as e:
            print(f"Error creating colored icon: {e}")
            return QIcon()


# Updated PDFViewerUI class with SVG icon support
class PDFViewerUI:
    """UI component factory and styling for PDF viewer with SVG icons"""
    
    def __init__(self):
        self.icon_manager = IconManager()
    
    def create_toolbar_container(self):
        """Create the main toolbar container"""
        toolbar_container = QWidget()
        toolbar_container.setStyleSheet(
            "background-color: #3c3c3c; border-bottom: 1px solid #4a4a4a;"
        )
        return toolbar_container
    
    def create_toolbar_layout(self, container):
        """Create and configure toolbar layout"""
        toolbar_layout = QHBoxLayout(container)
        toolbar_layout.setContentsMargins(15, 8, 15, 8)
        toolbar_layout.setSpacing(8)
        return toolbar_layout
    
    def create_icon_button(self, icon_path, tooltip, fixed_width=None, icon_size=(20, 20)):
        """Create a styled toolbar button with SVG icon"""
        button = QPushButton()
        button.setToolTip(tooltip)
        
        # Set icon
        icon = self.icon_manager.svg_to_qicon(icon_path, icon_size)
        button.setIcon(icon)
        button.setIconSize(QSize(icon_size[0], icon_size[1]))
        
        # Apply styling
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
    
    def create_button_with_fallback(self, icon_path, fallback_text, tooltip, fixed_width=None):
        """Create button with SVG icon and text fallback"""
        button = QPushButton()
        button.setToolTip(tooltip)
        
        # Try to load icon, fall back to text
        icon = self.icon_manager.svg_to_qicon(icon_path, (20, 20))
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(20, 20))
        else:
            button.setText(fallback_text)
        
        # Apply styling
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


# Updated ToolbarBuilder class with SVG icon support
class ToolbarBuilder:
    """Builder class for creating toolbar with SVG icons"""
    
    def __init__(self, layout, icon_manager=None):
        self.layout = layout
        self.buttons = {}
        self.icon_manager = icon_manager or IconManager()
    
    def add_icon_button(self, key, icon_path, tooltip, fixed_width=None, icon_size=(20, 20)):
        """Add a button with SVG icon to the toolbar"""
        button = QPushButton()
        button.setToolTip(tooltip)
        
        # Set icon
        icon = self.icon_manager.svg_to_qicon(icon_path, icon_size)
        button.setIcon(icon)
        button.setIconSize(QSize(icon_size[0], icon_size[1]))
        
        # Apply styling
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
        
        self.layout.addWidget(button)
        self.buttons[key] = button
        return button
    
    def add_button_with_fallback(self, key, icon_path, fallback_text, tooltip, fixed_width=None):
        """Add button with icon and text fallback"""
        button = QPushButton()
        button.setToolTip(tooltip)
        
        # Try to load icon, fall back to text
        icon = self.icon_manager.svg_to_qicon(icon_path, (20, 20))
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(20, 20))
        else:
            button.setText(fallback_text)
        
        # Apply styling
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


# Example usage in your main application
def create_toolbar_with_svg_icons(main_layout):
    """Example of how to create toolbar with SVG icons"""
    
    # Create toolbar container
    toolbar_container = QWidget()
    toolbar_container.setStyleSheet(
        "background-color: #3c3c3c; border-bottom: 1px solid #4a4a4a;"
    )
    
    # Create toolbar layout
    toolbar_layout = QHBoxLayout(toolbar_container)
    toolbar_layout.setContentsMargins(15, 8, 15, 8)
    toolbar_layout.setSpacing(8)
    
    # Create toolbar builder with icon manager
    icon_manager = IconManager()
    builder = ToolbarBuilder(toolbar_layout, icon_manager)
    
    # Add buttons with SVG icons (replace with your actual SVG paths)
    # Zoom controls
    builder.add_icon_button("zoom_out", "icons/zoom-out.svg", "Zoom Out", 40)
    builder.add_icon_button("zoom_in", "icons/zoom-in.svg", "Zoom In", 40)
    builder.add_spacing(15)
    
    # Page navigation
    builder.add_icon_button("prev_page", "icons/chevron-left.svg", "Previous Page", 40)
    builder.add_icon_button("next_page", "icons/chevron-right.svg", "Next Page", 40)
    builder.add_spacing(15)
    
    # File operations
    builder.add_icon_button("open_pdf", "icons/folder-open.svg", "Open PDF File")
    builder.add_icon_button("search", "icons/search.svg", "Search")
    builder.add_icon_button("print", "icons/printer.svg", "Print")
    builder.add_icon_button("rotate", "icons/rotate-cw.svg", "Rotate View")
    builder.add_icon_button("fullscreen", "icons/maximize.svg", "Full Screen")
    
    # Add with fallback for missing icons
    builder.add_button_with_fallback("read_aloud", "icons/volume-2.svg", "🔊", "Read Aloud")
    
    main_layout.addWidget(toolbar_container)
    
    return builder.get_all_buttons()
