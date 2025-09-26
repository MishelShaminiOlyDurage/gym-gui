import tkinter as tk  # Import the Tkinter library for GUI creation
from tkinter import font as tkfont, messagebox  # Import font management and message boxes
import os  # Import OS module to interact with the file system
import subprocess  # Import subprocess to run external Python scripts

class SprintNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title("FLEXI GYM System")  # Set window title for the application
        self.root.geometry("1100x750")  # Set fixed window size
        self.root.configure(bg="#f8faf9")  # Set background color

        # Configure root grid layout so content area expands correctly
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Define colors for consistent application theme
        self.primary_green = "#2e8b57"
        self.light_bg = "#e8f5e9"
        self.white = "#ffffff"
        self.primary_orange = "#ff8c00"

        # Dictionary to track subprocesses running sprint modules
        self.sprint_processes = {}

        # Create main sections of the application interface
        self.create_header()
        self.create_main_menu()
        self.create_footer()

    def create_header(self):
        # Create header frame with a fixed height and primary green background
        self.header = tk.Frame(self.root, bg=self.primary_green, height=40)
        self.header.grid(row=0, column=0, sticky="nsew")

        title_frame = tk.Frame(self.header, bg=self.primary_green)
        title_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Application title label in header
        self.title_label = tk.Label(
            title_frame,
            text="FLEXI GYM",
            font=("Montserrat", 22, "bold"),  # Title font style and size
            fg="white",
            bg=self.primary_green
        )
        self.title_label.pack()

    def create_main_menu(self):
        # Create the main menu frame with light background
        self.main_menu_frame = tk.Frame(self.root, bg=self.light_bg)
        self.main_menu_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        grid_frame = tk.Frame(self.main_menu_frame, bg=self.light_bg)
        grid_frame.pack(fill="both", expand=True, padx=60, pady=40)

        # List of sprint modules with details to display in the application
        sprints = [
            {"num": 1, "title": "Member Management Functionality ", "icon": "👤", "desc": "Manages staff and member profiles through secure sign-up and login."},
            {"num": 2, "title": "Membership Plans and Billings", "icon": "💳", "desc": "Handles membership subscriptions and payments efficiently."},
            {"num": 3, "title": "Class and Activity scheduling ", "icon": "📅", "desc": "Schedules and organises all fitness classes and activities smoothly."},
            {"num": 4, "title": "Assign trainers and track hours", "icon": "⏰", "desc": "Assigns trainers to classes and track their working hours accurately."}
        ]

        # Create cards for each sprint module in a grid layout
        for i, sprint in enumerate(sprints):
            card = self.create_sprint_card(grid_frame, sprint)
            card.grid(row=i//2, column=i%2, padx=25, pady=25, sticky="nsew")
            grid_frame.grid_columnconfigure(i % 2, weight=1)
            grid_frame.grid_rowconfigure(i // 2, weight=1)

        # Add a motivational quote at the bottom of the main menu
        quote = tk.Label(
            self.main_menu_frame,
            text="""Your body can stand almost anything. It's your mind that you have to convince.""",
            bg=self.light_bg,
            fg="#4e6e5d",
            font=("Montserrat", 11, "italic")
        )
        quote.pack(side="bottom", pady=(10, 20))

    def create_sprint_card(self, parent, sprint):
        # Create individual sprint card frame with white background and border
        card = tk.Frame(
            parent,
            bg=self.white,
            highlightbackground="#cccccc",
            highlightthickness=1,
            bd=0,
            relief="groove",
            width=250
        )

        # Colored header bar for the card
        header = tk.Frame(card, bg=self.primary_green, height=6)
        header.pack(fill="x")

        # Content area inside the card with padding
        content = tk.Frame(card, bg=self.white, padx=25, pady=20)
        content.pack(fill="both", expand=True)

        top_frame = tk.Frame(content, bg=self.white)
        top_frame.pack(fill="x", pady=(0, 15))

        # Icon label showing sprint emoji
        tk.Label(
            top_frame,
            text=sprint["icon"],
            font=("Segoe UI Emoji", 30),
            bg=self.white
        ).pack(side="left")

        # Sprint title label
        tk.Label(
            content,
            text=sprint["title"],
            font=("Montserrat", 17, "bold"),
            fg=self.primary_green,
            bg=self.white
        ).pack(anchor="w", pady=(0, 5))

        # Sprint description label
        tk.Label(
            content,
            text=sprint["desc"],
            font=("Montserrat", 10),
            fg="#555555",
            bg=self.white
        ).pack(anchor="w", pady=(0, 15))

        # Button to open the sprint application module
        open_btn = tk.Button(
            content,
            text="OPEN →",
            font=("Montserrat", 11, "bold"),
            fg="white",
            bg=self.primary_orange,
            activebackground="#e67e22",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            padx=20,
            pady=8,
            command=lambda n=sprint['num']: self.open_sprint(n)
        )
        open_btn.pack(anchor="e", pady=(10, 0))

        # Button hover effects
        open_btn.bind("<Enter>", lambda e: open_btn.config(bg="#e67e22"))
        open_btn.bind("<Leave>", lambda e: open_btn.config(bg=self.primary_orange))

        return card

    def create_footer(self):
        # Create footer frame matching header height with primary green background
        footer_frame = tk.Frame(self.root, bg=self.primary_green, height=40)
        footer_frame.grid(row=2, column=0, sticky="nsew")

        # Footer label with copyright and slogan
        footer = tk.Label(
            footer_frame,
            text="© 2025 FLEXI GYM · Train Smart, Live Strong",
            bg=self.primary_green,
            fg="white",
            font=("Montserrat", 9)
        )
        footer.place(relx=0.5, rely=0.5, anchor="center")

    def open_sprint(self, sprint_num):
        # Attempt to open the external Python sprint module file if it exists
        filename = f"Sprint_{sprint_num}.py"
        if os.path.exists(filename):
            try:
                # Check if the sprint process is already running
                if sprint_num in self.sprint_processes:
                    if self.sprint_processes[sprint_num].poll() is None:
                        messagebox.showinfo("Already Open", f"Sprint {sprint_num} is already running")
                        return
                # Start the sprint module as a new subprocess
                self.sprint_processes[sprint_num] = subprocess.Popen(["python", filename])
            except Exception as e:
                # Show error if unable to start the sprint module
                messagebox.showerror("Error", f"Could not open {filename}\n{str(e)}")
        else:
            # Show error if the sprint module file is not found
            messagebox.showerror("Not Found", f"File {filename} not found")

if __name__ == "__main__":
    root = tk.Tk()

    # Attempt to set default font to Montserrat for the whole application
    try:
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Montserrat", size=10)
    except:
        pass

    root.attributes('-alpha', 0.98)  # Set window transparency for subtle effect
    SprintNavigator(root)  # Create the application instance
    root.mainloop()  # Start the Tkinter event loop to run the application
