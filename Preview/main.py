"""
Main PDF Viewer Application
Combines all modules to create the complete PDF viewer
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgRenderer

# Import custom modules
from core import PDFViewerCore
from ui import PDFViewerUI, ToolbarBuilder
from widget import PDFContentWidget

class PDFViewerApp(QMainWindow):
    """Main PDF Viewer Application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preview")
        self.setGeometry(200, 200, 2000, 1600)
        self.setStyleSheet("QMainWindow { background-color: #0a0a0a; }")
        
        # Initialize core PDF functionality
        self.pdf_core = PDFViewerCore()
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create main layout
        central_widget, main_layout = PDFViewerUI.create_main_layout()
        self.setCentralWidget(central_widget)
        
        # Create toolbar
        self.create_toolbar(main_layout)
        
        # Create content area
        self.create_content_area(main_layout)
        
        # Update initial display
        self.update_page_display()
    
    def create_toolbar(self, main_layout):
        """Create the toolbar with all buttons"""
        toolbar_container = PDFViewerUI.create_toolbar_container()
        toolbar_layout = PDFViewerUI.create_toolbar_layout(toolbar_container)
        
        # Create toolbar builder
        builder = ToolbarBuilder(toolbar_layout)
        
        # Add toolbar buttons
        # builder.add_button("toc", "☰", "Table of Contents")
        # builder.add_button("view_options", "▼", "View Options")
        # builder.add_spacing(15)
        
        # builder.add_button("draw", "D", "Draw Tool")
        # builder.add_button("text_select", "🖚", "Text Selection")
        # builder.add_button("highlight", "🖍️", "Highlight Tool")
        # builder.add_button("erase", "🧹", "Erase Tool")
        # builder.add_spacing(15)
        
        # Zoom controls
        zoom_out_btn = builder.add_button("zoom_out", "−", "Zoom Out", 40)
        zoom_in_btn = builder.add_button("zoom_in", "+", "Zoom In", 40)
        
        # Page navigation
        self.page_input = PDFViewerUI.create_page_input()
        builder.add_widget(self.page_input)
        
        self.total_pages_label = PDFViewerUI.create_page_label()
        builder.add_widget(self.total_pages_label)
        builder.add_spacing(15)
        
        prev_btn = builder.add_button("prev_page", "◀", "Previous Page", 40)
        next_btn = builder.add_button("next_page", "▶", "Next Page", 40)
        builder.add_spacing(15)
        
        # builder.add_button("fit_width", "↔", "Fit to Width/Page")
        builder.add_stretch()
        
        # File and action buttons
        open_btn = builder.add_button("open_pdf", "📂", "Open PDF File")
        # builder.add_button("search", "🔍", "Search")
        # builder.add_button("print", "🖨️", "Print")
        # builder.add_button("rotate", "🔄", "Rotate View")
        # builder.add_button("read_aloud", "🔊", "Read Aloud")
        # builder.add_button("fullscreen", "⛶", "Full Screen")
        builder.add_spacing(15)
        
        # Store buttons for later use
        self.toolbar_buttons = builder.get_all_buttons()
        
        main_layout.addWidget(toolbar_container)
    
    def create_content_area(self, main_layout):
        """Create the PDF content display area"""
        # Create custom content widget for touch events
        self.pdf_content_widget = PDFContentWidget(self)
        content_layout = PDFViewerUI.create_content_widget_layout()
        self.pdf_content_widget.setLayout(content_layout)
        
        # Create content label
        self.pdf_content_label = PDFViewerUI.create_content_label()
        content_layout.addWidget(self.pdf_content_label)
        
        # Create scroll area
        self.scroll_area = PDFViewerUI.create_scroll_area()
        self.scroll_area.setWidget(self.pdf_content_widget)
        
        main_layout.addWidget(self.scroll_area)
    
    def connect_signals(self):
        """Connect UI signals to handlers"""
        # Page navigation
        self.page_input.returnPressed.connect(self.go_to_page_from_input)
        
        # Toolbar buttons
        self.toolbar_buttons["zoom_in"].clicked.connect(self.zoom_in)
        self.toolbar_buttons["zoom_out"].clicked.connect(self.zoom_out)
        self.toolbar_buttons["prev_page"].clicked.connect(self.prev_page)
        self.toolbar_buttons["next_page"].clicked.connect(self.next_page)
        self.toolbar_buttons["open_pdf"].clicked.connect(self.open_pdf_file)
    
    def open_pdf_file(self):
        """Open a PDF file dialog and load the selected file"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        
        if file_path:
            success, message = self.pdf_core.load_pdf(file_path)
            if success:
                self.update_page_display()
                # QMessageBox.information(self, "PDF Loaded", message)
            else:
                QMessageBox.critical(self, "Error Loading PDF", message)
    
    def update_page_display(self):
        """Update the page display and UI elements"""
        doc_info = self.pdf_core.get_document_info()
        
        if doc_info['has_document'] and doc_info['total_pages'] > 0:
            self.page_input.setText(str(doc_info['current_page']))
            self.total_pages_label.setText(f"of {doc_info['total_pages']}")
            self.display_page()
        else:
            self.page_input.setText("0")
            self.total_pages_label.setText("of 0")
            self.pdf_content_label.setText("Please open a PDF file.")
    
    def display_page(self):
        """Display the current page"""
        pixmap = self.pdf_core.get_page_pixmap()
        if pixmap:
            self.pdf_content_label.setPixmap(pixmap)
            
            # Apply scroll position if needed
            if hasattr(self, 'scroll_area'):
                scrollbar = self.scroll_area.verticalScrollBar()
                scrollbar.setValue(self.pdf_core.scroll_position)
    
    def go_to_page_from_input(self):
        """Handle page navigation from input field"""
        try:
            page_num = int(self.page_input.text())
            success, message = self.pdf_core.go_to_page(page_num)
            if success:
                self.update_page_display()
            else:
                QMessageBox.warning(self, "Invalid Page", message)
                self.page_input.setText(str(self.pdf_core.current_page_num))
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the page.")
            self.page_input.setText(str(self.pdf_core.current_page_num))
    
    def next_page(self):
        """Go to next page"""
        success, message = self.pdf_core.next_page()
        if success:
            self.update_page_display()
        elif message:
            QMessageBox.information(self, "Navigation", message)
    
    def prev_page(self):
        """Go to previous page"""
        success, message = self.pdf_core.prev_page()
        if success:
            self.update_page_display()
        elif message:
            QMessageBox.information(self, "Navigation", message)
    
    def zoom_in(self):
        """Zoom in the current page"""
        if self.pdf_core.zoom_in():
            self.update_page_display()
    
    def zoom_out(self):
        """Zoom out the current page"""
        if self.pdf_core.zoom_out():
            self.update_page_display()
    
    def zoom_in_by_factor(self, factor):
        """Zoom in by specific factor (for pinch gestures)"""
        if self.pdf_core.zoom_in_by_factor(factor):
            self.update_page_display()
    
    def zoom_out_by_factor(self, factor):
        """Zoom out by specific factor (for pinch gestures)"""
        if self.pdf_core.zoom_out_by_factor(factor):
            self.update_page_display()
    
    def scroll_up(self):
        """Handle upward scrolling"""
        if not self.pdf_core.pdf_document:
            return
        
        scrollbar = self.scroll_area.verticalScrollBar()
        current_scroll = scrollbar.value()
        
        # If at top, go to previous page
        if current_scroll <= 0:
            success, _ = self.pdf_core.prev_page()
            if success:
                self.update_page_display()
                # Start at bottom of previous page
                scrollbar.setValue(scrollbar.maximum())
        else:
            # Scroll up within page
            new_scroll = max(0, current_scroll - self.pdf_core.scroll_threshold)
            scrollbar.setValue(new_scroll)
    
    def scroll_down(self):
        """Handle downward scrolling"""
        if not self.pdf_core.pdf_document:
            return
        
        scrollbar = self.scroll_area.verticalScrollBar()
        current_scroll = scrollbar.value()
        max_scroll = scrollbar.maximum()
        
        # If at bottom, go to next page
        if current_scroll >= max_scroll:
            success, _ = self.pdf_core.next_page()
            if success:
                self.update_page_display()
                # Start at top of next page
                scrollbar.setValue(0)
        else:
            # Scroll down within page
            new_scroll = min(max_scroll, current_scroll + self.pdf_core.scroll_threshold)
            scrollbar.setValue(new_scroll)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    viewer = PDFViewerApp()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
