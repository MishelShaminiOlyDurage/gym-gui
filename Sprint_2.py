import tkinter as tk
from tkinter import messagebox, ttk

class FlexGymApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flex Gym Membership & Billing")
        self.geometry("800x600")
        self.configure(bg='White')
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TNotebook', background='white')
        style.configure('TNotebook.Tab', background='green', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', 'green')], foreground=[('selected', 'white')])
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self)

        self.tab_signup = ttk.Frame(tab_control)
        self.tab_membership = ttk.Frame(tab_control)
        self.tab_billing = ttk.Frame(tab_control)

        tab_control.add(self.tab_signup, text='Sign Up / Login')
        tab_control.add(self.tab_membership, text='Manage Membership')
        tab_control.add(self.tab_billing, text='Billing')
        tab_control.pack(expand=1, fill='both')

        self.create_signup_tab()
        self.create_membership_tab()
        self.create_billing_tab()

    def themed_label(self, parent, text):
        return tk.Label(parent, text=text, bg='green', fg='white')

    def themed_entry(self, parent):
        return tk.Entry(parent, bg='white', fg='green')

    def themed_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg='green', fg='white')

    def create_signup_tab(self):
        self.signup_name = tk.StringVar()
        self.signup_email = tk.StringVar()
        self.themed_label(self.tab_signup, "Choose a Membership Plan:").pack() 
        plans={ 
            
             'Basic' : '£10/month',
             'Silver': '£15/month',
             'Gold'  :'£20/month',
            'Inclusive': '£25/month',
             'Student'  : '£30/month',
             'VIP Elite':'£35/month',
             'Premium': '£40/month',
             'Personal Training':'£55/month',
            ' Platinum': '£60/month',
             'Diamond':'£65/month',
             'Family': '£70/month', 



             } 

        self.selected_plan = tk.StringVar()
        for plan, price in plans.items():
            tk.Radiobutton(
                self.tab_signup,
                text=f"{plan} Plan - {price}",
                variable=self.selected_plan,
                value=plan,
                bg='green',
                fg='black',
                selectcolor='white',
                activebackground='white',
                activeforeground='green'
            ).pack(anchor='w')
        self.themed_label(self.tab_signup, "Name:").pack()
        tk.Entry(self.tab_signup, textvariable=self.signup_name, bg='white', fg='green').pack()
        self.themed_label(self.tab_signup, "Email:").pack()
        tk.Entry(self.tab_signup, textvariable=self.signup_email, bg='white', fg='green').pack()
        self.themed_button(self.tab_signup, "Sign Up", self.sign_up_user).pack()
        self.themed_button(self.tab_signup, "Login", self.login_user).pack()

    def create_membership_tab(self):
        self.themed_label(self.tab_membership, "Update Profile:").pack()
        self.themed_button(self.tab_membership, "Edit Contact Info", self.edit_contact_info).pack()
        self.themed_button(self.tab_membership, "Set Fitness Goals", self.set_fitness_goals).pack()
        self.themed_button(self.tab_membership, "Pause Membership", self.pause_membership).pack()
        self.themed_button(self.tab_membership, "Reactivate Membership", self.reactivate_membership).pack()
        self.themed_button(self.tab_membership, "Manage Family Accounts", self.manage_family_accounts).pack()
        self.themed_button(self.tab_membership, "Book Gym Classes", self.book_gym_classes).pack()

    def create_billing_tab(self):
        self.themed_label(self.tab_billing, "Billing Options:").pack()
        self.themed_button(self.tab_billing, "View Billing History", self.view_billing_history).pack()
        self.themed_button(self.tab_billing, "Update Payment Method", self.update_payment_method).pack()
        self.themed_button(self.tab_billing, "Download Receipts", self.download_receipts).pack()
        self.discount_entry = self.themed_entry(self.tab_billing)
        self.discount_entry.pack()
        self.themed_button(self.tab_billing, "Apply Discount Code", self.apply_discount_code).pack()
        self.themed_label(self.tab_billing, "Email Alerts for Payment Issues Enabled").pack()

    def popup_window(self, title, message):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.configure(bg='white')
        self.themed_label(popup, message).pack(pady=10)
        self.themed_button(popup, "Close", popup.destroy).pack(pady=5)

    def edit_contact_info(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Contact Info")
        popup.configure(bg='black')
        self.themed_label(popup, "Phone:").pack()
        phone_entry = self.themed_entry(popup)
        phone_entry.pack()
        self.themed_label(popup, "Address:").pack()
        address_entry = self.themed_entry(popup)
        address_entry.pack()
        self.themed_button(popup, "Save", lambda: messagebox.showinfo("Saved", "Contact info updated.")).pack(pady=5)
        self.themed_button(popup, "Close", popup.destroy).pack()

    def set_fitness_goals(self):
        popup = tk.Toplevel(self)
        popup.title("Set Fitness Goals")
        popup.configure(bg='black')
        self.themed_label(popup, "Enter your fitness goal:").pack()
        goal_entry = self.themed_entry(popup)
        goal_entry.pack()
        self.themed_button(popup, "Save Goal", lambda: messagebox.showinfo("Saved", f"Goal '{goal_entry.get()}' set!")).pack(pady=5)
        self.themed_button(popup, "Close", popup.destroy).pack()

    def pause_membership(self):
        self.popup_window("Pause Membership", "Your membership is now paused.")

    def reactivate_membership(self):
        self.popup_window("Reactivate Membership", "Your membership has been reactivated.")

    def manage_family_accounts(self):
        popup = tk.Toplevel(self)
        popup.title("Manage Family Accounts")
        popup.configure(bg='black')
        self.themed_label(popup, "Add Family Member Name:").pack()
        family_entry = self.themed_entry(popup)
        family_entry.pack()
        self.themed_button(popup, "Add", lambda: messagebox.showinfo("Added", f"Added {family_entry.get()} to your family accounts.")).pack()
        self.themed_button(popup, "Close", popup.destroy).pack()

    def book_gym_classes(self):
        popup = tk.Toplevel(self)
        popup.title("Book Gym Classes")
        popup.configure(bg='black')
        self.themed_label(popup, "Enter class name to book:").pack()
        class_entry = self.themed_entry(popup)
        class_entry.pack()
        self.themed_button(popup, "Book", lambda: messagebox.showinfo("Booked", f"Booked class: {class_entry.get()}.")).pack(pady=5)
        self.themed_button(popup, "Close", popup.destroy).pack()

    def view_billing_history(self):
        self.popup_window("Billing History", "Here is your list of past payments and invoices.")

    def update_payment_method(self):
        popup = tk.Toplevel(self)
        popup.title("Update Payment Method")
        popup.configure(bg='black')
        self.themed_label(popup, "Card Number:").pack()
        card_entry = self.themed_entry(popup)
        card_entry.pack()
        self.themed_label(popup, "Expiry Date:").pack()
        expiry_entry = self.themed_entry(popup)
        expiry_entry.pack()
        self.themed_button(popup, "Save", lambda: messagebox.showinfo("Saved", "Payment method updated.")).pack()
        self.themed_button(popup, "Close", popup.destroy).pack()

    def download_receipts(self):
        self.popup_window("Download Receipts", "Receipts downloaded successfully.")

    def apply_discount_code(self):
        code = self.discount_entry.get()
        if code:
            messagebox.showinfo("Discount Applied", f"Code '{code}' applied.")
        else:
            messagebox.showwarning("Error", "Please enter a discount code.")

    def sign_up_user(self):
        selected = self.selected_plan.get()
        name = self.signup_name.get()
        email = self.signup_email.get()
        if not name or not email:
            messagebox.showwarning("Missing Info", "Name and Email are required to sign up.")
            return
        if selected:
            self.show_welcome_page(name, selected)
        else:
            messagebox.showwarning("No Plan Selected", "Please select a membership plan before signing up.")
        
    def login_user(self):
        name = self.signup_name.get()
        email = self.signup_email.get()
        if not name or not email:
            messagebox.showwarning("Missing Info", "Name and Email are required to login.")
            return
        self.show_welcome_page(name, None)

    def show_welcome_page(self, name, plan):
        popup = tk.Toplevel(self)
        popup.title("Welcome")
        popup.configure(bg='black')
        msg = f"Welcome {name}!"
        if plan:
            msg += f" You have selected the {plan} plan."
        self.themed_label(popup, msg).pack(pady=20)
        self.themed_button(popup, "Close", popup.destroy).pack(pady=10)

if __name__ == "__main__":
    app = FlexGymApp()
    app.mainloop()
