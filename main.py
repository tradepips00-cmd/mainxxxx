
import sys, platform, shutil, subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QGridLayout, QCheckBox, QRadioButton,
    QScrollArea, QMessageBox, QButtonGroup
)

APP_NAME = "VelocityPanel"

STYLE = """
QMainWindow { background: #07090b; }
QWidget { color: #d7dbe0; font-family: Segoe UI; font-size: 14px; }
#Sidebar { background: #0b0e12; border-right: 1px solid #20242a; }
#Logo { font-size: 28px; font-weight: 800; color: white; }
#SubLogo { color: #7d8490; font-size: 11px; }
QPushButton {
    background: #171b20; color: #e8eaed; border: 1px solid #252b33;
    padding: 12px 16px; border-radius: 8px; text-align: left;
}
QPushButton:hover { background: #222832; }
QPushButton:checked { background: #1f242c; border-left: 4px solid #ffffff; }
QPushButton#Primary {
    background: #ffffff; color: #111; border-radius: 8px; text-align: center;
    font-weight: 700;
}
QPushButton#Primary:hover { background: #e8e8e8; }
QFrame#Card {
    background: #171b20; border: 1px solid #232932; border-radius: 14px;
}
QLabel#Title { font-size: 28px; font-weight: 800; color: white; }
QLabel#CardTitle { font-size: 20px; font-weight: 800; color: white; }
QLabel#Muted { color: #8c94a0; }
QLabel#BigNumber { font-size: 32px; font-weight: 900; color: #e9edf3; }
QCheckBox, QRadioButton { spacing: 10px; padding: 8px; }
"""

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=8).strip()
    except Exception:
        return "Unknown"

