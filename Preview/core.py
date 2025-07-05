"""
PDF Viewer Core Module
Contains the main PDF viewing logic and document management
"""

import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage


class PDFViewerCore:
    """Core PDF document handling and rendering logic"""
    
    def __init__(self):
        self.pdf_document = None
        self.current_pdf_path = None
        self.current_page_num = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        self.scroll_position = 0
        self.page_height = 0
        self.scroll_threshold = 100
    
    def load_pdf(self, file_path):
        """Load a PDF document from file path"""
        try:
            self.pdf_document = fitz.open(file_path)
            self.current_pdf_path = file_path
            self.total_pages = len(self.pdf_document)
            self.current_page_num = 1
            self.scroll_position = 0
            return True, f"Successfully loaded: {os.path.basename(file_path)}"
        except Exception as e:
            self.reset_pdf_state()
            return False, f"Could not load PDF: {e}"
    
    def get_page_pixmap(self, page_num=None):
        """Get pixmap for specified page (or current page if None)"""
        if not self.pdf_document:
            return None
            
        if page_num is None:
            page_num = self.current_page_num
            
        if 0 <= page_num - 1 < self.total_pages:
            page = self.pdf_document.load_page(page_num - 1)
            pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_level, self.zoom_level))
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.page_height = pixmap.height()
            return pixmap
        return None
    
    def go_to_page(self, page_num):
        """Navigate to a specific page"""
        if self.pdf_document and self.total_pages > 0:
            if 1 <= page_num <= self.total_pages:
                self.current_page_num = page_num
                self.scroll_position = 0
                return True, None
            else:
                return False, f"Page number must be between 1 and {self.total_pages}."
        return False, "No PDF document loaded."
    
    def next_page(self):
        """Go to next page"""
        if self.pdf_document and self.current_page_num < self.total_pages:
            return self.go_to_page(self.current_page_num + 1)
        elif self.pdf_document:
            return False, "You are already on the last page."
        return False, "No PDF document loaded."
    
    def prev_page(self):
        """Go to previous page"""
        if self.pdf_document and self.current_page_num > 1:
            return self.go_to_page(self.current_page_num - 1)
        elif self.pdf_document:
            return False, "You are already on the first page."
        return False, "No PDF document loaded."
    
    def zoom_in(self, factor=0.1):
        """Zoom in by specified factor"""
        self.zoom_level = min(self.zoom_level + factor, 3.0)
        return True
    
    def zoom_out(self, factor=0.1):
        """Zoom out by specified factor"""
        self.zoom_level = max(self.zoom_level - factor, 0.5)
        return True
    
    def zoom_in_by_factor(self, factor):
        """Zoom in by multiplication factor"""
        self.zoom_level = min(self.zoom_level * factor, 3.0)
        return True
    
    def zoom_out_by_factor(self, factor):
        """Zoom out by division factor"""
        self.zoom_level = max(self.zoom_level / factor, 0.5)
        return True
    
    def reset_pdf_state(self):
        """Reset all PDF-related state"""
        self.pdf_document = None
        self.current_pdf_path = None
        self.current_page_num = 0
        self.total_pages = 0
        self.zoom_level = 1.0
        self.scroll_position = 0
        self.page_height = 0
    
    def get_document_info(self):
        """Get current document information"""
        return {
            'current_page': self.current_page_num,
            'total_pages': self.total_pages,
            'zoom_level': self.zoom_level,
            'file_path': self.current_pdf_path,
            'has_document': self.pdf_document is not None
        }
