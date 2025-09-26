import sqlite3                             # Import the sqlite3 module to connect to and interact with a SQLite database
import tkinter as tk                       # Import the tkinter module to create a GUI (Graphical User Interface) in Python
from tkinter import ttk, messagebox        # Import ttk for themed widgets
from datetime import datetime              # Import datetime to work with dates and times 

class ProfessionalTrainerAssignmentApp:    # Define a class to manage the professional trainer assignment GUI
    def __init__(self, root):
        self.root = root
        self.root.title("FlexiGym Professional Trainer Management")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 650)
        
        # Create database connection 
        self.conn = sqlite3.connect('gym_database.db')
        self.cursor = self.conn.cursor()
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color scheme configuration
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure('Header.TLabel', background="#2e8b57", foreground="white", 
                           font=('Helvetica', 14, 'bold'))
        self.style.configure('Green.TButton', background="#2e8b57", foreground="white", 
                           font=('Helvetica', 10, 'bold'))
        self.style.configure('Red.TButton', background="#d32f2f", foreground="white", 
                           font=('Helvetica', 10, 'bold'))
        self.style.map('Green.TButton', 
                      background=[('active', '#3cb371'), ('disabled', '#d3d3d3')],
                      foreground=[('active', 'white'), ('disabled', 'gray')])
        self.style.map('Red.TButton', 
                      background=[('active', '#f44336'), ('disabled', '#d3d3d3')],
                      foreground=[('active', 'white'), ('disabled', 'gray')])
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25, background="#f0f0f0")
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'), background="#2e8b57", foreground="white")
        self.style.map('Treeview', background=[('selected', '#2e8b57')])
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Enhanced Header Section
        self.header_frame = tk.Frame(self.main_container, bg="#2e8b57", height=60)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        # Left-aligned header content
        self.header_content = tk.Frame(self.header_frame, bg="#2e8b57")
        self.header_content.pack(side="left", padx=20)
        
        # Logo with consistent styling
        self.logo_label = tk.Label(
            self.header_content,
            text="FLEXIGYM",
            font=('Helvetica', 14, 'bold'),
            fg="white",
            bg="#2e8b57",
            padx=5
        )
        self.logo_label.pack(side="left")
        
        # Title with same styling as logo
        self.title_label = tk.Label(
            self.header_content,
            text="PROFESSIONAL TRAINER MANAGEMENT SYSTEM",
            font=('Helvetica', 14, 'bold'),
            fg="white",
            bg="#2e8b57",
            padx=5
        )
        self.title_label.pack(side="left")
        
        # Current date display on the right
        self.date_label = tk.Label(
            self.header_frame,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=('Helvetica', 10),
            fg="white",
            bg="#2e8b57",
            padx=20
        )
        self.date_label.pack(side="right")
        
        # Separator with gradient
        separator = tk.Frame(self.main_container, height=2, bg="#2e8b57")
        separator.pack(fill="x", pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create Trainer Management Tab
        self.create_trainer_management_tab()
        
        # Create Assignment Tab
        self.create_assignment_tab()
        
        # Status Bar
        self.status_bar = tk.Frame(self.main_container, height=25, bg="#2e8b57")
        self.status_bar.pack(fill="x", pady=(10, 0))
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready",
            font=('Helvetica', 9),
            fg="white",
            bg="#2e8b57",
            anchor="w",
            padx=10
        )
        self.status_label.pack(side="left", fill="x", expand=True)
    
    def create_trainer_management_tab(self):
        # Create trainer tab
        self.trainer_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trainer_tab, text="Trainer Management")
        
        # Content Frame
        self.trainer_content_frame = ttk.Frame(self.trainer_tab)
        self.trainer_content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel - Add Trainer Form
        self.trainer_left_panel = ttk.Frame(self.trainer_content_frame)
        self.trainer_left_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        # Trainer Form
        self.trainer_form_frame = ttk.LabelFrame(
            self.trainer_left_panel,
            text=" Add/Update Trainer ",
            padding=(15, 10)
        )
        self.trainer_form_frame.pack(fill="both", expand=True)
        
        # Form Fields
        ttk.Label(
            self.trainer_form_frame,
            text="First Name:",
            font=('Helvetica', 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(
            self.trainer_form_frame,
            textvariable=self.first_name_var,
            font=('Helvetica', 10),
            width=30
        )
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(
            self.trainer_form_frame,
            text="Last Name:",
            font=('Helvetica', 10)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(
            self.trainer_form_frame,
            textvariable=self.last_name_var,
            font=('Helvetica', 10),
            width=30
        )
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(
            self.trainer_form_frame,
            text="Trainer ID:",
            font=('Helvetica', 10)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.trainer_id_var = tk.StringVar()
        self.trainer_id_entry = ttk.Entry(
            self.trainer_form_frame,
            textvariable=self.trainer_id_var,
            font=('Helvetica', 10),
            width=30
        )
        self.trainer_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Button Frame
        self.trainer_button_frame = ttk.Frame(self.trainer_form_frame)
        self.trainer_button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.add_trainer_button = ttk.Button(
            self.trainer_button_frame,
            text="Add Trainer",
            command=self.add_trainer,
            style='Green.TButton'
        )
        self.add_trainer_button.pack(side="left", padx=5)
        
        self.update_trainer_button = ttk.Button(
            self.trainer_button_frame,
            text="Update Trainer",
            command=self.update_trainer,
            style='Green.TButton'
        )
        self.update_trainer_button.pack(side="left", padx=5)
        
        self.delete_trainer_button = ttk.Button(
            self.trainer_button_frame,
            text="Delete Selected",
            command=self.delete_trainer,
            style='Red.TButton'
        )
        self.delete_trainer_button.pack(side="left", padx=5)
        
        # Add Refresh button
        self.refresh_trainer_button = ttk.Button(
            self.trainer_button_frame,
            text="Refresh",
            command=self.clear_trainer_fields,
            style='Green.TButton'
        )
        self.refresh_trainer_button.pack(side="left", padx=5)
        
        # Configure grid weights
        self.trainer_form_frame.grid_columnconfigure(1, weight=1)
        
        # Right Panel - Trainers List
        self.trainer_right_panel = ttk.Frame(self.trainer_content_frame)
        self.trainer_right_panel.pack(side="right", fill="both", expand=True, padx=10)
        
        # Trainers List
        self.trainers_list_frame = ttk.LabelFrame(
            self.trainer_right_panel,
            text=" Current Trainers ",
            padding=(15, 10)
        )
        self.trainers_list_frame.pack(fill="both", expand=True)
        
        # Create Treeview with scrollbars
        self.trainers_tree_container = ttk.Frame(self.trainers_list_frame)
        self.trainers_tree_container.pack(fill="both", expand=True)
        
        self.trainers_tree = ttk.Treeview(
            self.trainers_tree_container,
            columns=("trainer_id", "first_name", "last_name", "status"), 
            show="headings",
            height=15
        )
        
        # Configure columns 
        self.trainers_tree.heading("trainer_id", text="Trainer ID", anchor="center")
        self.trainers_tree.heading("first_name", text="First Name", anchor="center")
        self.trainers_tree.heading("last_name", text="Last Name", anchor="center")
        self.trainers_tree.heading("status", text="Status", anchor="center")
        
        self.trainers_tree.column("trainer_id", width=100, anchor="center")
        self.trainers_tree.column("first_name", width=150, anchor="center")  
        self.trainers_tree.column("last_name", width=150, anchor="center")   
        self.trainers_tree.column("status", width=100, anchor="center")
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(self.trainers_tree_container, orient="vertical", command=self.trainers_tree.yview)
        self.trainers_tree.configure(yscrollcommand=y_scroll.set)
        
        # Grid layout
        self.trainers_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        
        self.trainers_tree_container.grid_columnconfigure(0, weight=1)
        self.trainers_tree_container.grid_rowconfigure(0, weight=1)
        
        # Bind treeview selection to populate form
        self.trainers_tree.bind("<<TreeviewSelect>>", self.on_trainer_select)
    
    def create_assignment_tab(self):
        # Create assignment tab
        self.assignment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.assignment_tab, text="Trainer Assignment")
        
        # Main Content Area
        self.content_frame = ttk.Frame(self.assignment_tab)
        self.content_frame.pack(fill="both", expand=True)
        
        # Left Panel - Assignment Form
        self.left_panel = ttk.Frame(self.content_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        # Assignment Form
        self.form_frame = ttk.LabelFrame(
            self.left_panel,
            text=" New Assignment ",
            padding=(15, 10)
        )
        self.form_frame.pack(fill="both", expand=True)
        
        # Form Fields
        self.create_form_fields()
        
        # Right Panel - Summary and Assignments
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10)
        
        # Assignments List with Delete Button
        self.assignments_frame = ttk.LabelFrame(
            self.right_panel,
            text=" Current Assignments ",
            padding=(15, 10)
        )
        self.assignments_frame.pack(fill="both", expand=True)
        
        self.create_assignments_treeview()
        
        # Delete Button Frame
        self.delete_button_frame = ttk.Frame(self.assignments_frame)
        self.delete_button_frame.pack(fill="x", pady=(5, 0))
        
        self.delete_button = ttk.Button(
            self.delete_button_frame,
            text="Delete Selected Assignment",
            command=self.delete_assignment,
            style='Red.TButton'
        )
        self.delete_button.pack(side="right", padx=5)
        
        # Hours Summary
        self.hours_frame = ttk.LabelFrame(
            self.right_panel,
            text=" Trainer Hours Summary ",
            padding=(15, 10)
        )
        self.hours_frame.pack(fill="both", expand=True, pady=(15, 0))
        
        self.create_hours_treeview()
    
    def create_form_fields(self):
        # Class Selection
        ttk.Label(
            self.form_frame,
            text="Class:",
            font=('Helvetica', 10)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.class_var,
            state="readonly",
            font=('Helvetica', 10),
            width=30
        )
        self.class_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.class_combobox.bind("<<ComboboxSelected>>", self.update_class_details)
        
        # Class Details
        self.class_details_frame = ttk.Frame(self.form_frame)
        self.class_details_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.class_details_label = ttk.Label(
            self.class_details_frame,
            text="No class selected",
            font=('Helvetica', 10),
            wraplength=300,
            justify="left",
            background="#e8f5e9",
            padding=(10, 8),
            relief="solid",
            borderwidth=1
        )
        self.class_details_label.pack(fill="both", expand=True)
        
        # Trainer Selection
        ttk.Label(
            self.form_frame,
            text="Trainer:",
            font=('Helvetica', 10)
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.trainer_var = tk.StringVar()
        self.trainer_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.trainer_var,
            state="readonly",
            font=('Helvetica', 10),
            width=30
        )
        self.trainer_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Assignment Button
        self.assign_button = ttk.Button(
            self.form_frame,
            text="Assign Trainer",
            command=self.assign_trainer,
            style='Green.TButton'
        )
        self.assign_button.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Configure grid weights
        self.form_frame.grid_columnconfigure(1, weight=1)
    
    def create_assignments_treeview(self):
        # Create Treeview with scrollbars
        self.tree_container = ttk.Frame(self.assignments_frame)
        self.tree_container.pack(fill="both", expand=True)
        
        self.assignments_tree = ttk.Treeview(
            self.tree_container,
            columns=("class_id", "class_name", "trainer_id", "trainer_name", "date", "duration"), 
            show="headings",
            height=8
        )
        
        # Configure columns 
        self.assignments_tree.heading("class_id", text="Class ID", anchor="center")
        self.assignments_tree.heading("class_name", text="Class Name", anchor="center")
        self.assignments_tree.heading("trainer_id", text="Trainer ID", anchor="center")
        self.assignments_tree.heading("trainer_name", text="Trainer Name", anchor="center")
        self.assignments_tree.heading("date", text="Date", anchor="center")
        self.assignments_tree.heading("duration", text="Duration (min)", anchor="center")
        
        self.assignments_tree.column("class_id", width=90, anchor="center")
        self.assignments_tree.column("class_name", width=150, anchor="w")
        self.assignments_tree.column("trainer_id", width=90, anchor="center")
        self.assignments_tree.column("trainer_name", width=150, anchor="center")  # Changed to center
        self.assignments_tree.column("date", width=100, anchor="center")
        self.assignments_tree.column("duration", width=100, anchor="center")
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.assignments_tree.yview)
        x_scroll = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.assignments_tree.xview)
        self.assignments_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout
        self.assignments_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)
    
    def create_hours_treeview(self):
        # Create Treeview with scrollbars
        self.hours_container = ttk.Frame(self.hours_frame)
        self.hours_container.pack(fill="both", expand=True)
        
        self.hours_tree = ttk.Treeview(
            self.hours_container,
            columns=("trainer_id", "trainer_name", "total_hours"), 
            show="headings",
            height=8
        )
        
        # Configure columns
        self.hours_tree.heading("trainer_id", text="Trainer ID", anchor="center")
        self.hours_tree.heading("trainer_name", text="Trainer Name", anchor="center")
        self.hours_tree.heading("total_hours", text="Total Hours", anchor="center")
        
        self.hours_tree.column("trainer_id", width=100, anchor="center")
        self.hours_tree.column("trainer_name", width=150, anchor="center")  # Changed to center
        self.hours_tree.column("total_hours", width=100, anchor="center")
        
        # Add scrollbar
        y_scroll = ttk.Scrollbar(self.hours_container, orient="vertical", command=self.hours_tree.yview)
        self.hours_tree.configure(yscrollcommand=y_scroll.set)
        
        # Grid layout
        self.hours_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        
        self.hours_container.grid_columnconfigure(0, weight=1)
        self.hours_container.grid_rowconfigure(0, weight=1)
    
    def clear_trainer_fields(self): # Clears trainer form fields and shows confirmation
        """Clear all fields in the trainer form"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.trainer_id_var.set("")
        self.update_status("Fields cleared")
        messagebox.showinfo("Refresh", "Fields refreshed successfully")
    
    def on_trainer_select(self, event): # Fills form with selected trainer's data from the table
        selected_item = self.trainers_tree.selection()
        if selected_item:
            item_data = self.trainers_tree.item(selected_item, 'values')
            self.trainer_id_var.set(item_data[0])
            self.first_name_var.set(item_data[1])
            self.last_name_var.set(item_data[2])
    
    def add_trainer(self): # Adds a new trainer after validating inputs and checking for duplicates
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        trainer_id = self.trainer_id_var.get().strip()
        
        if not first_name or not last_name or not trainer_id:
            messagebox.showwarning("Input Required", "Please fill in all fields")
            return
        
        try:
            self.cursor.execute("SELECT * FROM trainers WHERE staff_id = ?", (trainer_id,))
            if self.cursor.fetchone():
                messagebox.showwarning("Duplicate ID", "This Trainer ID already exists")
                return
            
            self.cursor.execute(
                "INSERT INTO trainers (staff_id, forname, surname) VALUES (?, ?, ?)",
                (trainer_id, first_name, last_name)
            )
            self.conn.commit()
            
            self.update_status(f"Added new trainer: {first_name} {last_name} (ID: {trainer_id})")
            messagebox.showinfo("Success", "Trainer added successfully")
            
            # Clear fields without showing refresh message
            self.first_name_var.set("")
            self.last_name_var.set("")
            self.trainer_id_var.set("")
            
            self.load_trainers_list()
            self.load_data()
            
        except Exception as e:
            self.conn.rollback()
            self.update_status(f"Error adding trainer: {str(e)}")
            messagebox.showerror("Database Error", f"Failed to add trainer: {str(e)}")
    
    def update_trainer(self): # Updates selected trainer details across all related tables after validation
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        new_trainer_id = self.trainer_id_var.get().strip()
        
        if not first_name or not last_name or not new_trainer_id:
            messagebox.showwarning("Input Required", "Please fill in all fields")
            return
        
        try:
            selected_item = self.trainers_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a trainer to update")
                return
                
            original_data = self.trainers_tree.item(selected_item, 'values')
            original_trainer_id = original_data[0]
            
            if new_trainer_id != original_trainer_id:
                self.cursor.execute("SELECT * FROM trainers WHERE staff_id = ?", (new_trainer_id,))
                if self.cursor.fetchone():
                    messagebox.showwarning("Duplicate ID", "This Trainer ID already exists")
                    return
            
            with self.conn:
                self.cursor.execute(
                    "UPDATE trainers SET staff_id = ?, forname = ?, surname = ? WHERE staff_id = ?",
                    (new_trainer_id, first_name, last_name, original_trainer_id)
                )
                
                self.cursor.execute(
                    "UPDATE assignments SET trainer_id = ?, trainer_name = ? WHERE trainer_id = ?",
                    (new_trainer_id, f"{first_name} {last_name}", original_trainer_id)
                )
                
                self.cursor.execute(
                    "UPDATE trainer_hours SET trainer_id = ?, trainer_name = ? WHERE trainer_id = ?",
                    (new_trainer_id, f"{first_name} {last_name}", original_trainer_id)
                )
            
            self.update_status(f"Updated trainer: {first_name} {last_name} (ID: {new_trainer_id})")
            messagebox.showinfo("Success", "Trainer updated successfully")
            
            # Clear fields without showing refresh message
            self.first_name_var.set("")
            self.last_name_var.set("")
            self.trainer_id_var.set("")
            
            self.load_trainers_list()
            self.load_data()
            
        except Exception as e:
            self.conn.rollback()
            self.update_status(f"Error updating trainer: {str(e)}")
            messagebox.showerror("Database Error", f"Failed to update trainer: {str(e)}")
    
    def delete_trainer(self): # Deletes selected trainer after checking for existing assignments
        selected_item = self.trainers_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a trainer to delete")
            return
        
        item_data = self.trainers_tree.item(selected_item, 'values')
        trainer_id, first_name, last_name, _ = item_data
        
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this trainer?\n\n"
            f"ID: {trainer_id}\n"
            f"Name: {first_name} {last_name}"
        ):
            return
        
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM assignments WHERE trainer_id = ?",
                (trainer_id,)
            )
            assignment_count = self.cursor.fetchone()[0]
            
            if assignment_count > 0:
                messagebox.showwarning(
                    "Cannot Delete",
                    f"This trainer has {assignment_count} assignments and cannot be deleted"
                )
                return
            
            self.cursor.execute(
                "DELETE FROM trainers WHERE staff_id = ?",
                (trainer_id,)
            )
            
            self.conn.commit()
            self.update_status(f"Deleted trainer: {first_name} {last_name} (ID: {trainer_id})")
            messagebox.showinfo("Success", "Trainer deleted successfully")
            
            self.load_trainers_list()
            self.load_data()
            
        except Exception as e:
            self.conn.rollback()
            self.update_status(f"Error deleting trainer: {str(e)}")
            messagebox.showerror("Database Error", f"Failed to delete trainer: {str(e)}")
    
    def load_trainers_list(self): # Loads and displays all trainers with their assignment status
        for item in self.trainers_tree.get_children():
            self.trainers_tree.delete(item)
        
        try:
            self.cursor.execute('''
                SELECT 
                    t.staff_id, 
                    t.forname, 
                    t.surname,
                    CASE 
                        WHEN NOT EXISTS (SELECT 1 FROM trainers WHERE staff_id = t.staff_id) THEN 'New'
                        WHEN EXISTS (SELECT 1 FROM assignments WHERE trainer_id = t.staff_id) THEN 'Assigned'
                        ELSE 'Not Assigned'
                    END as status
                FROM trainers t
                ORDER BY 
                    CASE status
                        WHEN 'Assigned' THEN 1
                        WHEN 'Not Assigned' THEN 2
                        WHEN 'New' THEN 3
                        ELSE 4
                    END,
                    t.surname, t.forname
            ''')
            
            for row in self.cursor.fetchall():
                self.trainers_tree.insert("", "end", values=row)
                
        except Exception as e:
            self.update_status(f"Error loading trainers: {str(e)}")
    
    def load_data(self): # Refreshes the app by loading necessary data and updating the status
        self.update_status("Loading data...")
        
        try:
            # Load classes into combobox
            self.cursor.execute("SELECT class_id, class_name, date, time, duration FROM classes")
            classes = self.cursor.fetchall()
            class_display = [f"{c[0]} - {c[1]} ({c[2]} at {c[3]})" for c in classes]
            self.class_combobox["values"] = class_display
            self.class_data = {display: c for display, c in zip(class_display, classes)}
            
            # Load trainers into combobox
            self.cursor.execute("SELECT staff_id, forname || ' ' || surname FROM trainers")
            trainers = self.cursor.fetchall()
            trainer_display = [f"{t[0]} - {t[1]}" for t in trainers]
            self.trainer_combobox["values"] = trainer_display
            self.trainer_data = {display: t for display, t in zip(trainer_display, trainers)}
            
            # Load current assignments
            self.load_assignments()
            
            # Load hours summary
            self.load_hours_summary()
            
            # Load trainers list
            self.load_trainers_list()
            
            self.update_status("Ready")
        except Exception as e:
            self.update_status(f"Error loading data: {str(e)}")
            messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
    
    def update_class_details(self, event):   # Update the class details display when a class is selected
        selected_class = self.class_var.get()
        if selected_class in self.class_data:
            class_id, class_name, date, time, duration = self.class_data[selected_class]
            duration_min = int(duration.replace("min", "").strip())
            details = (f"Class: {class_name}\n"
                      f"ID: {class_id}\n"
                      f"Date: {date}\n"
                      f"Time: {time}\n"
                      f"Duration: {duration} ({duration_min} minutes)")
            self.class_details_label.config(text=details)
    
    def assign_trainer(self): # Assign selected trainer to selected class, update database and UI, with validation and error handling
        selected_class = self.class_var.get()
        selected_trainer = self.trainer_var.get()
        
        if not selected_class or not selected_trainer:
            self.update_status("Please select both a class and a trainer")
            messagebox.showwarning("Selection Required", "Please select both a class and a trainer")
            return
        
        class_id, class_name, date, time, duration = self.class_data[selected_class]
        trainer_id, trainer_name = self.trainer_data[selected_trainer]
        duration_min = int(duration.replace("min", "").strip())
        assignment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.cursor.execute(
                "SELECT * FROM assignments WHERE class_id = ?", 
                (class_id,)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                messagebox.showwarning("Assignment Exists", 
                                     f"This class already has {existing[4]} assigned")
                return
            
            self.cursor.execute(
                '''
                INSERT INTO assignments 
                (class_id, class_name, trainer_id, trainer_name, date, duration_minutes, assignment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (class_id, class_name, trainer_id, trainer_name, date, duration_min, assignment_date)
            )
            
            self.cursor.execute(
                '''
                INSERT INTO trainer_hours 
                (trainer_id, trainer_name, date, minutes_worked)
                VALUES (?, ?, ?, ?)
                ''',
                (trainer_id, trainer_name, date, duration_min)
            )
            
            self.conn.commit()
            self.update_status(f"Successfully assigned {trainer_name} to {class_name}")
            messagebox.showinfo("Success", 
                              f"Trainer {trainer_name} assigned to {class_name} on {date}")
            
            self.load_assignments()
            self.load_hours_summary()
            self.load_trainers_list()
            
            self.class_var.set("")
            self.trainer_var.set("")
            self.class_details_label.config(text="No class selected")
            
        except Exception as e:
            self.conn.rollback()
            self.update_status(f"Assignment failed: {str(e)}")
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    
    def delete_assignment(self): # Delete selected assignment and update trainer hours, with confirmation and error handling
        selected_item = self.assignments_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an assignment to delete")
            return
        
        item_data = self.assignments_tree.item(selected_item, 'values')
        class_id, class_name, trainer_id, trainer_name, date, duration = item_data
        
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this assignment?\n\n"
            f"Class: {class_name}\n"
            f"Trainer: {trainer_name}\n"
            f"Date: {date}"
        ):
            return
        
        try:
            self.cursor.execute(
                "DELETE FROM assignments WHERE class_id = ? AND trainer_id = ? AND date = ?",
                (class_id, trainer_id, date)
            )
            
            self.cursor.execute(
                '''
                UPDATE trainer_hours 
                SET minutes_worked = minutes_worked - ?
                WHERE trainer_id = ? AND date = ?
                ''',
                (int(duration), trainer_id, date)
            )
            
            self.cursor.execute(
                "DELETE FROM trainer_hours WHERE trainer_id = ? AND date = ? AND minutes_worked <= 0",
                (trainer_id, date)
            )
            
            self.conn.commit()
            
            self.load_assignments()
            self.load_hours_summary()
            self.load_trainers_list()
            
            self.update_status(f"Deleted assignment for {class_name} with {trainer_name}")
            messagebox.showinfo("Success", "Assignment deleted successfully")
            
        except Exception as e:
            self.conn.rollback()
            self.update_status(f"Error deleting assignment: {str(e)}")
            messagebox.showerror("Database Error", f"Failed to delete assignment: {str(e)}")
    
    def load_assignments(self): # Load all assignments from the database into the assignments treeview
        for item in self.assignments_tree.get_children():
            self.assignments_tree.delete(item)
        
        try:
            self.cursor.execute(
                '''
                SELECT class_id, class_name, trainer_id, trainer_name, date, duration_minutes 
                FROM assignments 
                ORDER BY assignment_date ASC
                '''
            )
            
            for row in self.cursor.fetchall():
                self.assignments_tree.insert("", "end", values=row)
                
        except Exception as e:
            self.update_status(f"Error loading assignments: {str(e)}")
    
    def load_hours_summary(self): # Load and display total hours worked by each trainer in the hours summary treeview
        for item in self.hours_tree.get_children():
            self.hours_tree.delete(item)
        
        try:
            self.cursor.execute(
                '''
                SELECT 
                    trainer_id, 
                    trainer_name, 
                    SUM(minutes_worked) as total_minutes
                FROM trainer_hours
                GROUP BY trainer_id, trainer_name
                ORDER BY total_minutes ASC
                '''
            )
            
            for row in self.cursor.fetchall():
                trainer_id, trainer_name, total_minutes = row
                total_hours = round(total_minutes / 60, 1)
                self.hours_tree.insert("", "end", values=(trainer_id, trainer_name, total_hours))
                
            self.update_status("Hours summary updated")
        except Exception as e:
            self.update_status(f"Error loading hours: {str(e)}")
    
    def update_status(self, message):  # Update the status label with a given message
        self.status_label.config(text=message)
    
    def __del__(self): # Ensure database connection is closed when the object is deleted
        self.conn.close()

if __name__ == "__main__": # Create the main window and run the ProfessionalTrainerAssignmentApplication                          
    root = tk.Tk()
    app = ProfessionalTrainerAssignmentApp(root)
    root.mainloop() 