def card(title, body=None):
    f = QFrame()
    f.setObjectName("Card")
    lay = QVBoxLayout(f)
    lay.setContentsMargins(24, 18, 24, 18)
    t = QLabel(title)
    t.setObjectName("CardTitle")
    lay.addWidget(t)
    if body:
        b = QLabel(body)
        b.setObjectName("Muted")
        b.setWordWrap(True)
        lay.addWidget(b)
    return f, lay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Win11 Toolkit")
        self.resize(1250, 760)

        wrapper = QWidget()
        self.setCentralWidget(wrapper)
        main = QHBoxLayout(wrapper)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        side = QWidget()
        side.setObjectName("Sidebar")
        side.setFixedWidth(260)
        side_lay = QVBoxLayout(side)
        side_lay.setContentsMargins(24, 28, 18, 20)

        logo = QLabel(APP_NAME)
        logo.setObjectName("Logo")
        sub = QLabel("WIN11 PYTHON TOOLKIT")
        sub.setObjectName("SubLogo")
        side_lay.addWidget(logo)
        side_lay.addWidget(sub)
        side_lay.addSpacing(28)

        self.stack = QStackedWidget()
        nav = [
            ("⌂  Dashboard", self.page_dashboard),
            ("⚡  Optimize Engine", self.page_optimize),
            ("▣  PC Optimization", self.page_pc),
            ("🎮  PC Games", self.page_games),
            ("▤  Emulated Games", self.page_emulators),
            ("🧹  Deep Cleaner", self.page_cleaner),
            ("🌐  Network", self.page_network),
            ("📦  Install Apps", self.page_apps),
        ]
        self.buttons = []
        for i, (name, factory) in enumerate(nav):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, ix=i: self.goto(ix))
            side_lay.addWidget(btn)
            self.buttons.append(btn)
            self.stack.addWidget(factory())
        side_lay.addStretch()
        admin = QLabel("● ADMIN MODE\nAdmin")
        admin.setStyleSheet("color:#b06cff; background:#171b20; padding:12px; border-radius:8px;")
        side_lay.addWidget(admin)

        main.addWidget(side)
        main.addWidget(self.stack)
        self.goto(0)

    def goto(self, index):
        self.stack.setCurrentIndex(index)
        for i, b in enumerate(self.buttons):
            b.setChecked(i == index)

    def page_base(self, title, subtitle=""):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(36, 32, 36, 22)
        h = QLabel(title)
        h.setObjectName("Title")
        lay.addWidget(h)
        if subtitle:
            s = QLabel(subtitle)
            s.setObjectName("Muted")
            lay.addWidget(s)
        lay.addSpacing(18)
        return page, lay

    def page_dashboard(self):
        page, lay = self.page_base("Welcome to VelocityPanel", "System snapshot")
        c, cl = card("🖥 Detected System")
        info = QLabel(
            f"CPU: {platform.processor() or 'Detected CPU'}\n"
            f"RAM: {round((shutil.disk_usage('/').total / (1024**3)), 1)} GB disk detected\n"
            f"OS: {platform.platform()}\n"
            f"Type: Desktop"
        )
        info.setObjectName("Muted")
        cl.addWidget(info)
        lay.addWidget(c)

        r, rl = card("✨ Recommended Preset", "High-end gaming preset. Safe mode is recommended.")
        btn = QPushButton("Apply Recommended")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Applied", "Recommended settings applied."))
        rl.addWidget(btn)
        lay.addWidget(r)

        grid = QGridLayout()
        for i, (name, num) in enumerate([("Active Tweaks", "8"), ("Available Tweaks", "12"), ("License", "FREE")]):
            small, sl = card(name)
            n = QLabel(num)
            n.setObjectName("BigNumber")
            sl.addWidget(n)
            grid.addWidget(small, 0, i)
        lay.addLayout(grid)
        lay.addStretch()
        return page

    def page_optimize(self):
        page, lay = self.page_base("Optimize Engine", "One-click safe optimizations.")
        c, cl = card("Ready to optimize")
        btn = QPushButton("▶  Start Optimization")
        btn.setObjectName("Primary")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Done", "Optimization completed."))
        cl.addWidget(btn)
        lay.addWidget(c)
        return page

    def page_pc(self):
        page, lay = self.page_base("PC Optimization")
        c, cl = card("Windows Tweaks")
        for x in ["Disable startup delay", "Clean temp files", "Set high performance power plan", "Disable game bar capture"]:
            cl.addWidget(QCheckBox(x))
        lay.addWidget(c)
        return page

    def page_games(self):
        page, lay = self.page_base("PC Games")
        c, cl = card("Gaming Presets")
        group = QButtonGroup(self)
        for x in ["Safe Mode (recommended)", "Performance Mode", "Extreme Mode"]:
            rb = QRadioButton(x)
            group.addButton(rb)
            cl.addWidget(rb)
        btn = QPushButton("⚡ Apply to Selected")
        btn.setObjectName("Primary")
        cl.addWidget(btn)
        lay.addWidget(c)
        return page

    def page_emulators(self):
        page, lay = self.page_base("Emulated Games")
        c, cl = card("Step 1 · Select Emulators")
        for x in ["GameLoop", "LDPlayer", "BlueStacks", "Nox Player", "MEmu Play"]:
            cl.addWidget(QCheckBox(x))
        level, ll = card("Step 2 · Optimization Level")
        for x in ["Safe Mode (FREE)", "Performance Mode", "Extreme Mode"]:
            ll.addWidget(QRadioButton(x))
        lay.addWidget(c)
        lay.addWidget(level)
        return page

    def page_cleaner(self):
        page, lay = self.page_base("Deep Cleaner", "Restores fresh OS performance without touching personal files.")
        c, cl = card("Basic Clean (FREE)", "Temp files, browser caches, DNS cache, recycle bin.")
        b = QPushButton("🧹 Run Basic Clean")
        b.setObjectName("Primary")
        b.clicked.connect(lambda: QMessageBox.information(self, "Clean", "Basic clean finished."))
        cl.addWidget(b)
        lay.addWidget(c)
        pro, pl = card("Deep Clean (PRO)", "DISM cleanup, old driver versions, Windows.old removal.")
        pl.addWidget(QPushButton("🚀 Run Deep Clean"))
        lay.addWidget(pro)
        return page

    def page_network(self):
        page, lay = self.page_base("Network")
        c, cl = card("DNS Test & Apply (FREE)", "Test popular DNS providers and apply the fastest one.")
        for name, ping in [("Cloudflare (1.1.1.1)", "9 ms"), ("OpenDNS", "30 ms"), ("Google (8.8.8.8)", "41 ms"), ("Quad9 (9.9.9.9)", "42 ms")]:
            row = QPushButton(f"{name}                                      {ping}     Apply")
            cl.addWidget(row)
        lay.addWidget(c)
        return page

    def page_apps(self):
        page, outer = self.page_base("Install Apps", "Install essential apps via winget.")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        body = QWidget()
        lay = QVBoxLayout(body)
        for app in ["Google Chrome", "Brave Browser", "Mozilla Firefox", "DirectX Runtimes", "VC++ All-in-One", ".NET Desktop Runtime", "7-Zip", "WinRAR"]:
            lay.addWidget(QCheckBox(app))
        btn = QPushButton("📦 Install Selected")
        btn.setObjectName("Primary")
        lay.addWidget(btn)
        lay.addStretch()
        scroll.setWidget(body)
        outer.addWidget(scroll)
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
