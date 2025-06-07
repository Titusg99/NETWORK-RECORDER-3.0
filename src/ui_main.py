import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QTextEdit, QFormLayout, QStackedWidget, QListWidgetItem, QComboBox, QDateEdit, QMessageBox, QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QStyle, QFileDialog, QInputDialog, QColorDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QCompleter, QToolButton, QStackedLayout, QFrame
)
from PyQt5.QtCore import Qt, QDate, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QPalette, QColor, QKeySequence, QDrag, QIcon
from PyQt5.QtWidgets import QShortcut
from models import Contact, Interaction, DEFAULT_FOLLOWUP_INTERVALS, save_contacts, load_contacts
from datetime import datetime, timedelta
from collections import Counter
import csv
import shutil

CONTACTS_PATH = os.path.join(os.path.dirname(__file__), '../data/contacts.json')

class ContactForm(QWidget):
    def __init__(self, on_save, parent=None):
        super().__init__(parent)
        self.on_save = on_save
        self.init_ui()
        self.setStyleSheet('QWidget { background: #fff; border-radius: 16px; font-size: 16px; padding: 24px; } QLineEdit, QTextEdit { border: 1px solid #e5e7eb; border-radius: 8px; padding: 6px; font-size: 15px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 8px 20px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')

    def init_ui(self):
        self.layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.company_input = QLineEdit()
        self.role_input = QLineEdit()
        self.tags_input = QLineEdit()
        self.linkedin_input = QLineEdit()
        self.website_input = QLineEdit()
        self.how_met_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.location_input = QLineEdit()
        self.birthday_input = QLineEdit()
        self.layout.addRow("Name*", self.name_input)
        self.layout.addRow("Email", self.email_input)
        self.layout.addRow("Phone", self.phone_input)
        self.layout.addRow("Company", self.company_input)
        self.layout.addRow("Role", self.role_input)
        self.layout.addRow("Tags (comma-separated)", self.tags_input)
        self.layout.addRow("LinkedIn", self.linkedin_input)
        self.layout.addRow("Website", self.website_input)
        self.layout.addRow("How Met", self.how_met_input)
        self.layout.addRow("Notes", self.notes_input)
        self.layout.addRow("Location", self.location_input)
        self.layout.addRow("Birthday", self.birthday_input)
        self.save_btn = QPushButton("Save Contact")
        self.save_btn.clicked.connect(self.save_contact)
        self.layout.addRow(self.save_btn)
        self.setLayout(self.layout)

        # Build auto-complete lists from existing contacts
        contacts = load_contacts(CONTACTS_PATH)
        companies = sorted(set(c.company for c in contacts if c.company))
        tags = sorted(set(t for c in contacts for t in c.tags))
        roles = sorted(set(c.role for c in contacts if c.role))
        locations = sorted(set(c.location for c in contacts if c.location))
        self.company_input.setCompleter(QCompleter(companies))
        self.tags_input.setCompleter(QCompleter(tags))
        self.role_input.setCompleter(QCompleter(roles))
        self.location_input.setCompleter(QCompleter(locations))

    def save_contact(self):
        print('Save contact called')
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Name is required.")
            return
        contact = Contact(
            name=name,
            email=self.email_input.text().strip() or None,
            phone=self.phone_input.text().strip() or None,
            company=self.company_input.text().strip() or None,
            role=self.role_input.text().strip() or None,
            tags=[t.strip() for t in self.tags_input.text().split(",") if t.strip()],
            linkedin=self.linkedin_input.text().strip() or None,
            website=self.website_input.text().strip() or None,
            how_met=self.how_met_input.text().strip() or None,
            notes=self.notes_input.toPlainText().strip() or None,
            location=self.location_input.text().strip() or None,
            birthday=self.birthday_input.text().strip() or None,
        )
        contact.calculate_next_followup()
        self.on_save(contact)
        self.clear_form()

    def clear_form(self):
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.company_input.clear()
        self.role_input.clear()
        self.tags_input.clear()
        self.linkedin_input.clear()
        self.website_input.clear()
        self.how_met_input.clear()
        self.notes_input.clear()
        self.location_input.clear()
        self.birthday_input.clear()

    def update_completers(self, contacts):
        companies = sorted(set(c.company for c in contacts if c.company))
        tags = sorted(set(t for c in contacts for t in c.tags))
        roles = sorted(set(c.role for c in contacts if c.role))
        locations = sorted(set(c.location for c in contacts if c.location))
        self.company_input.setCompleter(QCompleter(companies))
        self.tags_input.setCompleter(QCompleter(tags))
        self.role_input.setCompleter(QCompleter(roles))
        self.location_input.setCompleter(QCompleter(locations))

class Dashboard(QWidget):
    def __init__(self, contacts):
        super().__init__()
        self.contacts = contacts
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Stats
        total_contacts = len(self.contacts)
        today = datetime.now().date()
        due_today = [c for c in self.contacts if c.next_followup and c.next_followup.date() == today]
        overdue = [c for c in self.contacts if c.next_followup and c.next_followup.date() < today]
        recent = sorted(self.contacts, key=lambda c: c.last_interaction or datetime.min, reverse=True)[:5]
        layout.addWidget(QLabel("<h2>Progress Dashboard</h2>"))
        stats = QLabel(f"<b>Total Contacts:</b> {total_contacts} | <b>Due Today:</b> {len(due_today)} | <b>Overdue:</b> {len(overdue)}")
        layout.addWidget(stats)
        layout.addWidget(QLabel("<h3>Activity Graph (Coming Soon)</h3>"))
        layout.addWidget(QLabel("[Graph Placeholder]"))
        layout.addWidget(QLabel("<h3>Recently Added/Active</h3>"))
        for c in recent:
            label = QLabel(f"<b>{c.name}</b> - Last: {c.last_interaction.strftime('%Y-%m-%d') if c.last_interaction else 'N/A'}")
            layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)

