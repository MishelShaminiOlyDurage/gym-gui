import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Database utility functions
def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect("gym_database.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def initialize_database():
    """Initialize the database with required tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                member_id TEXT UNIQUE NOT NULL,
                remember_me BOOLEAN DEFAULT 0
            )
        ''')
        
        # Create staff table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                staff_id TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                remember_me BOOLEAN DEFAULT 0
            )
        ''')
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    """Execute a SQL query with parameters"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
        
        conn.commit()
        return result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Initialize database
initialize_database()

# Color scheme
BG_COLOR = "#4CAF50"  # Green background
FG_COLOR = "#000000"  # Black text for labels
BUTTON_COLOR = "#000000"  # Black buttons
ACTIVE_BUTTON_COLOR = "#333333"  # Darker black for active buttons
ENTRY_BG = "#000000"  # Black for entry widgets
ENTRY_FG = "#4CAF50"  # Green text in entry widgets
BUTTON_TEXT_COLOR = "#FFFFFF"  # White text on black buttons

# Style dictionaries
style = {
    "bg": BG_COLOR,
    "fg": FG_COLOR,
    "font": ("Arial", 12),
    "activebackground": ACTIVE_BUTTON_COLOR,
    "activeforeground": BUTTON_TEXT_COLOR,
    "highlightbackground": BG_COLOR,
    "highlightcolor": BG_COLOR
}

button_style = {
    "bg": BUTTON_COLOR,
    "fg": BUTTON_TEXT_COLOR,
    "font": ("Arial", 12),
    "activebackground": ACTIVE_BUTTON_COLOR,
    "activeforeground": BUTTON_TEXT_COLOR,
    "relief": tk.RAISED,
    "borderwidth": 2,
    "padx": 10,
    "pady": 5
}

# Global variables
current_user = None
current_staff = None

# User management functions
def load_remembered_user():
    result = execute_query(
        "SELECT username FROM members WHERE remember_me = 1",
        fetch_one=True
    )
    return result['username'] if result else None

def load_remembered_staff():
    result = execute_query(
        "SELECT username FROM staff WHERE remember_me = 1",
        fetch_one=True
    )
    return result['username'] if result else None

def save_remembered_user(username):
    execute_query("UPDATE members SET remember_me = 0")
    execute_query(
        "UPDATE members SET remember_me = 1 WHERE username = ?",
        (username,)
    )

def save_remembered_staff(username):
    execute_query("UPDATE staff SET remember_me = 0")
    execute_query(
        "UPDATE staff SET remember_me = 1 WHERE username = ?",
        (username,)
    )

def clear_remembered_user():
    execute_query("UPDATE members SET remember_me = 0")

def clear_remembered_staff():
    execute_query("UPDATE staff SET remember_me = 0")

# Login functions
def login():
    global current_user
    username_or_id = entry_username.get().strip()
    password = entry_password.get().strip()

    try:
        user = execute_query(
            "SELECT * FROM members WHERE (username = ? OR member_id = ?) AND password = ?",
            (username_or_id, username_or_id, password),
            fetch_one=True
        )
        
        if user:
            current_user = user['username']
            if remember_me_var.get():
                save_remembered_user(current_user)
            else:
                clear_remembered_user()
            
            messagebox.showinfo("Login Success", f"Welcome to Flexi Gym, {current_user}!")
            login_window.destroy()
            show_user_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username, member ID, or password!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def staff_login():
    global current_staff
    username_or_id = entry_staff_username.get().strip()
    password = entry_staff_password.get().strip()

    try:
        staff_member = execute_query(
            "SELECT * FROM staff WHERE (username = ? OR staff_id = ?) AND password = ?",
            (username_or_id, username_or_id, password),
            fetch_one=True
        )
        
        if staff_member:
            current_staff = staff_member['username']
            if staff_remember_me_var.get():
                save_remembered_staff(current_staff)
            else:
                clear_remembered_staff()
            
            messagebox.showinfo("Staff Login Success", f"Welcome back, {staff_member['role']} {current_staff}!")
            staff_login_window.destroy()
            show_staff_dashboard(staff_member['role'])
        else:
            messagebox.showerror("Login Failed", "Invalid username, staff ID, or password!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Registration functions
def register():
    email = entry_new_email.get().strip()
    username = entry_new_username.get().strip()
    password = entry_new_password.get().strip()
    member_id = entry_new_member_id.get().strip()

    if not all([email, username, password, member_id]):
        messagebox.showerror("Registration Failed", "Please fill in all fields.")
        return

    try:
        # Check if email is already registered
        if execute_query("SELECT 1 FROM members WHERE email = ?", (email,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Email already registered! Use another email.")
            return

        # Check if username exists
        if execute_query("SELECT 1 FROM members WHERE username = ?", (username,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Username already exists! Choose another.")
            return

        # Check if member ID exists
        if execute_query("SELECT 1 FROM members WHERE member_id = ?", (member_id,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Member ID already exists! Choose another.")
            return

        # Insert new member
        execute_query(
            "INSERT INTO members (username, email, password, member_id) VALUES (?, ?, ?, ?)",
            (username, email, password, member_id)
        )

        messagebox.showinfo("Registration Successful", "You can now log in!")
        register_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")

def staff_register():
    email = entry_staff_email.get().strip()
    username = entry_staff_username_reg.get().strip()
    password = entry_staff_password_reg.get().strip()
    staff_id = entry_staff_id.get().strip()
    role = entry_staff_role.get().strip()

    if not all([email, username, password, staff_id, role]):
        messagebox.showerror("Registration Failed", "Please fill in all fields.")
        return

    try:
        # Validate work email
        if not email.endswith("@flexigym.com"):
            messagebox.showerror("Registration Failed", "Please use your official Flexi Gym work email (@flexigym.com).")
            return

        # Check if email is already registered
        if execute_query("SELECT 1 FROM staff WHERE email = ?", (email,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Email already registered! Use another email.")
            return

        # Check if username exists
        if execute_query("SELECT 1 FROM staff WHERE username = ?", (username,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Username already exists! Choose another.")
            return

        # Check if staff ID exists
        if execute_query("SELECT 1 FROM staff WHERE staff_id = ?", (staff_id,), fetch_one=True):
            messagebox.showerror("Registration Failed", "Staff ID already exists! Choose another.")
            return

        # Insert new staff member
        execute_query(
            "INSERT INTO staff (username, email, password, staff_id, role) VALUES (?, ?, ?, ?, ?)",
            (username, email, password, staff_id, role)
        )

        messagebox.showinfo("Registration Successful", "Staff account created successfully!")
        staff_register_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")

# Logout functions
def logout():
    global current_user
    current_user = None
    clear_remembered_user()
    messagebox.showinfo("Logout", "You have been logged out.")

def staff_logout():
    global current_staff
    current_staff = None
    clear_remembered_staff()
    messagebox.showinfo("Staff Logout", "You have been logged out.")

# Window management functions
def open_login_window():
    global login_window, entry_username, entry_password, remember_me_var
    login_window = tk.Toplevel(welcome_window)
    login_window.title("Flexi Gym - Member Login")
    login_window.configure(bg=BG_COLOR)
    
    # Add Update Info button in top right
    update_button = tk.Button(
        login_window, 
        text="Update User Information", 
        **button_style,
        command=open_update_user_window
    )
    update_button.pack(anchor=tk.NE, padx=10, pady=10)
    
    main_frame = tk.Frame(login_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Username or Member ID:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_username = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_username.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Password:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_password = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_password.pack(pady=5)

    remember_me_var = tk.BooleanVar()
    tk.Checkbutton(
        main_frame, 
        text="Remember Me", 
        variable=remember_me_var,
        bg=BG_COLOR,
        fg=FG_COLOR,
        activebackground=BG_COLOR,
        activeforeground=FG_COLOR,
        selectcolor=BG_COLOR
    ).pack(pady=5)

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    tk.Button(
        button_frame, 
        text="Login", 
        **button_style,
        command=login
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        button_frame, 
        text="Register", 
        **button_style,
        command=open_register_window
    ).pack(side=tk.LEFT, padx=5)

def open_update_user_window():
    update_window = tk.Toplevel(welcome_window)
    update_window.title("Flexi Gym - Update User Information")
    update_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(update_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Current Username or Member ID:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_current_id = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_current_id.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Current Password:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_current_pass = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_current_pass.pack(pady=5)

    tk.Label(
        main_frame, 
        text="New Email (leave blank to keep current):", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_email = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_email.pack(pady=5)

    tk.Label(
        main_frame, 
        text="New Username (leave blank to keep current):", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_username = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_username.pack(pady=5)

    tk.Label(
        main_frame, 
        text="New Password (leave blank to keep current):", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_password = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_password.pack(pady=5)

    def update_user_info():
        current_id = entry_current_id.get().strip()
        current_pass = entry_current_pass.get().strip()
        new_email = entry_new_email.get().strip()
        new_username = entry_new_username.get().strip()
        new_password = entry_new_password.get().strip()
        
        try:
            # Find the user
            user = execute_query(
                "SELECT * FROM members WHERE (username = ? OR member_id = ?) AND password = ?",
                (current_id, current_id, current_pass),
                fetch_one=True
            )
            
            if not user:
                messagebox.showerror("Error", "Invalid credentials!")
                return
            
            current_username = user['username']
            current_data = {
                "email": user['email'],
                "password": user['password'],
                "member_id": user['member_id']
            }
            
            # Check if new email is provided and not used by others
            if new_email:
                if execute_query("SELECT 1 FROM members WHERE email = ? AND username != ?", (new_email, current_username), fetch_one=True):
                    messagebox.showerror("Error", "Email already in use by another account!")
                    return
                current_data['email'] = new_email
            
            # Check if new password is provided
            if new_password:
                current_data['password'] = new_password
            
            # Handle username change
            if new_username and new_username != current_username:
                if execute_query("SELECT 1 FROM members WHERE username = ?", (new_username,), fetch_one=True):
                    messagebox.showerror("Error", "Username already taken!")
                    return
                
                # Update username
                execute_query(
                    "UPDATE members SET username = ? WHERE username = ?",
                    (new_username, current_username)
                )
                current_username = new_username
            
            # Update other fields
            execute_query(
                "UPDATE members SET email = ?, password = ? WHERE username = ?",
                (current_data['email'], current_data['password'], current_username)
            )
            
            messagebox.showinfo("Success", "User information updated successfully!")
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    tk.Button(
        main_frame, 
        text="Update Information", 
        **button_style,
        command=update_user_info
    ).pack(pady=10)

def show_user_dashboard():
    user_window = tk.Toplevel(welcome_window)
    user_window.title("Flexi Gym - Member Dashboard")
    user_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(user_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Member Dashboard", 
        font=("Arial", 16, "bold"),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=10)
    
    tk.Label(
        main_frame, 
        text=f"Welcome, {current_user}!", 
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    try:
        user_info = execute_query(
            "SELECT email, member_id FROM members WHERE username = ?",
            (current_user,),
            fetch_one=True
        )
        
        tk.Label(
            main_frame, 
            text=f"Email: {user_info['email']}", 
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=5)
        
        tk.Label(
            main_frame, 
            text=f"Member ID: {user_info['member_id']}", 
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load user information: {str(e)}")

    tk.Button(
        main_frame, 
        text="Logout", 
        **button_style,
        command=lambda: [user_window.destroy(), logout()]
    ).pack(pady=20)

def open_staff_login_window():
    global staff_login_window, entry_staff_username, entry_staff_password, staff_remember_me_var
    staff_login_window = tk.Toplevel(welcome_window)
    staff_login_window.title("Flexi Gym - Staff Login")
    staff_login_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(staff_login_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Username or Staff ID:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_username = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_username.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Password:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_password = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_password.pack(pady=5)

    staff_remember_me_var = tk.BooleanVar()
    tk.Checkbutton(
        main_frame, 
        text="Remember Me", 
        variable=staff_remember_me_var,
        bg=BG_COLOR,
        fg=FG_COLOR,
        activebackground=BG_COLOR,
        activeforeground=FG_COLOR,
        selectcolor=BG_COLOR
    ).pack(pady=5)

    tk.Button(
        main_frame, 
        text="Login", 
        **button_style,
        command=staff_login
    ).pack(pady=10)

def open_register_window():
    global register_window, entry_new_email, entry_new_username, entry_new_password, entry_new_member_id
    register_window = tk.Toplevel(welcome_window)
    register_window.title("Flexi Gym - Member Registration")
    register_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(register_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Email:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_email = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_email.pack(pady=5)

    tk.Label(
        main_frame, 
        text="New Username:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_username = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_username.pack(pady=5)

    tk.Label(
        main_frame, 
        text="New Password:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_password = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_password.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Member ID:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_new_member_id = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_new_member_id.pack(pady=5)

    tk.Button(
        main_frame, 
        text="Register", 
        **button_style,
        command=register
    ).pack(pady=10)

def open_staff_register_window():
    global staff_register_window, entry_staff_email, entry_staff_username_reg, entry_staff_password_reg, entry_staff_id, entry_staff_role
    staff_register_window = tk.Toplevel(welcome_window)
    staff_register_window.title("Flexi Gym - Staff Registration")
    staff_register_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(staff_register_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text="Work Email (@flexigym.com):", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_email = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_email.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Username:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_username_reg = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_username_reg.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Password:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_password_reg = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        show="*", 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_password_reg.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Staff ID:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_id = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_id.pack(pady=5)

    tk.Label(
        main_frame, 
        text="Role:", 
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    entry_staff_role = tk.Entry(
        main_frame, 
        font=("Arial", 12), 
        bg=ENTRY_BG,
        fg=ENTRY_FG,
        insertbackground=ENTRY_FG
    )
    entry_staff_role.pack(pady=5)

    tk.Button(
        main_frame, 
        text="Register", 
        **button_style,
        command=staff_register
    ).pack(pady=10)

def show_staff_dashboard(role):
    staff_window = tk.Toplevel(welcome_window)
    staff_window.title(f"Flexi Gym - {role} Dashboard")
    staff_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(staff_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)

    tk.Label(
        main_frame, 
        text=f"{role} Dashboard", 
        font=("Arial", 16, "bold"),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=10)
    
    tk.Label(
        main_frame, 
        text=f"Welcome, {current_staff}!", 
        font=("Arial", 14),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    # Member Management section
    tk.Label(
        main_frame, 
        text="Member Management:", 
        font=("Arial", 12, "underline"),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    button_frame1 = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame1.pack(pady=5)
    
    tk.Button(
        button_frame1, 
        text="View Members", 
        **button_style,
        command=view_members
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        button_frame1, 
        text="Check Member Status", 
        **button_style
    ).pack(side=tk.LEFT, padx=5)
    
    # Gym Operations section
    tk.Label(
        main_frame, 
        text="Gym Operations:", 
        font=("Arial", 12, "underline"),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)
    
    button_frame2 = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame2.pack(pady=5)
    
    tk.Button(
        button_frame2, 
        text="Equipment Status", 
        **button_style
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        button_frame2, 
        text="Class Schedule", 
        **button_style
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        main_frame, 
        text="Logout", 
        **button_style,
        command=lambda: [staff_window.destroy(), staff_logout()]
    ).pack(pady=20)

def view_members():
    view_window = tk.Toplevel(welcome_window)
    view_window.title("Flexi Gym - Member List")
    view_window.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(view_window, bg=BG_COLOR)
    main_frame.pack(padx=20, pady=20)
    
    try:
        members = execute_query(
            "SELECT username, email, member_id FROM members",
            fetch_all=True
        )
        
        if not members:
            tk.Label(
                main_frame, 
                text="No members registered yet.", 
                font=("Arial", 12),
                bg=BG_COLOR,
                fg=FG_COLOR
            ).pack(pady=20)
        else:
            tk.Label(
                main_frame, 
                text="Registered Members:", 
                font=("Arial", 14, "bold"),
                bg=BG_COLOR,
                fg=FG_COLOR
            ).pack(pady=10)
            
            frame = tk.Frame(main_frame, bg=BG_COLOR)
            frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            member_list = tk.Listbox(
                frame, 
                yscrollcommand=scrollbar.set, 
                font=("Arial", 12), 
                width=60,
                bg=ENTRY_BG,
                fg=ENTRY_FG
            )
            
            for member in members:
                member_list.insert(tk.END, f"Username: {member['username']} | Email: {member['email']} | Member ID: {member['member_id']}")
            
            member_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=member_list.yview)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load members: {str(e)}")

# Create the welcome screen
welcome_window = tk.Tk()
welcome_window.title("Flexi Gym")
welcome_window.geometry("450x500")
welcome_window.configure(bg=BG_COLOR)

# Welcome labels
tk.Label(
    welcome_window, 
    text="🏋️ Flexi Gym 🏋️", 
    font=("Arial", 18, "bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
).pack(pady=20)

tk.Label(
    welcome_window, 
    text="Your fitness journey starts here!", 
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=FG_COLOR
).pack(pady=10)

# Member login button
tk.Button(
    welcome_window, 
    text="Member Login", 
    **button_style,
    command=open_login_window
).pack(pady=5)

# Staff login button
tk.Button(
    welcome_window, 
    text="Staff Login", 
    **button_style,
    command=open_staff_login_window
).pack(pady=5)

# Member registration button
tk.Button(
    welcome_window, 
    text="Member Registration", 
    **button_style,
    command=open_register_window
).pack(pady=5)

# Staff registration button
tk.Button(
    welcome_window, 
    text="Staff Registration", 
    **button_style,
    command=open_staff_register_window
).pack(pady=5)

# About button
tk.Button(
    welcome_window, 
    text="About Gym", 
    **button_style
).pack(pady=5)

welcome_window.mainloop()