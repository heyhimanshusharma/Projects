# PDF Viewer Application

A modern, feature-rich PDF viewer built with PyQt5 and PyMuPDF, featuring touch gestures, continuous scrolling, and a sleek dark interface.

## Features

- 🖱️ **Continuous Page Scrolling**: Navigate through pages naturally with mouse wheel
- 📱 **Touch Gestures**: Pinch-to-zoom support for touchscreens and trackpads
- 🔍 **Zoom Controls**: Multiple zoom options with smooth scaling
- 🎨 **Modern Dark UI**: Sleek interface with larger, more visible icons
- 📄 **Page Navigation**: Quick page jumping and navigation controls
- 🏗️ **Modular Architecture**: Clean, separated code for easy maintenance

## Project Structure

```
pdf_viewer/
├── main.py       # Main application entry point
├── core.py       # Core PDF handling logic
├── ui.py         # UI components and styling
├── widget.py    # Touch and gesture handling
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python pdf_viewer_main.py
```

### Controls

- **Mouse Wheel**: Scroll through pages continuously
- **Ctrl + Mouse Wheel**: Zoom in/out
- **Pinch Gestures**: Zoom on touchscreens/trackpads
- **Page Input**: Jump to specific page numbers
- **Navigation Buttons**: Previous/Next page controls
- **Toolbar**: Access various PDF tools and options

## Module Details

### `pdf_viewer_main.py`
- Main application class (`PDFViewerApp`)
- Coordinates all modules
- Handles UI events and user interactions
- Application entry point

### `pdf_viewer_core.py`
- Core PDF document management (`PDFViewerCore`)
- Document loading and rendering
- Page navigation logic
- Zoom and scroll state management

### `pdf_viewer_ui.py`
- UI component factory (`PDFViewerUI`)
- Toolbar builder (`ToolbarBuilder`)
- Styling and layout definitions
- Reusable UI components

### `pdf_content_widget.py`
- Touch event handling (`PDFContentWidget`)
- Gesture recognition for pinch-to-zoom
- Mouse wheel event processing
- Scroll and zoom gesture coordination

## Customization

### Adding New Features

1. **UI Components**: Add new methods to `PDFViewerUI`
2. **Core Logic**: Extend `PDFViewerCore` for document operations
3. **Gestures**: Modify `PDFContentWidget` for new touch interactions
4. **Main App**: Update `PDFViewerApp` to connect new components

### Styling

Modify the stylesheet strings in `pdf_viewer_ui.py` to change:
- Colors and themes
- Button sizes and spacing
- Typography and fonts
- Layout margins and padding

### Configuration

Adjust constants in `PDFViewerCore.__init__()`:
- `scroll_threshold`: Scroll sensitivity
- Zoom limits (min/max values)
- Default zoom level

## Dependencies

- **PyQt5**: GUI framework
- **PyMuPDF (fitz)**: PDF rendering and manipulation
- **Python 3.7+**: Required Python version

## Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure all files are in the same directory
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Touch Gestures Not Working**: Verify touchscreen/trackpad drivers
4. **PDF Loading Issues**: Check file permissions and PDF validity

### Performance Tips

- **Large PDFs**: Consider implementing page caching for better performance
- **High DPI Displays**: The interface automatically scales for better visibility
- **Memory Usage**: The application loads one page at a time to optimize memory

## Development
The app came out of inspiration and frustation using windows defualt app and lack of minimatlistic pdf viewer other than [sumatraPDF](https://www.sumatrapdfreader.org/free-pdf-reader). It is [vibe-coded](https://en.wikipedia.org/wiki/Vibe_coding) using claude, ChatGPT and Gemini and i am learning the libraries along the go. Any suggestions or help are welcomed.
