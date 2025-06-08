import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import json
import os
from datetime import datetime, timedelta

CONTACTS_FILE = "contacts.json"

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = []
        self.companies = []
        self.filtered_contacts = []
        self.selected_contact_index = None
        self.selected_company_index = None
        self.current_page = "dashboard"
        
        # Define relationship types and their follow-up rules
        self.RELATIONSHIP_TYPES = {
            "Passive Friendship": None,  # No reminders
            "Lead": {
                "stages": {
                    "First Outreach": 0,  # Immediate
                    "First Follow-up": 7,  # 7 days
                    "Second Follow-up": 7,  # 7 days after previous
                    "Third Follow-up": 7   # 7 days after previous (optional)
                }
            },
            "Professional Relationship": {
                "maintenance": 120,  # 120 days (4 months)
                "recurring": True  # This will keep recurring every 4 months
            }
        }
        
        self.JOB_TITLE_OPTIONS = [
            "Intern", "Analyst", "Associate", "Senior Associate", "Vice President", "VP", "Director", "Senior Director", "Executive Director", "Managing Director", "MD", "Partner", "Principal", "CEO", "CFO", "COO", "CTO", "CIO", "CMO", "Chairman", "President", "Owner", "Founder", "Co-Founder", "Boss", "Manager", "Team Lead", "Head of", "Consultant", "Advisor", "Board Member", "Staff", "Engineer", "Developer", "Designer", "Product Manager", "Project Manager", "Business Development", "Sales", "Marketing", "Operations", "HR", "Legal", "Other"
        ]
        self.CAREER_OPTIONS = [
            "Entrepreneur", "Investment Banker", "Private Equity", "Venture Capital", "Startup Founder", "Corporate Executive", "Family Office", "Hedge Fund Manager", "Consultant", "Management Consultant", "Strategy Consultant", "Accountant", "Auditor", "Lawyer", "Attorney", "Engineer", "Software Engineer", "Product Manager", "Project Manager", "Sales", "Marketing", "Operations", "Human Resources", "Recruiter", "Real Estate", "Insurance", "Healthcare", "Doctor", "Nurse", "Pharmacist", "Scientist", "Researcher", "Professor", "Teacher", "Student", "Government", "Nonprofit", "Philanthropy", "Artist", "Musician", "Writer", "Designer", "Other"
        ]
        self.US_STATES = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "International", "Global"
        ]
        self.COMPANY_STAGES = [
            "Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Series D", "Public", "Private"
        ]
        self.COMPANY_TYPES = [
            "Investment Bank", "Private Equity", "Venture Capital", "Startup", "Corporate", "Family Office", "Hedge Fund", "Real Estate", "Other"
        ]
        self.COMPANY_SECTORS = [
            "Technology", "Healthcare", "Finance", "Real Estate", "Consumer", "Energy", "Industrial", "Telecom", "Education", "Other"
        ]
        self.CITY_OPTIONS = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Mesa", "Sacramento", "Atlanta", "Kansas City", "Colorado Springs", "Miami", "Raleigh", "Omaha", "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tulsa", "Arlington", "Tampa", "New Orleans", "Wichita", "Cleveland", "Bakersfield", "Aurora", "Anaheim", "Honolulu", "Santa Ana", "Riverside", "Corpus Christi", "Lexington", "Stockton", "Henderson", "Saint Paul", "St. Louis", "Cincinnati", "Pittsburgh", "Greensboro", "Anchorage", "Plano", "Lincoln", "Orlando", "Irvine", "Newark", "Toledo", "Durham", "Chula Vista", "Fort Wayne", "Jersey City", "St. Petersburg", "Laredo", "Madison", "Chandler", "Buffalo", "Lubbock", "Scottsdale", "Reno", "Glendale", "Gilbert", "Winston–Salem", "North Las Vegas", "Norfolk", "Chesapeake", "Garland", "Irving", "Hialeah", "Fremont", "Boise", "Richmond"
        ]
        
        # Define relationship options
        self.RELATIONSHIP_TYPE_OPTIONS = [
            "Passive Friendship",
            "Lead - First Outreach",
            "Lead - First Follow-up",
            "Lead - Second Follow-up",
            "Lead - Third Follow-up",
            "Professional Relationship",
            "Dead Lead"
        ]
        
        self.load_data()
        self.setup_ui()
        self.refresh_contacts()

    def setup_ui(self):
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Loading overlay
        self.loading_overlay = tk.Frame(self.root, bg="white")
        self.loading_label = tk.Label(self.loading_overlay, text="Loading...", font=("Helvetica", 18, "bold"), bg="white", fg="black")
        self.loading_label.pack(expand=True)
        self.loading_overlay.place_forget()
        
        # Create navigation buttons
        nav_frame = ttk.Frame(self.main_container)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        self.nav_buttons = {}
        style = ttk.Style()
        style.configure("ActiveNav.TButton", font=("Helvetica", 10, "bold"), relief="solid", borderwidth=2)
        style.configure("InactiveNav.TButton", font=("Helvetica", 10, "normal"), relief="flat", borderwidth=1)
        self.nav_buttons["dashboard"] = ttk.Button(nav_frame, text="Analytics Dashboard", command=lambda: self.show_page("dashboard"), style="ActiveNav.TButton")
        self.nav_buttons["dashboard"].pack(side=tk.LEFT, padx=5)
        self.nav_buttons["contacts"] = ttk.Button(nav_frame, text="Contacts", command=lambda: self.show_page("contacts"), style="InactiveNav.TButton")
        self.nav_buttons["contacts"].pack(side=tk.LEFT, padx=5)
        self.nav_buttons["companies"] = ttk.Button(nav_frame, text="Companies", command=lambda: self.show_page("companies"), style="InactiveNav.TButton")
        self.nav_buttons["companies"].pack(side=tk.LEFT, padx=5)
        self.nav_buttons["tasks"] = ttk.Button(nav_frame, text="Tasks", command=lambda: self.show_page("tasks"), style="InactiveNav.TButton")
        self.nav_buttons["tasks"].pack(side=tk.LEFT, padx=5)
        self.nav_buttons["analytics"] = ttk.Button(nav_frame, text="Data Search", command=lambda: self.show_page("analytics"), style="InactiveNav.TButton")
        self.nav_buttons["analytics"].pack(side=tk.LEFT, padx=5)
        
        # Create pages
        self.setup_dashboard_ui()
        self.setup_contacts_ui()
        self.setup_companies_ui()
        self.setup_tasks_ui()
        self.analytics_frame = ttk.Frame(self.root)
        self.setup_analytics_ui()
        
        # Show initial page
        self.show_page("dashboard")
        
        # Fix treeview style after all frames are created
        self.fix_treeview_style()

    def setup_dashboard_ui(self):
        self.dashboard_frame = ttk.Frame(self.root)
        header = ttk.Label(self.dashboard_frame, text="Analytics Dashboard", font=("Helvetica", 18, "bold"))
        header.pack(pady=20)
        # Placeholder for dashboard content
        summary_label = ttk.Label(self.dashboard_frame, text="Welcome to your Analytics Dashboard!", font=("Helvetica", 12))
        summary_label.pack(pady=10)

    def show_loading(self):
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_overlay.lift()
        self.root.update_idletasks()

    def hide_loading(self):
        self.loading_overlay.place_forget()
        self.root.update_idletasks()

    def show_page(self, page_name):
        self.show_loading()
        self.root.after(100, lambda: self._show_page(page_name))

    def _show_page(self, page_name):
        # Hide all pages
        if hasattr(self, 'dashboard_frame'):
            self.dashboard_frame.pack_forget()
        self.contacts_frame.pack_forget()
        self.companies_frame.pack_forget()
        self.tasks_frame.pack_forget()
        if hasattr(self, 'analytics_frame'):
            self.analytics_frame.pack_forget()
        # Update nav button styles
        for key, btn in self.nav_buttons.items():
            if key == page_name:
                btn.config(style="ActiveNav.TButton")
            else:
                btn.config(style="InactiveNav.TButton")
        if page_name == "dashboard":
            self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "contacts":
            self.contacts_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "companies":
            self.companies_frame.pack(fill=tk.BOTH, expand=True)
            self.refresh_companies()  # Always refresh companies when showing the page
        elif page_name == "tasks":
            self.tasks_frame.pack(fill=tk.BOTH, expand=True)
            self.refresh_tasks()
        elif page_name == "analytics":
            self.analytics_frame.pack(fill=tk.BOTH, expand=True)
        self.current_page = page_name
        self.hide_loading()

    def setup_tasks_ui(self):
        self.tasks_frame = ttk.Frame(self.root)
        
        # Tasks header
        header_frame = ttk.Frame(self.tasks_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(header_frame, text="Follow-up Tasks", font=("Helvetica", 14, "bold")).pack(side=tk.LEFT)
        
        # Tasks table
        table_frame = ttk.Frame(self.tasks_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Contact", "Type", "Due Date", "Days Left", "Status", "Notes")
        self.tasks_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=120)
        
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        self.tasks_tree.bind("<ButtonRelease-1>", self.on_task_select)
        
        # Mark as Done button
        self.mark_done_btn = ttk.Button(self.tasks_frame, text="Mark as Done", command=self.mark_task_done, state=tk.DISABLED)
        self.mark_done_btn.pack(pady=5)
        
        # Refresh button
        ttk.Button(self.tasks_frame, text="Refresh Tasks", command=self.refresh_tasks).pack(pady=5)
        
        # Notification label
        self.notification_label = ttk.Label(self.tasks_frame, text="", font=("Helvetica", 10, "bold"))
        self.notification_label.pack(pady=2)

    def on_task_select(self, event):
        selection = self.tasks_tree.selection()
        if selection:
            self.mark_done_btn.config(state=tk.NORMAL)
        else:
            self.mark_done_btn.config(state=tk.DISABLED)

    def mark_task_done(self):
        selection = self.tasks_tree.selection()
        if not selection:
            return
        item = self.tasks_tree.item(selection[0])
        contact_name = item['values'][0]
        task_type = item['values'][1]
        due_date = item['values'][2]
        # Find the contact
        contact = None
        for c in self.contacts:
            if c.get("name") == contact_name:
                contact = c
                break
        if not contact:
            return
        # Log the interaction
        if "history" not in contact:
            contact["history"] = []
        contact["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": task_type,
            "stage": task_type,
            "note": f"Completed {task_type} scheduled for {due_date}"
        })
        contact["last_contact"] = datetime.now().strftime("%Y-%m-%d")
        # Lead follow-up workflow
        if contact.get("relationship_type") == "Lead":
            stages = list(self.RELATIONSHIP_TYPES["Lead"]["stages"].keys())
            current_stage = contact.get("lead_stage", stages[1])  # Default to First Follow-up
            if task_type in stages:
                idx = stages.index(task_type)
                # Show dialog to ask about response
                response = messagebox.askyesnocancel(
                    "Follow-up Response",
                    f"Did you get a response from {contact_name}?",
                    icon='question'
                )
                if response is None:
                    return
                elif response:
                    contact["relationship_type"] = "Professional Relationship"
                    contact.pop("lead_stage", None)
                    messagebox.showinfo("Status Updated", f"{contact_name} has been converted to a Professional Relationship.")
                else:
                    if idx + 1 < len(stages):
                        contact["lead_stage"] = stages[idx + 1]
                        messagebox.showinfo("Status Updated", f"{contact_name} will be moved to {stages[idx + 1]}.")
                    else:
                        contact["relationship_type"] = "Dead Lead"
                        contact.pop("lead_stage", None)
                        messagebox.showinfo("Status Updated", f"{contact_name} has been marked as a Dead Lead after no response.")
        self.save_data()
        self.refresh_tasks()
        self.refresh_contacts()
        self.mark_done_btn.config(state=tk.DISABLED)
        messagebox.showinfo("Task Completed", f"Marked {task_type} for {contact_name} as done.")

    def refresh_tasks(self):
        # Clear existing tasks
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        self.notification_label.config(text="")
        overdue_count = 0
        tasks = []
        for contact in self.contacts:
            last_contact = contact.get("last_contact")
            if not last_contact:
                continue
            relationship_type = contact.get("relationship_type", "Passive Friendship")
            if relationship_type == "Passive Friendship":
                continue
            try:
                last_contact_date = datetime.strptime(last_contact, "%Y-%m-%d")
            except Exception:
                continue
            history = contact.get("history", [])
            done_stages = [h.get("stage") for h in history]
            if relationship_type == "Lead":
                stages = list(self.RELATIONSHIP_TYPES["Lead"]["stages"].keys())
                lead_stage = contact.get("lead_stage", stages[1])  # Default to First Follow-up
                if lead_stage in stages:
                    i = stages.index(lead_stage)
                    stage = lead_stage
                    # Find the date of the previous follow-up (or last_contact for first follow-up)
                    if i == 1:
                        prev_date = last_contact_date
                    else:
                        # Find the most recent completion date for the previous stage
                        prev_stage = stages[i-1]
                        prev_date = last_contact_date
                        for h in reversed(history):
                            if h.get("stage") == prev_stage:
                                try:
                                    prev_date = datetime.strptime(h["date"][:10], "%Y-%m-%d")
                                except Exception:
                                    pass
                                break
                    due_date = prev_date + timedelta(days=self.RELATIONSHIP_TYPES["Lead"]["stages"][stage])
                    days_left = (due_date - datetime.now()).days
                    if due_date < datetime.now():
                        status = "Overdue"
                    elif days_left <= 2:
                        status = "Upcoming"
                    else:
                        status = "Done"
                    tasks.append((status, days_left, contact["name"], stage, due_date.strftime("%Y-%m-%d"), status, f"{stage} for {contact['name']}"))
                    if status == "Overdue":
                        overdue_count += 1
            elif relationship_type == "Professional Relationship":
                maintenance_interval = self.RELATIONSHIP_TYPES["Professional Relationship"]["maintenance"]
                next_maintenance = last_contact_date
                while next_maintenance <= datetime.now():
                    next_maintenance += timedelta(days=maintenance_interval)
                days_left = (next_maintenance - datetime.now()).days
                if next_maintenance < datetime.now():
                    status = "Overdue"
                elif days_left <= 2:
                    status = "Upcoming"
                else:
                    status = "Done"
                tasks.append((status, days_left, contact["name"], "Maintenance", next_maintenance.strftime("%Y-%m-%d"), status, f"Regular check-in with {contact['name']}"))
                if status == "Overdue":
                    overdue_count += 1
        # Sort: Overdue (red), Upcoming (yellow), Done (green)
        status_order = {"Overdue": 0, "Upcoming": 1, "Done": 2}
        tasks.sort(key=lambda x: (status_order.get(x[0], 3), x[1]))
        columns = ("Contact", "Type", "Due Date", "Days Left", "Status", "Notes")
        self.tasks_tree["columns"] = columns
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=120)
        for t in tasks:
            self.tasks_tree.insert("", tk.END, values=(t[2], t[3], t[4], t[1], t[5], t[6]), tags=(t[0],))
        self.tasks_tree.tag_configure("Overdue", background="#ffcccc", foreground="#000000")
        self.tasks_tree.tag_configure("Upcoming", background="#fff2cc", foreground="#000000")
        self.tasks_tree.tag_configure("Done", background="#ccffcc", foreground="#000000")
        if overdue_count > 0:
            self.notification_label.config(text=f"You have {overdue_count} overdue follow-up task(s)!", foreground="red")
        else:
            self.notification_label.config(text="All tasks are up to date!", foreground="green")

    # Fix font color for all Treeviews
    def fix_treeview_style(self):
        style = ttk.Style()
        style.theme_use('arc')
        style.configure("Treeview", foreground="#000000", background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", foreground="#000000", background="#e0e0e0")
        style.map("Treeview", background=[('selected', '#cce5ff')], foreground=[('selected', '#000000')])
        # Set default background for frames and labels
        self.root.configure(bg="#ffffff")
        for frame in [self.contacts_frame, self.companies_frame, self.tasks_frame]:
            frame.configure(style="White.TFrame")
        style.configure("White.TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#000000")
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")
        style.configure("TCombobox", fieldbackground="#ffffff", foreground="#000000")
        style.configure("TButton", background="#e0e0e0", foreground="#000000")

    def setup_contacts_ui(self):
        self.contacts_frame = ttk.Frame(self.root)
        form_frame = ttk.LabelFrame(self.contacts_frame, text="Contact Details")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        entry_frame = ttk.Frame(form_frame)
        entry_frame.pack(fill=tk.X, padx=5, pady=5)
        self.entries = {}
        # Redesigned layout: 3 columns, more balanced
        labels = [
            ("Name", 0, 0), ("Email", 0, 1), ("Phone", 0, 2),
            ("Company", 1, 0), ("Tags", 1, 1)
        ]
        for label, row, col in labels:
            ttk.Label(entry_frame, text=f"{label}:").grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(entry_frame)
            entry.grid(row=row, column=col*2+1, sticky=tk.W+tk.E, padx=5, pady=2)
            self.entries[label] = entry
        # Job Title
        ttk.Label(entry_frame, text="Job Title:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.job_title_var = tk.StringVar()
        self.job_title_dropdown = ttk.Combobox(entry_frame, textvariable=self.job_title_var, values=self.JOB_TITLE_OPTIONS)
        self.job_title_dropdown.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        self.job_title_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.job_title_dropdown, self.JOB_TITLE_OPTIONS))
        # Career
        ttk.Label(entry_frame, text="Career:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.career_var = tk.StringVar()
        self.career_dropdown = ttk.Combobox(entry_frame, textvariable=self.career_var, values=self.CAREER_OPTIONS)
        self.career_dropdown.grid(row=2, column=3, sticky=tk.W+tk.E, padx=5, pady=2)
        self.career_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.career_dropdown, self.CAREER_OPTIONS))
        # Relationship Type
        ttk.Label(entry_frame, text="Relationship:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.relationship_var = tk.StringVar()
        self.relationship_dropdown = ttk.Combobox(entry_frame, textvariable=self.relationship_var, values=self.RELATIONSHIP_TYPE_OPTIONS)
        self.relationship_dropdown.grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        self.relationship_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.relationship_dropdown, self.RELATIONSHIP_TYPE_OPTIONS))
        # Relationship Level
        ttk.Label(entry_frame, text="Relationship Level:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.relationship_level_var = tk.IntVar(value=3)
        self.relationship_level_dropdown = ttk.Combobox(entry_frame, textvariable=self.relationship_level_var, values=[1,2,3,4,5], state="readonly")
        self.relationship_level_dropdown.grid(row=3, column=3, sticky=tk.W+tk.E, padx=5, pady=2)
        # State
        ttk.Label(entry_frame, text="State:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.state_var = tk.StringVar()
        self.state_dropdown = ttk.Combobox(entry_frame, textvariable=self.state_var, values=self.US_STATES)
        self.state_dropdown.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        self.state_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.state_dropdown, self.US_STATES))
        # City
        ttk.Label(entry_frame, text="City:").grid(row=4, column=2, sticky=tk.W, padx=5, pady=2)
        self.city_var = tk.StringVar()
        self.city_dropdown = ttk.Combobox(entry_frame, textvariable=self.city_var, values=self.CITY_OPTIONS)
        self.city_dropdown.grid(row=4, column=3, sticky=tk.W+tk.E, padx=5, pady=2)
        self.city_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.city_dropdown, self.CITY_OPTIONS))
        # Last Contact
        ttk.Label(entry_frame, text="Last Contact:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.last_contact_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.last_contact_entry = ttk.Entry(entry_frame, textvariable=self.last_contact_var)
        self.last_contact_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        ttk.Label(entry_frame, text="(YYYY-MM-DD)").grid(row=5, column=2, sticky=tk.W, padx=5, pady=2)
        # Notes (large, white Text box)
        ttk.Label(entry_frame, text="Notes:").grid(row=6, column=0, sticky=tk.NW, padx=5, pady=2)
        self.notes_text = tk.Text(entry_frame, height=4, width=40, bg="white", fg="black")
        self.notes_text.grid(row=6, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=2)
        # Buttons
        btn_frame = ttk.Frame(self.contacts_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        self.add_contact_btn = ttk.Button(btn_frame, text="Add Contact", command=self.add_contact)
        self.add_contact_btn.pack(side=tk.LEFT, padx=5)
        self.update_contact_btn = ttk.Button(btn_frame, text="Update Contact", command=self.update_contact)
        self.update_contact_btn.pack(side=tk.LEFT, padx=5)
        self.delete_contact_btn = ttk.Button(btn_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_contact_btn.pack(side=tk.LEFT, padx=5)
        self.clear_contact_btn = ttk.Button(btn_frame, text="Clear Form", command=self.clear_contact_form)
        self.clear_contact_btn.pack(side=tk.LEFT, padx=5)
        # Bind Enter key to focused button
        for btn in [self.add_contact_btn, self.update_contact_btn, self.delete_contact_btn, self.clear_contact_btn]:
            btn.bind('<Return>', lambda e, b=btn: b.invoke())
        self.contacts_frame.bind_all('<Return>', self._handle_enter_key)
        # Table
        table_frame = ttk.Frame(self.contacts_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("Name", "Email", "Phone", "Company", "Job Title", "Career", "Relationship", "Relationship Level", "State", "City", "Last Contact", "Tags", "Notes")
        self.contacts_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.contacts_tree.heading(col, text=col)
            self.contacts_tree.column(col, width=120, minwidth=120, stretch=False)
        # Add horizontal scrollbar
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.contacts_tree.xview)
        self.contacts_tree.configure(xscrollcommand=xscroll.set)
        self.contacts_tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        xscroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.contacts_tree.bind("<<TreeviewSelect>>", self.on_contact_select)

    def get_contact_form_data(self):
        data = {k.lower(): self.entries[k].get().strip() for k in self.entries}
        data["job_title"] = self.job_title_var.get()
        data["career"] = self.career_var.get()
        data["relationship_type"] = self.relationship_var.get()
        data["relationship_level"] = self.relationship_level_var.get()
        data["state"] = self.state_var.get()
        data["city"] = self.city_var.get()
        data["last_contact"] = self.last_contact_var.get()
        data["notes"] = self.notes_text.get("1.0", tk.END).strip()
        return data

    def fill_contact_form(self, contact):
        for key, entry in self.entries.items():
            value = contact.get(key.lower(), "")
            if key == "Company":
                entry.set(value)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, value)
        self.job_title_var.set(contact.get("job_title", ""))
        self.career_var.set(contact.get("career", ""))
        self.relationship_var.set(contact.get("relationship_type", ""))
        self.relationship_level_var.set(contact.get("relationship_level", 3))
        self.state_var.set(contact.get("state", ""))
        self.city_var.set(contact.get("city", ""))
        self.last_contact_var.set(contact.get("last_contact", datetime.now().strftime("%Y-%m-%d")))
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(tk.END, contact.get("notes", ""))

    def clear_contact_form(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
        self.job_title_var.set("")
        self.career_var.set("")
        self.relationship_var.set("")
        self.relationship_level_var.set(3)
        self.state_var.set("")
        self.city_var.set("")
        self.last_contact_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.notes_text.delete("1.0", tk.END)
        self.selected_contact_index = None

    def refresh_contacts(self):
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        for contact in self.filtered_contacts:
            self.contacts_tree.insert("", tk.END, values=(
                contact.get("name", ""),
                contact.get("email", ""),
                contact.get("phone", ""),
                contact.get("company", ""),
                contact.get("job_title", ""),
                contact.get("career", ""),
                contact.get("relationship_type", ""),
                contact.get("relationship_level", ""),
                contact.get("state", ""),
                contact.get("city", ""),
                contact.get("last_contact", ""),
                contact.get("tags", ""),
                contact.get("notes", "")
            ))

    def show_contacts_page(self):
        self.companies_frame.pack_forget()
        self.tasks_frame.pack_forget()
        self.contacts_frame.pack(fill=tk.BOTH, expand=True)
        self.current_page = "contacts"
        self.refresh_contacts()

    def show_companies_page(self):
        self.contacts_frame.pack_forget()
        self.tasks_frame.pack_forget()
        self.companies_frame.pack(fill=tk.BOTH, expand=True)
        self.current_page = "companies"
        self.refresh_companies()

    def load_data(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.contacts = data
                    self.companies = []
                    self.save_data()
                else:
                    self.contacts = data.get("contacts", [])
                    # Convert old company format (list of strings) to new format (list of dicts)
                    companies = data.get("companies", [])
                    self.companies = [{"name": c} if isinstance(c, str) else c for c in companies]
        else:
            self.contacts = []
            self.companies = []
            
        self.filtered_contacts = self.contacts.copy()

    def save_data(self):
        data = {
            "contacts": self.contacts,
            "companies": self.companies
        }
        with open(CONTACTS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def on_contact_select(self, event):
        selection = self.contacts_tree.selection()
        if selection:
            index = self.contacts_tree.index(selection[0])
            self.selected_contact_index = index
            self.fill_contact_form(self.filtered_contacts[index])

    def add_contact(self):
        data = self.get_contact_form_data()
        if not data["name"]:
            messagebox.showerror("Error", "Name is required!")
            return
        # Validate last contact date format
        if data["last_contact"]:
            try:
                datetime.strptime(data["last_contact"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Last Contact date must be in YYYY-MM-DD format!")
                return
        # Add company if it doesn't exist
        if data.get("company"):
            company_exists = False
            for company in self.companies:
                if company.get("name") == data["company"]:
                    company_exists = True
                    break
            if not company_exists:
                self.companies.append({
                    "name": data["company"],
                    "location": data.get("city", ""),
                    "stage": "",
                    "type": "",
                    "sector": "",
                    "website": "",
                    "description": ""
                })
        self.contacts.append(data)
        self.filtered_contacts = self.contacts.copy()
        self.save_data()
        self.clear_contact_form()
        self.refresh_contacts()
        self.refresh_companies()  # Refresh companies to update stats
        self.refresh_tasks()  # Refresh tasks to show new follow-ups
        messagebox.showinfo("Success", "Contact added successfully!")
        self.selected_contact_index = None

    def update_contact(self):
        if self.selected_contact_index is None:
            messagebox.showerror("Error", "Please select a contact to update!")
            return
        data = self.get_contact_form_data()
        if not data["name"]:
            messagebox.showerror("Error", "Name is required!")
            return
        # Validate last contact date format
        if data["last_contact"]:
            try:
                datetime.strptime(data["last_contact"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Last Contact date must be in YYYY-MM-DD format!")
                return
        # Add company if it doesn't exist
        if data.get("company"):
            company_exists = False
            for company in self.companies:
                if company.get("name") == data["company"]:
                    company_exists = True
                    break
            if not company_exists:
                self.companies.append({
                    "name": data["company"],
                    "location": data.get("city", ""),
                    "stage": "",
                    "type": "",
                    "sector": "",
                    "website": "",
                    "description": ""
                })
        self.contacts[self.selected_contact_index] = data
        self.filtered_contacts = self.contacts.copy()
        self.save_data()
        self.refresh_contacts()
        self.refresh_companies()  # Refresh companies to update stats
        self.refresh_tasks()  # Refresh tasks to show updated follow-ups
        self.clear_contact_form()
        messagebox.showinfo("Success", "Contact updated successfully!")
        self.selected_contact_index = None

    def delete_contact(self):
        if self.selected_contact_index is None:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            del self.contacts[self.selected_contact_index]
            self.filtered_contacts = self.contacts.copy()
            self.save_data()
            self.refresh_contacts()
            self.clear_contact_form()
            messagebox.showinfo("Success", "Contact deleted successfully!")

    def setup_companies_ui(self):
        self.companies_frame = ttk.Frame(self.root)
        
        # Form
        form_frame = ttk.LabelFrame(self.companies_frame, text="Company Details")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        entry_frame = ttk.Frame(form_frame)
        entry_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Name
        ttk.Label(entry_frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.company_name_entry = ttk.Entry(entry_frame)
        self.company_name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        # Location
        ttk.Label(entry_frame, text="Location:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.company_location_var = tk.StringVar()
        self.company_location_dropdown = ttk.Combobox(entry_frame, textvariable=self.company_location_var, values=self.CITY_OPTIONS, state="readonly")
        self.company_location_dropdown.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        # State
        ttk.Label(entry_frame, text="State:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.company_state_var = tk.StringVar()
        self.company_state_dropdown = ttk.Combobox(entry_frame, textvariable=self.company_state_var, values=self.US_STATES)
        self.company_state_dropdown.grid(row=0, column=5, sticky=tk.W, padx=5, pady=2)
        self.company_state_dropdown.bind('<KeyRelease>', lambda e: self._autocomplete(self.company_state_dropdown, self.US_STATES))
        # Stage
        ttk.Label(entry_frame, text="Stage:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.company_stage_var = tk.StringVar()
        self.company_stage_dropdown = ttk.Combobox(entry_frame, textvariable=self.company_stage_var, values=self.COMPANY_STAGES, state="readonly")
        self.company_stage_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        # Type
        ttk.Label(entry_frame, text="Type:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.company_type_var = tk.StringVar()
        self.company_type_dropdown = ttk.Combobox(entry_frame, textvariable=self.company_type_var, values=self.COMPANY_TYPES, state="readonly")
        self.company_type_dropdown.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        # Sector
        ttk.Label(entry_frame, text="Sector:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.company_sector_var = tk.StringVar()
        self.company_sector_dropdown = ttk.Combobox(entry_frame, textvariable=self.company_sector_var, values=self.COMPANY_SECTORS, state="readonly")
        self.company_sector_dropdown.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        # Website
        ttk.Label(entry_frame, text="Website:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.company_website_entry = ttk.Entry(entry_frame)
        self.company_website_entry.grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
        # Description
        ttk.Label(entry_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.company_desc_text = tk.Text(entry_frame, height=4, width=40, bg="white", fg="black")
        self.company_desc_text.grid(row=3, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(self.companies_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Add Company", command=self.add_company).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Company", command=self.update_company).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Company", command=self.delete_company).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_company_form).pack(side=tk.LEFT, padx=5)
        
        # Table
        table_frame = ttk.Frame(self.companies_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("Name", "Location", "State", "Stage", "Type", "Sector", "Website", "Description")
        self.companies_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            if col == "Description":
                self.companies_tree.heading(col, text=col)
                self.companies_tree.column(col, width=260, minwidth=180, stretch=True)
            else:
                self.companies_tree.heading(col, text=col)
                self.companies_tree.column(col, width=120, minwidth=100, stretch=False)
        # Add horizontal scrollbar
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.companies_tree.xview)
        self.companies_tree.configure(xscrollcommand=xscroll.set)
        self.companies_tree.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        xscroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.companies_tree.bind("<<TreeviewSelect>>", self.on_company_select)

    def get_company_form_data(self):
        return {
            "name": self.company_name_entry.get().strip(),
            "location": self.company_location_var.get(),
            "state": self.company_state_var.get(),
            "stage": self.company_stage_var.get(),
            "type": self.company_type_var.get(),
            "sector": self.company_sector_var.get(),
            "website": self.company_website_entry.get().strip(),
            "description": self.company_desc_text.get("1.0", tk.END).strip()
        }

    def fill_company_form(self, company):
        self.company_name_entry.delete(0, tk.END)
        self.company_name_entry.insert(0, company.get("name", ""))
        self.company_location_var.set(company.get("location", ""))
        self.company_state_var.set(company.get("state", ""))
        self.company_stage_var.set(company.get("stage", ""))
        self.company_type_var.set(company.get("type", ""))
        self.company_sector_var.set(company.get("sector", ""))
        self.company_website_entry.delete(0, tk.END)
        self.company_website_entry.insert(0, company.get("website", ""))
        self.company_desc_text.delete("1.0", tk.END)
        self.company_desc_text.insert("1.0", company.get("description", ""))

    def clear_company_form(self):
        self.company_name_entry.delete(0, tk.END)
        self.company_location_var.set("")
        self.company_state_var.set("")
        self.company_stage_var.set("")
        self.company_type_var.set("")
        self.company_sector_var.set("")
        self.company_website_entry.delete(0, tk.END)
        self.company_desc_text.delete("1.0", tk.END)
        self.selected_company_index = None

    def refresh_companies(self):
        for item in self.companies_tree.get_children():
            self.companies_tree.delete(item)
        for company in self.companies:
            # Calculate stats for this company-location
            leads = 0
            professionals = 0
            for contact in self.contacts:
                contact_company = (contact.get("company") or "").strip().lower()
                contact_location = (contact.get("city") or contact.get("location") or "").strip().lower()
                company_name = (company.get("name") or "").strip().lower()
                company_location = (company.get("location") or "").strip().lower()
                if contact_company == company_name and contact_location == company_location:
                    if contact.get("relationship_type") and "lead" in contact.get("relationship_type").lower():
                        leads += 1
                    elif contact.get("relationship_type") == "Professional Relationship":
                        professionals += 1
            stats = f"Leads: {leads}, Professional Relationships: {professionals}"
            self.companies_tree.insert("", tk.END, values=(
                company.get("name", ""),
                company.get("location", ""),
                company.get("state", ""),
                company.get("stage", ""),
                company.get("type", ""),
                company.get("sector", ""),
                company.get("website", ""),
                stats
            ))

    def on_company_select(self, event):
        selection = self.companies_tree.selection()
        if selection:
            index = self.companies_tree.index(selection[0])
            self.selected_company_index = index
            self.fill_company_form(self.companies[index])

    def add_company(self):
        data = self.get_company_form_data()
        if not data["name"]:
            messagebox.showerror("Error", "Company name is required!")
            return
        self.companies.append(data)
        self.save_data()
        self.refresh_companies()
        self.clear_company_form()
        messagebox.showinfo("Success", "Company added successfully!")

    def update_company(self):
        if self.selected_company_index is None:
            messagebox.showerror("Error", "Please select a company to update!")
            return
        data = self.get_company_form_data()
        if not data["name"]:
            messagebox.showerror("Error", "Company name is required!")
            return
        self.companies[self.selected_company_index] = data
        self.save_data()
        self.refresh_companies()
        self.clear_company_form()
        messagebox.showinfo("Success", "Company updated successfully!")

    def delete_company(self):
        if self.selected_company_index is None:
            messagebox.showerror("Error", "Please select a company to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this company?"):
            del self.companies[self.selected_company_index]
            self.save_data()
            self.refresh_companies()
            self.clear_company_form()
            messagebox.showinfo("Success", "Company deleted successfully!")

    def _autocomplete(self, combobox, options):
        value = combobox.get()
        filtered = [item for item in options if value.lower() in item.lower()]
        combobox['values'] = filtered if filtered else options

    def _handle_enter_key(self, event):
        widget = self.root.focus_get()
        if isinstance(widget, ttk.Button):
            widget.invoke()

    def setup_analytics_ui(self):
        # Create main container with padding
        main_container = ttk.Frame(self.analytics_frame, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Mode selector (Businesses/Individuals)
        mode_frame = ttk.Frame(main_container)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        self.analytics_mode_var = tk.StringVar(value="Businesses")
        ttk.Label(mode_frame, text="View:").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Businesses", variable=self.analytics_mode_var, value="Businesses").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Individuals", variable=self.analytics_mode_var, value="Individuals").pack(side=tk.LEFT, padx=5)
        
        # Left panel for filters
        left_panel = ttk.LabelFrame(main_container, text="Filters", padding="5")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        self.analytics_filter_frame = ttk.Frame(left_panel)
        self.analytics_filter_frame.pack(fill=tk.X, pady=5)
        
        # Search button
        search_btn = ttk.Button(left_panel, text="Search", command=self.update_analytics)
        search_btn.pack(pady=10)
        
        # Right panel for data display
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Summary section
        summary_frame = ttk.LabelFrame(right_panel, text="Summary", padding="5")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_text = tk.Text(summary_frame, height=4, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.X)
        
        # Data display section
        data_frame = ttk.LabelFrame(right_panel, text="Data", padding="5")
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analytics_data_frame = data_frame
        self.analytics_tree = None  # Will be created in update_analytics
        
        # Initialize analytics
        self.update_analytics()

    def update_analytics(self, event=None):
        # Clear filter frame
        for widget in self.analytics_filter_frame.winfo_children():
            widget.destroy()
        # Remove old treeview if exists
        if self.analytics_tree:
            self.analytics_tree.destroy()
        for widget in self.analytics_data_frame.winfo_children():
            if isinstance(widget, ttk.Scrollbar):
                widget.destroy()
        mode = self.analytics_mode_var.get()
        data = []
        columns = []
        filter_widgets = []
        # --- Businesses Mode ---
        if mode == "Businesses":
            columns = ("Company Name", "State", "City", "Sector", "Type", "Stage", "Website", "# of Contacts", "Leads", "Professionals")
            # Filters
            ttk.Label(self.analytics_filter_frame, text="State:").pack(anchor=tk.W)
            state_var = tk.StringVar(value="All")
            state_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=state_var, values=["All"] + self.US_STATES)
            state_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("state", state_var))
            
            ttk.Label(self.analytics_filter_frame, text="Sector:").pack(anchor=tk.W)
            sector_var = tk.StringVar(value="All")
            sector_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=sector_var, values=["All"] + self.COMPANY_SECTORS)
            sector_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("sector", sector_var))
            
            ttk.Label(self.analytics_filter_frame, text="Type:").pack(anchor=tk.W)
            type_var = tk.StringVar(value="All")
            type_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=type_var, values=["All"] + self.COMPANY_TYPES)
            type_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("type", type_var))
            
            ttk.Label(self.analytics_filter_frame, text="Stage:").pack(anchor=tk.W)
            stage_var = tk.StringVar(value="All")
            stage_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=stage_var, values=["All"] + self.COMPANY_STAGES)
            stage_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("stage", stage_var))
            
            # Collect data
            for company in self.companies:
                if state_var.get() != "All" and company.get("state", "") != state_var.get():
                    continue
                if sector_var.get() != "All" and company.get("sector", "") != sector_var.get():
                    continue
                if type_var.get() != "All" and company.get("type", "") != type_var.get():
                    continue
                if stage_var.get() != "All" and company.get("stage", "") != stage_var.get():
                    continue
                
                # Count contacts and categorize them
                leads = 0
                professionals = 0
                total_contacts = 0
                for contact in self.contacts:
                    if contact.get("company", "").lower() == company.get("name", "").lower():
                        total_contacts += 1
                        if contact.get("relationship_type") and "lead" in contact.get("relationship_type", "").lower():
                            leads += 1
                        elif contact.get("relationship_type") == "Professional Relationship":
                            professionals += 1
                
                data.append((
                    company.get("name", ""),
                    company.get("state", ""),
                    company.get("location", ""),
                    company.get("sector", ""),
                    company.get("type", ""),
                    company.get("stage", ""),
                    company.get("website", ""),
                    total_contacts,
                    leads,
                    professionals
                ))
        # --- Individuals Mode ---
        else:
            columns = ("Name", "Company", "State", "City", "Relationship", "Job Title", "Career", "Last Contact", "Tags", "Notes")
            # Filters
            ttk.Label(self.analytics_filter_frame, text="State:").pack(anchor=tk.W)
            state_var = tk.StringVar(value="All")
            state_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=state_var, values=["All"] + self.US_STATES)
            state_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("state", state_var))
            
            ttk.Label(self.analytics_filter_frame, text="Relationship:").pack(anchor=tk.W)
            rel_var = tk.StringVar(value="All")
            rel_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=rel_var, values=["All"] + self.RELATIONSHIP_TYPE_OPTIONS)
            rel_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("relationship", rel_var))
            
            ttk.Label(self.analytics_filter_frame, text="Company:").pack(anchor=tk.W)
            company_var = tk.StringVar(value="All")
            company_names = sorted(list(set([c.get("company", "") for c in self.contacts if c.get("company")])))
            company_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=company_var, values=["All"] + company_names)
            company_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("company", company_var))
            
            ttk.Label(self.analytics_filter_frame, text="Career:").pack(anchor=tk.W)
            career_var = tk.StringVar(value="All")
            career_dropdown = ttk.Combobox(self.analytics_filter_frame, textvariable=career_var, values=["All"] + self.CAREER_OPTIONS)
            career_dropdown.pack(fill=tk.X, pady=(0, 10))
            filter_widgets.append(("career", career_var))
            
            # Collect data
            for contact in self.contacts:
                if state_var.get() != "All" and contact.get("state", "") != state_var.get():
                    continue
                if rel_var.get() != "All" and contact.get("relationship_type", "") != rel_var.get():
                    continue
                if company_var.get() != "All" and contact.get("company", "") != company_var.get():
                    continue
                if career_var.get() != "All" and contact.get("career", "") != career_var.get():
                    continue
                
                data.append((
                    contact.get("name", ""),
                    contact.get("company", ""),
                    contact.get("state", ""),
                    contact.get("city", ""),
                    contact.get("relationship_type", ""),
                    contact.get("job_title", ""),
                    contact.get("career", ""),
                    contact.get("last_contact", ""),
                    contact.get("tags", ""),
                    contact.get("notes", "")
                ))
        
        # Create new treeview
        self.analytics_tree = ttk.Treeview(self.analytics_data_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.analytics_tree.heading(col, text=col)
            self.analytics_tree.column(col, width=140, minwidth=100, stretch=True)
        
        # Add scrollbars
        yscroll = ttk.Scrollbar(self.analytics_data_frame, orient="vertical", command=self.analytics_tree.yview)
        xscroll = ttk.Scrollbar(self.analytics_data_frame, orient="horizontal", command=self.analytics_tree.xview)
        self.analytics_tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.analytics_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Insert data
        for row in data:
            self.analytics_tree.insert("", tk.END, values=row)
        
        # Update summary
        summary = f"Mode: {mode}\nTotal Results: {len(data)}\n"
        if mode == "Businesses":
            total_leads = sum(row[8] for row in data)
            total_professionals = sum(row[9] for row in data)
            summary += f"Total Leads: {total_leads}\nTotal Professional Relationships: {total_professionals}"
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", summary)

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = ContactManager(root)
    root.mainloop() 