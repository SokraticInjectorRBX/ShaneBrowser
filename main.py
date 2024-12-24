import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QColor, QPalette

# DNS Resolver - Map the custom domain to a real website
def custom_dns_resolver(url):
    if url.startswith("shane://"):
        domain = url[len("shane://"):]
        # Define custom mapping of domains to real websites
        if domain == "robertstover.shane":
            return "file:///html/RobertStover.html"  # Redirect to Robert Stover's website
        elif domain == "shanestover.shane":
            return "file:///html/index.html"  # Update with actual path to HTML file
    return url  # Return the URL as is if no match

class BrowserTab(QWebEngineView):
    def __init__(self, url, tab_name):
        super().__init__()
        resolved_url = custom_dns_resolver(url)  # Resolve the URL first
        self.setUrl(QUrl(resolved_url))  # Set the resolved URL
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.tab_name = tab_name

    def reload(self):
        self.reload()

    def go_back(self):
        if self.history().canGoBack():
            self.back()

    def go_forward(self):
        if self.history().canGoForward():
            self.forward()

class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shane Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.setCentralWidget(self.tabs)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL (shane://WEBSITE.shane)")

        self.nav_buttons = QHBoxLayout()
        self.back_button = QPushButton("<", self)
        self.forward_button = QPushButton(">", self)
        self.refresh_button = QPushButton("↻", self)
        self.nav_buttons.addWidget(self.back_button)
        self.nav_buttons.addWidget(self.forward_button)
        self.nav_buttons.addWidget(self.refresh_button)
        
        self.back_button.clicked.connect(self.back_navigation)
        self.forward_button.clicked.connect(self.forward_navigation)
        self.refresh_button.clicked.connect(self.refresh_page)

        self.url_input.returnPressed.connect(self.load_url_from_input)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.nav_buttons)
        self.main_layout.addWidget(self.url_input)
        self.main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Apply custom dark theme
        self.apply_dark_theme()

        # Open the first tab with a custom URL
        self.open_new_tab("shane://shanestover.shane")

    def open_new_tab(self, url):
        resolved_url = custom_dns_resolver(url)
        tab = BrowserTab(resolved_url, url)  # Set the custom URL (shane://WEBSITE.shane) as the tab name
        tab.urlChanged.connect(self.update_url_input)
        self.tabs.addTab(tab, url)  # Set custom URL as the tab name

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def load_url_from_input(self):
        url = self.url_input.text()
        self.open_new_tab(url)

    def back_navigation(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.go_back()

    def forward_navigation(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.go_forward()

    def refresh_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.reload()

    def update_url_input(self, url):
        self.url_input.setText(url.toString())

    def apply_dark_theme(self):
        """Apply a dark theme with a purple-blue gradient."""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Highlight, QColor(66, 133, 244))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)

        self.setPalette(dark_palette)

        # Set gradient background for the main window
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(50, 0, 100, 255), stop:1 rgba(0, 0, 100, 255));
            }
            QPushButton {
                background-color: #444444;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QLineEdit {
                background-color: #333333;
                border: 1px solid #444444;
                padding: 5px;
                color: white;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #444444;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabWidget::tab {
                background-color: #444444;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QTabWidget::tab:selected {
                background-color: #666666;
            }
        """)

# Start the application
app = QApplication(sys.argv)
app.setApplicationName("Shane Browser")

# Apply Chrome-like styling
app.setStyle("Fusion")

browser = CustomBrowser()
browser.show()
sys.exit(app.exec_())
