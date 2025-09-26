# Import SQLite library for database operations
import sqlite3                           
# Import Tkinter for creating GUI applications
import tkinter as tk                     
# Import themed widgets and message boxes from Tkinter 
from tkinter import ttk, messagebox      
# Import datetime to handle date and time functions
from datetime import datetime            
# Import Calendar widget for date selection in the GUI
from tkcalendar import Calendar          

# Define the main class for the Gym Class Management GUI application 
class GymClassManager:                 
    # Initialize the main window with title, size, minimum size, and background color
    def __init__(self, root):           
        self.root = root
        self.root.title("FlexiGym Class Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#f0f0f0")
        
        # Database setup - create connection and cursor
        self.conn = sqlite3.connect('gym_database.db')
        self.cursor = self.conn.cursor()
        
        # Configure visual styles for the application
        self.setup_styles()
        
        # Create the header section at the top of the window
        self.create_header()
        
        # Create notebook widget for tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create the two main tabs (Staff and Member portals)
        self.create_staff_tab()
        self.create_member_tab()
        
        # Create status bar at bottom of window
        self.create_status_bar()
        
        # Load initial class data into the tables
        self.load_classes()

    def create_header(self):
        """Create the professional header with logo, title and date"""
        # Create header frame with green background
        self.header_frame = tk.Frame(self.root, bg="#2e8b57", height=60)
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # Create container for header content (left-aligned)
        self.header_content = tk.Frame(self.header_frame, bg="#2e8b57")
        self.header_content.pack(side="left", padx=20)
        
        # Add logo label
        self.logo_label = tk.Label(
            self.header_content,
            text="FLEXIGYM",
            font=('Helvetica', 14, 'bold'),
            fg="white",
            bg="#2e8b57",
            padx=5
        )
        self.logo_label.pack(side="left")
        
        # Add title label
        self.title_label = tk.Label(
            self.header_content,
            text="CLASS MANAGEMENT SYSTEM",
            font=('Helvetica', 14, 'bold'),
            fg="white",
            bg="#2e8b57",
            padx=5
        )
        self.title_label.pack(side="left")
        
        # Add current date display on the right side
        self.date_label = tk.Label(
            self.header_frame,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=('Helvetica', 10),
            fg="white",
            bg="#2e8b57",
            padx=20
        )
        self.date_label.pack(side="right")
        
        # Add separator line below header
        separator = tk.Frame(self.root, height=2, bg="#2e8b57")
        separator.pack(fill="x", pady=5)

    def create_status_bar(self):
        """Create status bar at bottom of window"""
        # Create status bar frame with green background
        self.status_bar = tk.Frame(self.root, height=25, bg="#2e8b57")
        self.status_bar.pack(fill="x", pady=(10, 0))
        
        # Create status label inside the bar
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

    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)

    def setup_styles(self):
        """Configure the visual styles for the application"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure styles for various widgets with green color scheme
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure('Header.TLabel', background="#2e8b57", foreground="white", 
                           font=('Helvetica', 14, 'bold'))
        
        # Green button style
        self.style.configure('Green.TButton', background="#2e8b57", foreground="white", 
                           font=('Helvetica', 10, 'bold'))
        
        # Red button style (for delete actions)
        self.style.configure('Red.TButton', background="#d32f2f", foreground="white", 
                           font=('Helvetica', 10, 'bold'))
        
        # Button state mappings (active, disabled states)
        self.style.map('Green.TButton', 
                      background=[('active', '#3cb371'), ('disabled', '#d3d3d3')],
                      foreground=[('active', 'white'), ('disabled', 'gray')])
        self.style.map('Red.TButton', 
                      background=[('active', '#f44336'), ('disabled', '#d3d3d3')],
                      foreground=[('active', 'white'), ('disabled', 'gray')])
        
        # Treeview (table) styling
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25, background="#f0f0f0")
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'), background="#2e8b57", foreground="white")
        self.style.map('Treeview', background=[('selected', '#2e8b57')])

    def create_staff_tab(self):
        """Create the Staff Portal tab for managing classes"""
        # Create tab frame and add to notebook
        staff_tab = ttk.Frame(self.notebook)
        self.notebook.add(staff_tab, text="Staff Portal")
        
        # Create header frame for tab
        header_frame = ttk.Frame(staff_tab, style='TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(header_frame, text="FLEXI GYM STAFF CLASS MANAGEMENT", style='Header.TLabel').pack(fill=tk.X, ipady=10)
        
        # Create main content frame (holds form and table)
        main_frame = ttk.Frame(staff_tab, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side: Form frame for class details
        self.form_frame = ttk.Frame(main_frame, style='TFrame')
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Right side: Table frame for class listings
        self.table_frame = ttk.Frame(main_frame, style='TFrame')
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create class management form
        self.create_class_form()
        
        # Create class table (Treeview widget)
        self.class_tree = ttk.Treeview(self.table_frame, 
                                     columns=('class_id', 'class_name', 'date', 'time', 'duration', 'capacity', 'difficulty_level'), 
                                     show='headings')
        
        # Configure column headings
        for col in ['class_id', 'class_name', 'date', 'time', 'duration', 'capacity', 'difficulty_level']:
            self.class_tree.heading(col, text=col.replace('_', ' ').title())
        
        # Set column widths and alignment
        self.class_tree.column('class_id', width=80, anchor=tk.CENTER)
        self.class_tree.column('class_name', width=150, anchor=tk.W)
        self.class_tree.column('date', width=100, anchor=tk.CENTER)
        self.class_tree.column('time', width=80, anchor=tk.CENTER)
        self.class_tree.column('duration', width=80, anchor=tk.CENTER)
        self.class_tree.column('capacity', width=70, anchor=tk.CENTER)
        self.class_tree.column('difficulty_level', width=100, anchor=tk.CENTER)
        
        # Pack the treeview to fill available space
        self.class_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self.class_tree, orient="vertical", command=self.class_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.class_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event to populate form when class is selected
        self.class_tree.bind('<<TreeviewSelect>>', self.on_class_select)

    def create_class_form(self):
        """Create the class management form in the Staff Portal"""
        # Form title
        form_title = ttk.Label(self.form_frame, text="Class Details", font=('Helvetica', 12, 'bold'))
        form_title.pack(pady=(0, 10))
        
        # Initialize form variables
        self.class_id_var = tk.StringVar()
        self.class_name_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.capacity_var = tk.StringVar()
        self.difficulty_var = tk.StringVar()
        
        # Define form fields with their properties
        fields = [
            ("Class ID:", self.class_id_var, ttk.Entry),
            ("Class Name:", self.class_name_var, ttk.Entry),
            ("Date:", self.date_var, ttk.Entry),
            ("Time:", self.time_var, ttk.Combobox, 
             ["7:00am", "8:00am", "9:00am", "10:00am", "11:00am", "12:00pm", "1:00pm", "2:00pm", "3:00pm", "4:00pm", "5:00pm", "6:00pm", "7:00pm"]),
            ("Duration:", self.duration_var, ttk.Combobox, 
             ["15min", "30min", "45min", "60min", "90min"]),
            ("Capacity:", self.capacity_var, ttk.Spinbox, (1, 50)),
            ("Difficulty Level:", self.difficulty_var, ttk.Combobox, 
             ["Beginner", "Intermediate", "Advanced"])
        ]
        
        # Create form fields dynamically based on the fields definition
        for label, var, widget_type, *args in fields:
            # Add label for each field
            ttk.Label(self.form_frame, text=label).pack(anchor=tk.W)
            
            # Create appropriate widget based on type
            if widget_type == ttk.Combobox:
                entry = widget_type(self.form_frame, textvariable=var, values=args[0])
            elif widget_type == ttk.Spinbox:
                entry = widget_type(self.form_frame, textvariable=var, from_=args[0][0], to=args[0][1])
            else:
                entry = widget_type(self.form_frame, textvariable=var)
            entry.pack(fill=tk.X, pady=(0, 10))
            
            # Special case: Add calendar button for date field
            if label == "Date:":
                ttk.Button(self.form_frame, text="Select Date", command=self.select_date, 
                          style='Green.TButton').pack(fill=tk.X, pady=(0, 10))
        
        # Create frame for action buttons
        button_frame = ttk.Frame(self.form_frame)
        button_frame.pack(fill=tk.X)
        
        # Add action buttons with appropriate commands
        self.add_button = ttk.Button(button_frame, text="Add Class", command=self.add_class, style='Green.TButton')
        self.add_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.update_button = ttk.Button(button_frame, text="Update Class", command=self.update_class, style='Green.TButton')
        self.update_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.delete_button = ttk.Button(button_frame, text="Delete Class", command=self.delete_class, style='Red.TButton')
        self.delete_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_data, style='Green.TButton')
        self.refresh_button.pack(side=tk.LEFT, expand=True, padx=2)

    def create_member_tab(self):
        """Create the Member Portal tab for class signups"""
        # Create tab frame and add to notebook
        member_tab = ttk.Frame(self.notebook)
        self.notebook.add(member_tab, text="Member Portal")
        
        # Create header frame for tab
        header_frame = ttk.Frame(member_tab, style='TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(header_frame, text="MEMBER CLASS SIGNUP FOR FLEXI GYM", style='Header.TLabel').pack(fill=tk.X, ipady=10)
        
        # Create main content frame (holds signup form and class list)
        main_frame = ttk.Frame(member_tab, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # LEFT SIDE: Signup form frame
        signup_frame = ttk.Frame(main_frame, style='TFrame', padding=10)
        signup_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        # Form container with padding
        form_container = ttk.Frame(signup_frame, style='TFrame', padding=15)
        form_container.pack(fill=tk.BOTH, expand=True)
        
        # Member ID field
        ttk.Label(form_container, text="Member ID:", font=('Helvetica', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.member_id_entry = ttk.Entry(form_container, width=25)
        self.member_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Class ID field (combobox for dropdown selection)
        ttk.Label(form_container, text="Class ID:", font=('Helvetica', 10)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.signup_class_entry = ttk.Combobox(form_container, width=23)
        self.signup_class_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # Populate class IDs in dropdown from database
        self.cursor.execute("SELECT class_id FROM classes")
        class_ids = [row[0] for row in self.cursor.fetchall()]
        self.signup_class_entry['values'] = class_ids
        
        # Signup button
        signup_btn = ttk.Button(form_container, text="SIGN UP", command=self.member_signup, 
                               style='Green.TButton', width=20)
        signup_btn.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Configure grid weights for proper resizing
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_columnconfigure(1, weight=1)
        
        # RIGHT SIDE: Class list frame
        class_list_frame = ttk.Frame(main_frame, style='TFrame')
        class_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create class table (Treeview widget)
        self.member_class_tree = ttk.Treeview(class_list_frame, 
                                           columns=('class_id', 'class_name', 'date', 'time', 'duration', 'capacity', 'difficulty_level'), 
                                           show='headings')
        
        # Configure column headings
        for col in ['class_id', 'class_name', 'date', 'time', 'duration', 'capacity', 'difficulty_level']:
            self.member_class_tree.heading(col, text=col.replace('_', ' ').title())
        
        # Set column widths and alignment
        self.member_class_tree.column('class_id', width=80, anchor=tk.CENTER)
        self.member_class_tree.column('class_name', width=150, anchor=tk.W)
        self.member_class_tree.column('date', width=100, anchor=tk.CENTER)
        self.member_class_tree.column('time', width=80, anchor=tk.CENTER)
        self.member_class_tree.column('duration', width=80, anchor=tk.CENTER)
        self.member_class_tree.column('capacity', width=70, anchor=tk.CENTER)
        self.member_class_tree.column('difficulty_level', width=100, anchor=tk.CENTER)
        
        # Pack the treeview to fill available space
        self.member_class_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self.member_class_tree, orient="vertical", command=self.member_class_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.member_class_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event to auto-fill class ID when member selects a class
        self.member_class_tree.bind('<<TreeviewSelect>>', self.on_member_class_select)

    def load_classes(self):
        """Load classes from database into both staff and member tables"""
        # Clear existing data from both tables
        for item in self.class_tree.get_children():
            self.class_tree.delete(item)
        for item in self.member_class_tree.get_children():
            self.member_class_tree.delete(item)
        
        # Fetch all classes from database
        self.cursor.execute("SELECT * FROM classes")
        classes = self.cursor.fetchall()
        
        # Insert classes into staff treeview 
        for cls in classes:
            self.class_tree.insert('', tk.END, values=cls)
        
        # Insert classes into member treeview with available capacity 
        for cls in classes:
            class_id = cls[0]
            # Get current signups count for this class
            self.cursor.execute("SELECT COUNT(*) FROM member_class WHERE class_id=?", (class_id,))
            signups = self.cursor.fetchone()[0]
            # Calculate available capacity (total capacity - current signups)
            available_capacity = cls[5] - signups
            # Insert with capacity display showing available/total
            self.member_class_tree.insert('', tk.END, values=(cls[0], cls[1], cls[2], cls[3], cls[4], f"{available_capacity}/{cls[5]}", cls[6]))

        # Update class ID dropdown in member portal
        if hasattr(self, 'signup_class_entry'):
            self.cursor.execute("SELECT class_id FROM classes")
            class_ids = [row[0] for row in self.cursor.fetchall()]
            self.signup_class_entry['values'] = class_ids

    def refresh_data(self):
        """Refresh the class data from database"""
        self.load_classes()
        self.clear_form()
        self.update_status("Data refreshed successfully")
        messagebox.showinfo("Info", "Data refreshed successfully")

    def clear_form(self):
        """Clear all form fields in the staff portal"""
        self.class_id_var.set('')
        self.class_name_var.set('')
        self.date_var.set('')
        self.time_var.set('')
        self.duration_var.set('')
        self.capacity_var.set('')
        self.difficulty_var.set('')
        
        # Clear any selection in the class tree
        self.class_tree.selection_remove(self.class_tree.selection())

    def select_date(self):
        """Open calendar popup to select date for class"""
        # Create popup window
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(padx=10, pady=10)
        
        def set_date():
            """Callback function to set selected date and close popup"""
            self.date_var.set(cal.get_date())
            top.destroy()
            
        # Add select button to calendar popup
        ttk.Button(top, text="Select", command=set_date, style='Green.TButton').pack(pady=5)

    def on_class_select(self, event):
        """Populate form fields when a class is selected in the staff portal"""
        selected = self.class_tree.focus()
        if not selected:
            return
            
        # Get values from selected row
        values = self.class_tree.item(selected, 'values')
        if values:
            # Set form variables with selected class data
            self.class_id_var.set(values[0])
            self.class_name_var.set(values[1])
            self.date_var.set(values[2])
            self.time_var.set(values[3])
            self.duration_var.set(values[4])
            self.capacity_var.set(values[5])
            self.difficulty_var.set(values[6])

    def on_member_class_select(self, event):
        """Auto-fill class ID when member selects a class in the member portal"""
        selected = self.member_class_tree.focus()
        if selected:
            # Get values from selected row and set class ID in combobox
            values = self.member_class_tree.item(selected, 'values')
            self.signup_class_entry.set(values[0])  # class_id

    def validate_class_form(self):
        """Validate all fields in the class form before submission"""
        if not self.class_id_var.get():
            self.update_status("Error: Class ID is required")
            messagebox.showerror("Error", "Class ID is required")
            return False
        if not self.class_name_var.get():
            self.update_status("Error: Class name is required")
            messagebox.showerror("Error", "Class name is required")
            return False
        if not self.date_var.get():
            self.update_status("Error: Date is required")
            messagebox.showerror("Error", "Date is required")
            return False
        if not self.time_var.get():
            self.update_status("Error: Time is required")
            messagebox.showerror("Error", "Time is required")
            return False
        if not self.duration_var.get():
            self.update_status("Error: Duration is required")
            messagebox.showerror("Error", "Duration is required")
            return False
        if not self.capacity_var.get():
            self.update_status("Error: Capacity is required")
            messagebox.showerror("Error", "Capacity is required")
            return False
        if not self.difficulty_var.get():
            self.update_status("Error: Difficulty level is required")
            messagebox.showerror("Error", "Difficulty level is required")
            return False
        return True

    def add_class(self):
        """Add a new class to the database"""
        # First validate form fields
        if not self.validate_class_form():
            return
            
        try:
            # Insert new class record into database
            self.cursor.execute('''
                INSERT INTO classes VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.class_id_var.get(),
                self.class_name_var.get(),
                self.date_var.get(),
                self.time_var.get(),
                self.duration_var.get(),
                int(self.capacity_var.get()),
                self.difficulty_var.get()
            ))
            self.conn.commit()
            
            # Refresh data to show new class 
            self.load_classes()
            
            self.update_status(f"Class {self.class_id_var.get()} added successfully")
            messagebox.showinfo("Success", "Class added successfully")
            self.clear_form()
            
            # Scroll to the bottom to show the newly added class
            self.class_tree.see(self.class_tree.get_children()[-1])
            self.member_class_tree.see(self.member_class_tree.get_children()[-1])
            
        except sqlite3.IntegrityError:
            # Handle case where class ID already exists
            self.update_status(f"Error: Class ID {self.class_id_var.get()} already exists")
            messagebox.showerror("Error", "Class ID already exists")
        except Exception as e:
            # Handle any other errors
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_class(self):
        """Update an existing class in the database"""
        # First validate form fields
        if not self.validate_class_form():
            return
            
        # Get the original class ID from the selection
        selected = self.class_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No class selected")
            return
            
        original_values = self.class_tree.item(selected, 'values')
        original_class_id = original_values[0]
        new_class_id = self.class_id_var.get()
            
        try:
            # Check if class ID is being changed to one that already exists
            if new_class_id != original_class_id:
                self.cursor.execute("SELECT 1 FROM classes WHERE class_id=?", (new_class_id,))
                if self.cursor.fetchone():
                    messagebox.showerror("Error", "New Class ID already exists")
                    return

            # Update the class record with all fields
            self.cursor.execute('''
                UPDATE classes SET
                class_id = ?,
                class_name = ?,
                date = ?,
                time = ?,
                duration = ?,
                capacity = ?,
                difficulty_level = ?
                WHERE class_id = ?
            ''', (
                new_class_id,
                self.class_name_var.get(),
                self.date_var.get(),
                self.time_var.get(),
                self.duration_var.get(),
                int(self.capacity_var.get()),
                self.difficulty_var.get(),
                original_class_id
            ))

            # If class ID was changed, update all related member_class records
            if new_class_id != original_class_id:
                self.cursor.execute('''
                    UPDATE member_class SET
                    class_id = ?
                    WHERE class_id = ?
                ''', (new_class_id, original_class_id))

            self.conn.commit()
            self.update_status(f"Class {original_class_id} updated to {new_class_id} successfully")
            messagebox.showinfo("Success", "Class updated successfully")
            self.load_classes()
            self.clear_form()
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_class(self):
        """Delete a class from the database"""
        # Confirm deletion with user
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this class?"):
            return
            
        try:
            # First delete all signups for this class
            self.cursor.execute("DELETE FROM member_class WHERE class_id=?", (self.class_id_var.get(),))
            # Then delete the class itself
            self.cursor.execute("DELETE FROM classes WHERE class_id=?", (self.class_id_var.get(),))
            self.conn.commit()
            self.update_status(f"Class {self.class_id_var.get()} deleted successfully")
            messagebox.showinfo("Success", "Class deleted successfully")
            self.load_classes()
            self.clear_form()
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def member_signup(self):
        """Sign up a member for a class"""
        # Get member and class IDs from form
        member_id = self.member_id_entry.get()
        class_id = self.signup_class_entry.get()
        
        # Validate input
        if not member_id:
            self.update_status("Error: Member ID is required")
            messagebox.showerror("Error", "Member ID is required")
            return
        if not class_id:
            self.update_status("Error: Class ID is required")
            messagebox.showerror("Error", "Class ID is required")
            return
            
        # Check if member exists in database
        self.cursor.execute("SELECT 1 FROM members WHERE member_id=?", (member_id,))
        if not self.cursor.fetchone():
            self.update_status(f"Error: Member ID {member_id} not found")
            messagebox.showerror("Error", "Member ID not found")
            return
            
        # Check if class exists and get its capacity
        self.cursor.execute("SELECT capacity FROM classes WHERE class_id=?", (class_id,))
        class_data = self.cursor.fetchone()
        if not class_data:
            self.update_status(f"Error: Class ID {class_id} not found")
            messagebox.showerror("Error", "Class ID not found")
            return
            
        capacity = class_data[0]
        
        # Check if member is already signed up for this class
        self.cursor.execute("SELECT 1 FROM member_class WHERE member_id=? AND class_id=?", (member_id, class_id))
        if self.cursor.fetchone():
            self.update_status(f"Error: Member {member_id} already signed up for class {class_id}")
            messagebox.showerror("Error", "Member is already signed up for this class")
            return
            
        # Check if class has available capacity
        self.cursor.execute("SELECT COUNT(*) FROM member_class WHERE class_id=?", (class_id,))
        signups = self.cursor.fetchone()[0]
        if signups >= capacity:
            self.update_status(f"Error: Class {class_id} is already full")
            messagebox.showerror("Error", "Class is already full")
            return
            
        # Process signup
        try:
            # Get current date/time for signup record
            signup_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            # Insert signup record
            self.cursor.execute('''
                INSERT INTO member_class VALUES (?, ?, ?)
            ''', (member_id, class_id, signup_date))
            self.conn.commit()
            self.update_status(f"Member {member_id} signed up for class {class_id} successfully")
            messagebox.showinfo("Success", "Member signed up successfully")
            # Clear form fields
            self.member_id_entry.delete(0, tk.END)
            self.signup_class_entry.delete(0, tk.END)
            # Refresh data to show updated capacity
            self.load_classes()
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def __del__(self):
        """Clean up database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Main entry point
if __name__ == "__main__":
    # Create main Tkinter window
    root = tk.Tk()
    # Create application instance
    app = GymClassManager(root)
    # Start main event loop
    root.mainloop()