class FilterBar(QWidget):
    def __init__(self, tags, on_filter):
        super().__init__()
        self.on_filter = on_filter
        self.init_ui(tags)

    def init_ui(self, tags):
        layout = QHBoxLayout()
        self.tag_filter = QComboBox()
        self.tag_filter.addItem("All Tags")
        for tag in sorted(tags):
            self.tag_filter.addItem(tag)
        self.tag_filter.currentIndexChanged.connect(self.apply_filter)
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Statuses", "Due", "Overdue", "Upcoming", "None"])
        self.status_filter.currentIndexChanged.connect(self.apply_filter)
        self.company_filter = QLineEdit()
        self.company_filter.setPlaceholderText("Filter by company...")
        self.company_filter.textChanged.connect(self.apply_filter)
        layout.addWidget(QLabel("Tag:"))
        layout.addWidget(self.tag_filter)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_filter)
        layout.addWidget(self.company_filter)
        layout.addStretch()
        self.setLayout(layout)

    def apply_filter(self):
        tag = self.tag_filter.currentText()
        status = self.status_filter.currentText()
        company = self.company_filter.text().strip()
        self.on_filter(tag, status, company)

class InteractionDialog(QDialog):
    def __init__(self, on_save, parent=None):
        super().__init__(parent)
        self.on_save = on_save
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle("Log Interaction")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        self.date_input = QDateEdit(QDate.currentDate())
        self.type_input = QComboBox()
        self.type_input.addItems(["Meeting", "Call", "Email", "Other"])
        self.summary_input = QTextEdit()
        layout.addRow("Date", self.date_input)
        layout.addRow("Type", self.type_input)
        layout.addRow("Summary", self.summary_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        self.setLayout(layout)

    def save(self):
        interaction = Interaction(
            date=self.date_input.date().toPyDate(),
            type=self.type_input.currentText(),
            summary=self.summary_input.toPlainText().strip()
        )
        self.on_save(interaction)
        self.accept()

class SettingsDialog(QDialog):
    def __init__(self, intervals, on_save, parent=None):
        super().__init__(parent)
        self.intervals = intervals.copy()
        self.on_save = on_save
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle("Settings")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        self.inputs = {}
        for tag in self.intervals:
            inp = QLineEdit(str(self.intervals[tag]))
            layout.addRow(f"{tag} (days)", inp)
            self.inputs[tag] = inp
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        self.setLayout(layout)

    def save(self):
        for tag, inp in self.inputs.items():
            try:
                self.intervals[tag] = int(inp.text())
            except ValueError:
                pass
        self.on_save(self.intervals)
        self.accept()

class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle("Welcome to Network Tracker!")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Welcome to Network Tracker!</h2>"))
        layout.addWidget(QLabel("<b>Quick Start Tips:</b>"))
        layout.addWidget(QLabel("- Add your first contact using the 'Add Contact' button or Ctrl+N."))
        layout.addWidget(QLabel("- Log interactions to keep your network fresh."))
        layout.addWidget(QLabel("- Use the Dashboard to track your progress and follow-ups."))
        layout.addWidget(QLabel("- Import contacts from CSV or export your data anytime."))
        layout.addWidget(QLabel("- Explore settings and dark mode for a personalized experience."))
        layout.addWidget(QLabel("- Use keyboard shortcuts for speed!"))
        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)
        self.setLayout(layout)

