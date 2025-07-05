"""
PDF Content Widget Module
Handles touch events and gestures for PDF viewing
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class PDFContentWidget(QWidget):
    """Custom widget to handle pinch-to-zoom gestures and mouse wheel events"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_viewer = parent
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.pinch_scale_factor = 1.0
        self.last_pinch_scale = 1.0
        
    def event(self, event):
        """Handle touch events for pinch-to-zoom"""
        if event.type() == event.TouchBegin or event.type() == event.TouchUpdate or event.type() == event.TouchEnd:
            return self.handle_touch_event(event)
        return super().event(event)
    
    def handle_touch_event(self, event):
        """Process touch events for pinch gestures"""
        if len(event.touchPoints()) == 2:
            # Handle pinch gesture
            touch_point1 = event.touchPoints()[0]
            touch_point2 = event.touchPoints()[1]
            
            # Calculate distance between touch points
            current_distance = ((touch_point1.pos().x() - touch_point2.pos().x()) ** 2 + 
                              (touch_point1.pos().y() - touch_point2.pos().y()) ** 2) ** 0.5
            
            if hasattr(self, 'initial_distance'):
                scale_factor = current_distance / self.initial_distance
                zoom_delta = scale_factor - self.last_pinch_scale
                
                if abs(zoom_delta) > 0.05:  # Threshold to prevent too sensitive zooming
                    if zoom_delta > 0:
                        self.parent_viewer.zoom_in_by_factor(1.1)
                    else:
                        self.parent_viewer.zoom_out_by_factor(1.1)
                    self.last_pinch_scale = scale_factor
            else:
                self.initial_distance = current_distance
                self.last_pinch_scale = 1.0
            
            if event.type() == event.TouchEnd:
                delattr(self, 'initial_distance')
                self.last_pinch_scale = 1.0
            
            return True
        return super().event(event)
    
    def wheelEvent(self, event):
        """Handle mouse wheel events for zoom and scroll"""
        # Handle mouse wheel zoom with Ctrl key
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.parent_viewer.zoom_in()
            else:
                self.parent_viewer.zoom_out()
            event.accept()
        else:
            # Handle continuous page scrolling
            if event.angleDelta().y() > 0:
                self.parent_viewer.scroll_up()
            else:
                self.parent_viewer.scroll_down()
            event.accept()
