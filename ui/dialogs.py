import tkinter as tk
from tkinter import ttk, messagebox
import config
from auth import auth


class AddUserDialog:
    """Dialog for adding a new user"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent.root)
        self.dialog.title("Add New User")
        self.dialog.geometry(config.DIALOG_WINDOW_GEOMETRY)
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent.root)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(expand=True)
        
        # Form fields
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=25).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=25).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=25).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value=config.ROLE_USER)
        role_combo = ttk.Combobox(frame, textvariable=self.role_var, 
                                 values=[config.ROLE_USER, config.ROLE_ADMIN], width=23)
        role_combo.grid(row=3, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Create User", command=self.create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def center_dialog(self):
        """Center the dialog on the screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_user(self):
        """Create a new user"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        email = self.email_var.get().strip() or None
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return
            
        if len(password) < config.MIN_PASSWORD_LENGTH:
            messagebox.showerror("Error", f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters!")
            return
            
        if auth.create_user(username, password, email, role):
            messagebox.showinfo("Success", f"User '{username}' created successfully!")
            self.dialog.destroy()
            if hasattr(self.parent, 'refresh_users'):
                self.parent.refresh_users()
        else:
            messagebox.showerror("Error", "Failed to create user (username may already exist)!")