class DocumentCenterDialog(QDialog):
    def __init__(self, contact_name, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle(f"Documents for {contact_name}")
        self.contact_name = contact_name
        self.docs_dir = os.path.join(os.path.dirname(__file__), '../data/docs', contact_name.replace(' ', '_'))
        os.makedirs(self.docs_dir, exist_ok=True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.refresh_files()
        layout.addWidget(self.file_list)
        btns = QHBoxLayout()
        upload_btn = QPushButton("Upload")
        open_btn = QPushButton("Open")
        delete_btn = QPushButton("Delete")
        btns.addWidget(upload_btn)
        btns.addWidget(open_btn)
        btns.addWidget(delete_btn)
        layout.addLayout(btns)
        upload_btn.clicked.connect(self.upload_file)
        open_btn.clicked.connect(self.open_file)
        delete_btn.clicked.connect(self.delete_file)
        self.setLayout(layout)

    def refresh_files(self):
        self.file_list.clear()
        for fname in os.listdir(self.docs_dir):
            self.file_list.addItem(fname)

    def upload_file(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Upload Document", "", "Documents (*.pdf *.docx *.txt)")
            if not path:
                return
            shutil.copy(path, self.docs_dir)
            self.refresh_files()
        except Exception as e:
            QMessageBox.warning(self, "Upload Failed", f"Error: {e}")

    def open_file(self):
        try:
            item = self.file_list.currentItem()
            if not item:
                return
            os.system(f'open "{os.path.join(self.docs_dir, item.text())}"')
        except Exception as e:
            QMessageBox.warning(self, "Open Failed", f"Error: {e}")

    def delete_file(self):
        try:
            item = self.file_list.currentItem()
            if not item:
                return
            os.remove(os.path.join(self.docs_dir, item.text()))
            self.refresh_files()
        except Exception as e:
            QMessageBox.warning(self, "Delete Failed", f"Error: {e}")

class NetworkMapDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle("Network Map (Coming Soon)")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Network Map</h2>"))
        layout.addWidget(QLabel("A visualization of your network will appear here in a future update!"))
        btns = QDialogButtonBox(QDialogButtonBox.Ok)
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)
        self.setLayout(layout)

class TagManagerDialog(QDialog):
    def __init__(self, tag_colors, on_save, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QDialog { border-radius: 16px; background: #fff; font-size: 15px; padding: 18px; } QPushButton { border-radius: 12px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        self.setWindowTitle("Manage Tags")
        self.tag_colors = tag_colors.copy()
        self.on_save = on_save
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.list = QListWidget()
        for tag, color in self.tag_colors.items():
            item = QListWidgetItem(tag)
            item.setBackground(color)
            self.list.addItem(item)
        layout.addWidget(self.list)
        btns = QHBoxLayout()
        add_btn = QPushButton("Add Tag")
        edit_btn = QPushButton("Edit Color")
        del_btn = QPushButton("Delete Tag")
        btns.addWidget(add_btn)
        btns.addWidget(edit_btn)
        btns.addWidget(del_btn)
        layout.addLayout(btns)
        add_btn.clicked.connect(self.add_tag)
        edit_btn.clicked.connect(self.edit_color)
        del_btn.clicked.connect(self.delete_tag)
        save_btn = QDialogButtonBox(QDialogButtonBox.Ok)
        save_btn.accepted.connect(self.save)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def add_tag(self):
        tag, ok = QInputDialog.getText(self, "Add Tag", "Tag name:")
        if ok and tag:
            color = QColorDialog.getColor()
            if color.isValid():
                self.tag_colors[tag] = color
                item = QListWidgetItem(tag)
                item.setBackground(color)
                self.list.addItem(item)

    def edit_color(self):
        item = self.list.currentItem()
        if not item:
            return
        color = QColorDialog.getColor()
        if color.isValid():
            self.tag_colors[item.text()] = color
            item.setBackground(color)

    def delete_tag(self):
        item = self.list.currentItem()
        if not item:
            return
        tag = item.text()
        del self.tag_colors[tag]
        self.list.takeItem(self.list.row(item))

    def save(self):
        self.on_save(self.tag_colors)
        self.accept()

class DraggableCard(QFrame):
    def __init__(self, contact, status, color, parent=None):
        super().__init__(parent)
        self.contact = contact
        self.status = status
        self.setAcceptDrops(True)
        self.setStyleSheet(f'background: #fff; border-radius: 10px; margin: 6px; padding: 8px; border: 2px solid {color};')
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'<b>{contact.name}</b>'))
        layout.addWidget(QLabel(f'{contact.company or ""}'))
        layout.addWidget(QLabel(f'<span style="color:#888">{", ".join(contact.tags)}</span>'))
        self.setLayout(layout)

    def mousePressEvent(self, event):
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.contact.name)
        drag.setMimeData(mime)
        drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Not used on card, handled by column
        pass

class DropArea(QVBoxLayout):
    def __init__(self, status, color, parent, mainwindow):
        super().__init__()
        self.status = status
        self.color = color
        self.parent = parent
        self.mainwindow = mainwindow
        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.widget = QWidget()
        self.widget.setAcceptDrops(True)
        self.widget.dragEnterEvent = self.dragEnterEvent
        self.widget.dropEvent = self.dropEvent
        self.addWidget(self.widget)
        self.cards = QVBoxLayout()
        self.widget.setLayout(self.cards)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        name = event.mimeData().text()
        contact = next((c for c in self.mainwindow.contacts if c.name == name), None)
        if contact:
            # Update follow-up date based on column
            today = datetime.now().date()
            if self.status == 'Overdue':
                contact.next_followup = datetime.combine(today, datetime.min.time()) - timedelta(days=1)
            elif self.status == 'Due':
                contact.next_followup = datetime.combine(today, datetime.min.time())
            elif self.status == 'Upcoming':
                contact.next_followup = datetime.combine(today, datetime.min.time()) + timedelta(days=3)
            else:
                contact.next_followup = datetime.combine(today, datetime.min.time()) + timedelta(days=30)
            self.mainwindow.save_all()
            self.mainwindow.kanban_view = self.mainwindow.build_kanban_view()
            self.mainwindow.views_stack.insertWidget(1, self.mainwindow.kanban_view)
            self.mainwindow.views_stack.setCurrentIndex(1)
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Tracker App")
        self.intervals = DEFAULT_FOLLOWUP_INTERVALS.copy()
        self.contacts = load_contacts(CONTACTS_PATH)
        self.dark_mode = False
        self.current_tag_filter = "All Tags"
        self.current_status_filter = "All Statuses"
        self.current_company_filter = ""
        self.tag_colors = self.generate_tag_colors()
        self.history = []
        self.future = []
        self.init_ui()
        self.init_shortcuts()

    def generate_tag_colors(self):
        import random
        color_map = {}
        tags = set(t for c in self.contacts for t in c.tags)
        for tag in tags:
            color_map[tag] = QColor(random.randint(100,255), random.randint(100,255), random.randint(100,255))
        return color_map

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        # Sidebar
        sidebar = QVBoxLayout()
        style = QApplication.style()
        # Networking section
        sidebar.addWidget(QLabel('<b style="color:#888;">NETWORKING</b>'))
        self.dashboard_btn = QPushButton(style.standardIcon(QStyle.SP_ComputerIcon), "Dashboard")
        self.dashboard_btn.setToolTip("View your networking progress dashboard")
        self.contacts_btn = QPushButton(style.standardIcon(QStyle.SP_DirHomeIcon), "Contacts")
        self.contacts_btn.setToolTip("View and manage your contacts")
        self.add_contact_btn = QPushButton(style.standardIcon(QStyle.SP_FileDialogNewFolder), "Add Contact")
        self.add_contact_btn.setToolTip("Add a new contact")
        sidebar.addWidget(self.dashboard_btn)
        sidebar.addWidget(self.contacts_btn)
        sidebar.addWidget(self.add_contact_btn)
        # Tools section
        sidebar.addSpacing(10)
        sidebar.addWidget(QLabel('<b style="color:#888;">TOOLS</b>'))
        self.import_btn = QPushButton(style.standardIcon(QStyle.SP_DialogOpenButton), "Import")
        self.import_btn.setToolTip("Import contacts from CSV")
        self.export_btn = QPushButton(style.standardIcon(QStyle.SP_DialogSaveButton), "Export")
        self.export_btn.setToolTip("Export contacts to CSV")
        self.onboarding_btn = QPushButton(style.standardIcon(QStyle.SP_MessageBoxInformation), "Tips")
        self.onboarding_btn.setToolTip("Show onboarding tips and quick start guide")
        self.undo_btn = QPushButton(style.standardIcon(QStyle.SP_ArrowBack), "Undo")
        self.undo_btn.setToolTip("Undo last change (Ctrl+Z)")
        self.redo_btn = QPushButton(style.standardIcon(QStyle.SP_ArrowForward), "Redo")
        self.redo_btn.setToolTip("Redo last undone change (Ctrl+Y)")
        self.network_map_btn = QPushButton(style.standardIcon(QStyle.SP_BrowserReload), "Network Map")
        self.network_map_btn.setToolTip("Visualize your network (coming soon)")
        self.tag_manager_btn = QPushButton(style.standardIcon(QStyle.SP_DirIcon), "Manage Tags")
        self.tag_manager_btn.setToolTip("Add, edit, or delete tags and assign colors")
        sidebar.addWidget(self.import_btn)
        sidebar.addWidget(self.export_btn)
        sidebar.addWidget(self.onboarding_btn)
        sidebar.addWidget(self.undo_btn)
        sidebar.addWidget(self.redo_btn)
        sidebar.addWidget(self.network_map_btn)
        sidebar.addWidget(self.tag_manager_btn)
        # Settings section
        sidebar.addSpacing(10)
        sidebar.addWidget(QLabel('<b style="color:#888;">SETTINGS</b>'))
        self.dark_mode_btn = QPushButton(style.standardIcon(QStyle.SP_DialogResetButton), "Toggle Dark Mode")
        self.dark_mode_btn.setToolTip("Switch between light and dark mode")
        self.settings_btn = QPushButton(style.standardIcon(QStyle.SP_FileDialogDetailedView), "Settings")
        self.settings_btn.setToolTip("Configure app settings")
        sidebar.addWidget(self.dark_mode_btn)
        sidebar.addWidget(self.settings_btn)
        # Profile section
        profile_box = QHBoxLayout()
        avatar = QLabel()
        avatar.setFixedSize(36,36)
        avatar.setStyleSheet("border-radius:18px; background:#bbb; margin-right:8px;")
        profile_box.addWidget(avatar)
        profile_info = QVBoxLayout()
        profile_info.addWidget(QLabel('<b>Titus Grimsley</b>'))
        profile_info.addWidget(QLabel('<span style="color:#888;">titus@email.com</span>'))
        profile_box.addLayout(profile_info)
        profile_box.addStretch()
        sidebar.addLayout(profile_box)
        sidebar.addStretch()
        # Main area
        self.stack = QStackedWidget()
        # Dashboard view
        self.dashboard = Dashboard(self.contacts)
        self.stack.addWidget(self.dashboard)
        # Contact table view
        contact_table_container = QWidget()
        vbox = QVBoxLayout()
        # Header bar above contact table
        header_bar = QHBoxLayout()
        self.view_switcher = QComboBox()
        self.view_switcher.addItems(['Timeline', 'Card/Grid'])
        self.view_switcher.currentIndexChanged.connect(self.switch_view)
        header_bar.insertWidget(0, self.view_switcher)
        # Stacked layout for views
        self.views_stack = QStackedLayout()
        # Timeline view
        self.timeline_view = self.build_timeline_view()
        self.views_stack.addWidget(self.timeline_view)
        # Card/Grid view
        self.card_grid_view = self.build_card_grid_view()
        self.views_stack.addWidget(self.card_grid_view)
        # Replace vbox with views_stack
        vbox.addLayout(self.views_stack)
        # Remove direct vbox.addWidget(self.contact_table) and vbox.addWidget(contact_table_container)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search contacts...")
        self.search_input.setToolTip("Type to search contacts by name, company, or tag")
        self.search_input.textChanged.connect(self.refresh_contact_table)
        vbox.addWidget(self.search_input)
        self.sort_dropdown = QComboBox()
        self.sort_dropdown.addItems(['Sort: Name', 'Sort: Last Interaction', 'Sort: Next Follow-Up'])
        self.sort_dropdown.currentIndexChanged.connect(self.refresh_contact_table)
        header_bar.addWidget(self.sort_dropdown)
        header_bar.addSpacing(10)
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(['Filter: All', 'Filter: Overdue', 'Filter: Due', 'Filter: Upcoming'])
        self.filter_dropdown.currentIndexChanged.connect(self.refresh_contact_table)
        header_bar.addWidget(self.filter_dropdown)
        header_bar.addStretch()
        add_btn = QPushButton('+ Add Contact')
        add_btn.setStyleSheet('QPushButton { border-radius: 16px; background: #52c41a; color: white; padding: 6px 18px; font-weight: bold; } QPushButton:hover { background: #389e0d; }')
        add_btn.clicked.connect(self.show_add_contact_form)
        header_bar.addWidget(add_btn)
        vbox.insertLayout(0, header_bar)
        self.contact_table = QTableWidget()
        self.contact_table.setColumnCount(8)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Tags", "Company", "Role", "Last Interaction", "Next Follow-Up", "Status", "Actions"])
        self.contact_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.contact_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contact_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contact_table.verticalHeader().setVisible(False)
        self.contact_table.cellDoubleClicked.connect(self.handle_table_double_click)
        vbox.addWidget(self.contact_table)
        contact_table_container.setLayout(vbox)
        self.stack.addWidget(contact_table_container)
        # Add contact form
        self.contact_form = ContactForm(self.add_contact)
        self.stack.addWidget(self.contact_form)
        # Connect sidebar
        self.dashboard_btn.clicked.connect(lambda: self.show_dashboard())
        self.contacts_btn.clicked.connect(lambda: self.show_contacts())
        self.add_contact_btn.clicked.connect(self.show_add_contact_form)
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        self.settings_btn.clicked.connect(self.open_settings)
        self.import_btn.clicked.connect(self.import_contacts)
        self.export_btn.clicked.connect(self.export_contacts)
        self.onboarding_btn.clicked.connect(self.show_onboarding)
        self.undo_btn.clicked.connect(self.undo)
        self.redo_btn.clicked.connect(self.redo)
        self.network_map_btn.clicked.connect(self.show_network_map)
        self.tag_manager_btn.clicked.connect(self.open_tag_manager)
        # Layout
        # Apply modern style to sidebar and table
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setStyleSheet('''
            QWidget { background: #23272f; border-radius: 16px; }
            QPushButton { color: #fff; background: transparent; border: none; text-align: left; padding: 8px 16px; font-size: 15px; }
            QPushButton:hover { background: #2c313c; }
            QLabel { color: #bbb; font-size: 13px; }
        ''')
        # Table area styling
        contact_table_container.setStyleSheet('''
            QWidget { background: #f7f8fa; border-radius: 16px; }
            QTableWidget { background: #fff; border-radius: 12px; font-size: 15px; }
            QHeaderView::section { background: #f0f2f5; border: none; font-weight: bold; font-size: 14px; }
        ''')
        self.contact_table.setAlternatingRowColors(True)
        self.contact_table.setStyleSheet('''
            QTableWidget::item:selected { background: #e6f7ff; }
            QTableWidget::item:hover { background: #f0f5ff; }
            QTableWidget { alternate-background-color: #fafbfc; }
        ''')
        # Add drop shadow effect (optional, for PyQt5)
        try:
            from PyQt5.QtWidgets import QGraphicsDropShadowEffect
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(18)
            shadow.setOffset(0, 2)
            shadow.setColor(QColor(0,0,0,60))
            contact_table_container.setGraphicsEffect(shadow)
            sidebar_widget.setGraphicsEffect(shadow)
        except Exception:
            pass
        # Replace sidebar in layout
        main_layout.insertWidget(0, sidebar_widget)
        # Remove old sidebar if present
        if main_layout.count() > 2:
            main_layout.takeAt(1)
        # Layout
        main_layout.addWidget(self.stack, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show_dashboard()

        # Floating '+' quick-add button
        self.fab = QToolButton(self)
        self.fab.setText('+')
        self.fab.setStyleSheet('''
            QToolButton {
                background: #52c41a;
                color: white;
                border-radius: 24px;
                font-size: 32px;
                padding: 0px;
                width: 48px;
                height: 48px;
                position: absolute;
            }
            QToolButton:hover { background: #389e0d; }
        ''')
        self.fab.setToolTip('Quick Add Contact')
        self.fab.clicked.connect(self.show_add_contact_form)
        self.fab.raise_()
        self.fab.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Position floating button at bottom right
        if hasattr(self, 'fab'):
            self.fab.move(self.width() - 72, self.height() - 72)

    def show_dashboard(self):
        if not self.contacts:
            self.show_onboarding()
        self.dashboard = Dashboard(self.contacts)
        self.stack.insertWidget(0, self.dashboard)
        self.stack.setCurrentIndex(0)

    def show_contacts(self):
        self.refresh_contact_table()
        self.stack.setCurrentIndex(1)

    def add_contact(self, contact):
        self.push_history()
        contact.calculate_next_followup(self.intervals)
        self.contacts.append(contact)
        self.contact_form.update_completers(self.contacts)
        self.save_all()
        self.refresh_contact_table()
        self.stack.setCurrentIndex(1)
        self.contact_form.clear_form()

    def handle_tab_change(self, idx):
        if idx == 0:
            self.current_tag_filter = 'All Tags'
        else:
            self.current_tag_filter = self.tabs.currentText()
        self.refresh_contact_table()

    def refresh_contact_table(self):
        # ...
        # Add sorting and filter logic
        sort_by = self.sort_dropdown.currentIndex() if hasattr(self, 'sort_dropdown') else 0
        filter_by = self.filter_dropdown.currentText() if hasattr(self, 'filter_dropdown') else 'Filter: All'
        contacts = self.contacts[:]
        # Filter by tab/tag
        if self.current_tag_filter != 'All Tags':
            contacts = [c for c in contacts if self.current_tag_filter in c.tags]
        # Filter by status
        today = datetime.now().date()
        if filter_by == 'Filter: Overdue':
            contacts = [c for c in contacts if c.next_followup and (c.next_followup.date() - today).days < 0]
        elif filter_by == 'Filter: Due':
            contacts = [c for c in contacts if c.next_followup and (c.next_followup.date() - today).days == 0]
        elif filter_by == 'Filter: Upcoming':
            contacts = [c for c in contacts if c.next_followup and 0 < (c.next_followup.date() - today).days <= 7]
        # Sort
        if sort_by == 0:
            contacts.sort(key=lambda c: c.name.lower())
        elif sort_by == 1:
            contacts.sort(key=lambda c: c.last_interaction or datetime.min, reverse=True)
        elif sort_by == 2:
            contacts.sort(key=lambda c: c.next_followup or datetime.max)
        self.contact_table.setRowCount(0)
        query = self.search_input.text().lower()
        for row, contact in enumerate(contacts):
            # Search filter
            if query and not (query in contact.name.lower() or (contact.company and query in contact.company.lower()) or any(query in t.lower() for t in contact.tags)):
                continue
            # Tag filter
            if self.current_tag_filter != "All Tags" and self.current_tag_filter not in contact.tags:
                continue
            # Status filter
            status = "None"
            if contact.next_followup:
                days = (contact.next_followup.date() - today).days
                if days < 0:
                    status = "Overdue"
                elif days == 0:
                    status = "Due"
                elif days <= 7:
                    status = "Upcoming"
                else:
                    status = "None"
            if self.current_status_filter != "All Statuses" and status != self.current_status_filter:
                continue
            # Company filter
            if self.current_company_filter and (not contact.company or self.current_company_filter.lower() not in contact.company.lower()):
                continue
            self.contact_table.insertRow(row)
            # Name
            self.contact_table.setItem(row, 0, QTableWidgetItem(contact.name))
            # Tags (badges)
            tag_widget = QWidget()
            tag_layout = QHBoxLayout()
            tag_layout.setContentsMargins(0,0,0,0)
            for tag in contact.tags:
                tag_label = QLabel(tag)
                tag_label.setStyleSheet(f"background-color: {self.tag_colors.get(tag, QColor(200,200,200)).name()}; color: #222; border-radius: 6px; padding: 2px 6px; margin-right: 2px;")
                tag_layout.addWidget(tag_label)
            tag_layout.addStretch()
            tag_widget.setLayout(tag_layout)
            self.contact_table.setCellWidget(row, 1, tag_widget)
            # Company
            self.contact_table.setItem(row, 2, QTableWidgetItem(contact.company or ""))
            # Role
            self.contact_table.setItem(row, 3, QTableWidgetItem(contact.role or ""))
            # Last Interaction
            li = contact.last_interaction.strftime('%Y-%m-%d') if contact.last_interaction else ""
            self.contact_table.setItem(row, 4, QTableWidgetItem(li))
            # Next Follow-Up
            nf = contact.next_followup.strftime('%Y-%m-%d') if contact.next_followup else ""
            self.contact_table.setItem(row, 5, QTableWidgetItem(nf))
            # Status (badge)
            status_label = QLabel(status)
            color = {"Overdue": "#ff4d4f", "Due": "#faad14", "Upcoming": "#1890ff", "None": "#52c41a"}.get(status, "#d9d9d9")
            status_label.setStyleSheet(f"background-color: {color}; color: white; border-radius: 12px; padding: 2px 14px; font-weight: 500; font-size: 13px;")
            status_label.setAlignment(Qt.AlignCenter)
            self.contact_table.setCellWidget(row, 6, status_label)
            # Actions (edit, delete, docs)
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0,0,0,0)
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon.fromTheme('edit', QIcon(style.standardIcon(QStyle.SP_FileDialogContentsView))))
            edit_btn.setToolTip("Edit Contact")
            edit_btn.clicked.connect(lambda _, r=row: self.edit_contact(r))
            del_btn = QPushButton()
            del_btn.setIcon(QIcon.fromTheme('delete', QIcon(style.standardIcon(QStyle.SP_TrashIcon))))
            del_btn.setToolTip("Delete Contact")
            del_btn.clicked.connect(lambda _, r=row: self.delete_contact(r))
            docs_btn = QPushButton()
            docs_btn.setIcon(QIcon.fromTheme('document', QIcon(style.standardIcon(QStyle.SP_FileIcon))))
            docs_btn.setToolTip("Documents")
            docs_btn.clicked.connect(lambda _, r=row: self.show_docs_for_row(r))
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(del_btn)
            action_layout.addWidget(docs_btn)
            action_layout.addStretch()
            action_widget.setLayout(action_layout)
            self.contact_table.setCellWidget(row, 7, action_widget)

    def handle_table_double_click(self, row, col):
        self.show_contact_details_by_row(row)

    def show_contact_details_by_row(self, row):
        if row < 0 or row >= len(self.contacts):
            return
        contact = self.contacts[row]
        details = f"<b>Name:</b> {contact.name}<br>"
        if contact.company:
            details += f"<b>Company:</b> {contact.company}<br>"
        if contact.role:
            details += f"<b>Role:</b> {contact.role}<br>"
        if contact.email:
            details += f"<b>Email:</b> {contact.email}<br>"
        if contact.phone:
            details += f"<b>Phone:</b> {contact.phone}<br>"
        if contact.tags:
            details += f"<b>Tags:</b> {', '.join(contact.tags)}<br>"
        if contact.last_interaction:
            details += f"<b>Last Interaction:</b> {contact.last_interaction.strftime('%Y-%m-%d')}<br>"
        if contact.next_followup:
            details += f"<b>Next Follow-Up:</b> {contact.next_followup.strftime('%Y-%m-%d')}<br>"
        if contact.notes:
            details += f"<b>Notes:</b> {contact.notes}<br>"
        # Show interaction history
        if contact.interactions:
            details += "<hr><b>Interaction History:</b><br>"
            for i in sorted(contact.interactions, key=lambda x: x.date, reverse=True):
                details += f"{i.date.strftime('%Y-%m-%d')} - {i.type}: {i.summary}<br>"
        msg = QMessageBox(self)
        msg.setWindowTitle("Contact Details")
        msg.setTextFormat(Qt.RichText)
        msg.setText(details)
        log_btn = QPushButton("Log Interaction")
        edit_btn = QPushButton("Edit Contact")
        delete_btn = QPushButton("Delete Contact")
        docs_btn = QPushButton("Documents")
        msg.addButton(log_btn, QMessageBox.ActionRole)
        msg.addButton(edit_btn, QMessageBox.ActionRole)
        msg.addButton(delete_btn, QMessageBox.ActionRole)
        msg.addButton(docs_btn, QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Ok)
        def log_interaction():
            dlg = InteractionDialog(lambda interaction: self.log_interaction(contact, interaction))
            dlg.exec_()
        def edit_contact():
            self.edit_contact(row)
        def delete_contact():
            self.delete_contact(row)
        def show_docs():
            dlg = DocumentCenterDialog(contact.name, self)
            dlg.exec_()
        log_btn.clicked.connect(log_interaction)
        edit_btn.clicked.connect(edit_contact)
        delete_btn.clicked.connect(delete_contact)
        docs_btn.clicked.connect(show_docs)
        msg.exec_()

    def show_docs_for_row(self, row):
        if row < 0 or row >= len(self.contacts):
            return
        contact = self.contacts[row]
        dlg = DocumentCenterDialog(contact.name, self)
        dlg.exec_()

    def show_contact_details(self, item):
        idx = self.contact_table.row(item)
        contact = self.contacts[idx]
        details = f"<b>Name:</b> {contact.name}<br>"
        if contact.company:
            details += f"<b>Company:</b> {contact.company}<br>"
        if contact.role:
            details += f"<b>Role:</b> {contact.role}<br>"
        if contact.email:
            details += f"<b>Email:</b> {contact.email}<br>"
        if contact.phone:
            details += f"<b>Phone:</b> {contact.phone}<br>"
        if contact.tags:
            details += f"<b>Tags:</b> {', '.join(contact.tags)}<br>"
        if contact.last_interaction:
            details += f"<b>Last Interaction:</b> {contact.last_interaction.strftime('%Y-%m-%d')}<br>"
        if contact.next_followup:
            details += f"<b>Next Follow-Up:</b> {contact.next_followup.strftime('%Y-%m-%d')}<br>"
        if contact.notes:
            details += f"<b>Notes:</b> {contact.notes}<br>"
        # Show interaction history
        if contact.interactions:
            details += "<hr><b>Interaction History:</b><br>"
            for i in sorted(contact.interactions, key=lambda x: x.date, reverse=True):
                details += f"{i.date.strftime('%Y-%m-%d')} - {i.type}: {i.summary}<br>"
        msg = QMessageBox(self)
        msg.setWindowTitle("Contact Details")
        msg.setTextFormat(Qt.RichText)
        msg.setText(details)
        log_btn = QPushButton("Log Interaction")
        edit_btn = QPushButton("Edit Contact")
        delete_btn = QPushButton("Delete Contact")
        docs_btn = QPushButton("Documents")
        msg.addButton(log_btn, QMessageBox.ActionRole)
        msg.addButton(edit_btn, QMessageBox.ActionRole)
        msg.addButton(delete_btn, QMessageBox.ActionRole)
        msg.addButton(docs_btn, QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Ok)
        def log_interaction():
            dlg = InteractionDialog(lambda interaction: self.log_interaction(contact, interaction))
            dlg.exec_()
        def edit_contact():
            self.edit_contact(idx)
        def delete_contact():
            self.delete_contact(idx)
        def show_docs():
            dlg = DocumentCenterDialog(contact.name, self)
            dlg.exec_()
        log_btn.clicked.connect(log_interaction)
        edit_btn.clicked.connect(edit_contact)
        delete_btn.clicked.connect(delete_contact)
        docs_btn.clicked.connect(show_docs)
        msg.exec_()

    def edit_contact(self, idx):
        self.push_history()
        contact = self.contacts[idx]
        form = ContactForm(lambda c: self.save_edited_contact(idx, c))
        # Pre-fill form
        form.name_input.setText(contact.name)
        form.email_input.setText(contact.email or "")
        form.phone_input.setText(contact.phone or "")
        form.company_input.setText(contact.company or "")
        form.role_input.setText(contact.role or "")
        form.tags_input.setText(", ".join(contact.tags))
        form.linkedin_input.setText(contact.linkedin or "")
        form.website_input.setText(contact.website or "")
        form.how_met_input.setText(contact.how_met or "")
        form.notes_input.setText(contact.notes or "")
        form.location_input.setText(contact.location or "")
        form.birthday_input.setText(contact.birthday or "")
        self.stack.addWidget(form)
        self.stack.setCurrentWidget(form)

    def save_edited_contact(self, idx, contact):
        self.push_history()
        contact.calculate_next_followup(self.intervals)
        self.contacts[idx] = contact
        self.save_all()
        self.refresh_contact_table()
        self.stack.setCurrentIndex(1)

    def delete_contact(self, idx):
        self.push_history()
        del self.contacts[idx]
        self.save_all()
        self.refresh_contact_table()
        self.stack.setCurrentIndex(1)

    def log_interaction(self, contact, interaction):
        self.push_history()
        contact.log_interaction(interaction, self.intervals)
        self.save_all()
        self.refresh_contact_table()
        self.show_dashboard()

    def open_settings(self):
        dlg = SettingsDialog(self.intervals, self.save_intervals)
        dlg.exec_()

    def save_intervals(self, intervals):
        self.push_history()
        self.intervals = intervals.copy()
        for c in self.contacts:
            c.calculate_next_followup(self.intervals)
        self.save_all()
        self.refresh_contact_table()
        self.show_dashboard()

    def save_all(self):
        save_contacts(self.contacts, CONTACTS_PATH)

    def toggle_dark_mode(self):
        self.push_history()
        self.dark_mode = not self.dark_mode
        palette = QPalette()
        if self.dark_mode:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette = QApplication.style().standardPalette()
        QApplication.setPalette(palette)

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, activated=lambda: self.stack.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+F"), self, activated=self.focus_search)
        QShortcut(QKeySequence("Ctrl+I"), self, activated=self.import_contacts)
        QShortcut(QKeySequence("Ctrl+E"), self, activated=self.export_contacts)
        QShortcut(QKeySequence("Ctrl+Z"), self, activated=self.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self, activated=self.redo)

    def focus_search(self):
        self.stack.setCurrentIndex(1)
        self.search_input.setFocus()

    def import_contacts(self):
        self.push_history()
        path, _ = QFileDialog.getOpenFileName(self, "Import Contacts", "", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    contact = Contact(
                        name=row['name'],
                        email=row.get('email'),
                        phone=row.get('phone'),
                        company=row.get('company'),
                        role=row.get('role'),
                        tags=[t.strip() for t in row.get('tags', '').split(',') if t.strip()],
                        linkedin=row.get('linkedin'),
                        website=row.get('website'),
                        how_met=row.get('how_met'),
                        notes=row.get('notes'),
                        location=row.get('location'),
                        birthday=row.get('birthday'),
                    )
                    contact.calculate_next_followup(self.intervals)
                    self.contacts.append(contact)
            self.save_all()
            self.refresh_contact_table()
            QMessageBox.information(self, "Import", "Contacts imported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Import Failed", f"Error: {e}")

    def export_contacts(self):
        self.push_history()
        path, _ = QFileDialog.getSaveFileName(self, "Export Contacts", "contacts.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, 'w', newline='') as csvfile:
                fieldnames = ['name', 'email', 'phone', 'company', 'role', 'tags', 'linkedin', 'website', 'how_met', 'notes', 'location', 'birthday']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for c in self.contacts:
                    writer.writerow({
                        'name': c.name,
                        'email': c.email,
                        'phone': c.phone,
                        'company': c.company,
                        'role': c.role,
                        'tags': ', '.join(c.tags),
                        'linkedin': c.linkedin,
                        'website': c.website,
                        'how_met': c.how_met,
                        'notes': c.notes,
                        'location': c.location,
                        'birthday': c.birthday,
                    })
            QMessageBox.information(self, "Export", "Contacts exported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"Error: {e}")

    def show_onboarding(self):
        dlg = OnboardingDialog(self)
        dlg.exec_()

    def push_history(self):
        import copy
        self.history.append(copy.deepcopy(self.contacts))
        if len(self.history) > 50:
            self.history.pop(0)
        self.future.clear()

    def undo(self):
        if not self.history:
            return
        self.future.append(self.contacts)
        self.contacts = self.history.pop()
        self.save_all()
        self.refresh_contact_table()

    def redo(self):
        if not self.future:
            return
        self.history.append(self.contacts)
        self.contacts = self.future.pop()
        self.save_all()
        self.refresh_contact_table()

    def show_network_map(self):
        dlg = NetworkMapDialog(self)
        dlg.exec_()

    def open_tag_manager(self):
        dlg = TagManagerDialog(self.tag_colors, self.save_tag_colors)
        dlg.exec_()

    def save_tag_colors(self, tag_colors):
        self.tag_colors = tag_colors.copy()
        self.filter_bar = FilterBar(sorted(self.tag_colors.keys()), self.apply_filters)
        self.refresh_contact_table()

    def switch_view(self, idx):
        self.views_stack.setCurrentIndex(idx)

    def build_timeline_view(self):
        timeline = QFrame()
        timeline.setStyleSheet('background: #f7f8fa; border-radius: 16px;')
        layout = QVBoxLayout()
        all_interactions = []
        for c in self.contacts:
            for i in c.interactions:
                all_interactions.append((i.date, c, i))
        all_interactions.sort(reverse=True)
        for date, c, i in all_interactions:
            card = QFrame()
            card.setStyleSheet('background: #fff; border-radius: 10px; margin: 6px; padding: 8px; border: 2px solid #d9d9d9;')
            card_layout = QVBoxLayout()
            card_layout.addWidget(QLabel(f'<b>{c.name}</b> ({c.company or ""})'))
            card_layout.addWidget(QLabel(f'<span style="color:#888">{i.date.strftime("%Y-%m-%d")}</span> - {i.type}: {i.summary}'))
            card.setLayout(card_layout)
            layout.addWidget(card)
        layout.addStretch()
        timeline.setLayout(layout)
        return timeline

    def build_card_grid_view(self):
        grid = QFrame()
        grid.setStyleSheet('background: #f7f8fa; border-radius: 16px;')
        layout = QHBoxLayout()
        col_count = 3
        cols = [QVBoxLayout() for _ in range(col_count)]
        for idx, c in enumerate(self.contacts):
            card = QFrame()
            card.setStyleSheet('background: #fff; border-radius: 12px; margin: 10px; padding: 12px; border: 2px solid #d9d9d9;')
            card_layout = QVBoxLayout()
            avatar = QLabel()
            avatar.setFixedSize(48,48)
            avatar.setStyleSheet('border-radius:24px; background:#bbb; margin-bottom:8px;')
            card_layout.addWidget(avatar)
            card_layout.addWidget(QLabel(f'<b>{c.name}</b>'))
            card_layout.addWidget(QLabel(f'{c.company or ""}'))
            tag_line = QLabel(f'<span style="color:#888">{", ".join(c.tags)}</span>')
            card_layout.addWidget(tag_line)
            card.setLayout(card_layout)
            cols[idx % col_count].addWidget(card)
        for col in cols:
            col.addStretch()
            layout.addLayout(col)
        grid.setLayout(layout)
        return grid

    def build_kanban_view(self):
        kanban = QFrame()
        kanban.setStyleSheet('background: #f7f8fa; border-radius: 16px;')
        layout = QHBoxLayout()
        columns = [
            ('Overdue', '#ff4d4f', lambda days: days < 0),
            ('Due', '#faad14', lambda days: days == 0),
            ('Upcoming', '#1890ff', lambda days: 0 < days <= 7),
            ('None', '#52c41a', lambda days: days > 7 or days is None),
        ]
        today = datetime.now().date()
        contacts_by_status = {k: [] for k, _, _ in columns}
        for c in self.contacts:
            days = None
            if c.next_followup:
                days = (c.next_followup.date() - today).days
            for status, _, cond in columns:
                if days is not None and cond(days):
                    contacts_by_status[status].append(c)
                    break
                elif days is None and status == 'None':
                    contacts_by_status[status].append(c)
        for status, color, _ in columns:
            col_widget = QWidget()
            col_widget.setAcceptDrops(True)
            col_widget.setStyleSheet('background: transparent;')
            col_layout = QVBoxLayout()
            header = QLabel(f'<b style="color:{color}">{status}</b>')
            header.setAlignment(Qt.AlignCenter)
            col_layout.addWidget(header)
            for c in contacts_by_status[status]:
                card = DraggableCard(c, status, color, self)
                col_layout.addWidget(card)
            col_layout.addStretch()
            col_widget.setLayout(col_layout)
            # Drag-and-drop events
            def make_drop_event(status):
                def dropEvent(event, status=status):
                    name = event.mimeData().text()
                    contact = next((c for c in self.contacts if c.name == name), None)
                    if contact:
                        if status == 'Overdue':
                            contact.next_followup = datetime.combine(today, datetime.min.time()) - timedelta(days=1)
                        elif status == 'Due':
                            contact.next_followup = datetime.combine(today, datetime.min.time())
                        elif status == 'Upcoming':
                            contact.next_followup = datetime.combine(today, datetime.min.time()) + timedelta(days=3)
                        else:
                            contact.next_followup = datetime.combine(today, datetime.min.time()) + timedelta(days=30)
                        self.save_all()
                        self.kanban_view = self.build_kanban_view()
                        self.views_stack.insertWidget(1, self.kanban_view)
                        self.views_stack.setCurrentIndex(1)
                    event.acceptProposedAction()
                return dropEvent
            col_widget.dragEnterEvent = lambda event: event.acceptProposedAction()
            col_widget.dropEvent = make_drop_event(status)
            layout.addWidget(col_widget)
        kanban.setLayout(layout)
        return kanban

    def show_add_contact_form(self):
        print('Showing add contact form')
        self.stack.setCurrentWidget(self.contact_form)
        self.contact_form.show()

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 