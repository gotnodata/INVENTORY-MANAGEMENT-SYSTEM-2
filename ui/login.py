import tkinter as tk
from tkinter import ttk, messagebox
import config
from auth import auth


class LoginWindow:
    """Login window class for user authentication"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{config.MAIN_WINDOW_TITLE} - Login")
        self.root.geometry(config.LOGIN_WINDOW_GEOMETRY)
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Login frame
        login_frame = ttk.Frame(root, padding="20")
        login_frame.pack(expand=True)
        
        # Title
        title_label = ttk.Label(login_frame, text=config.MAIN_WINDOW_TITLE, 
                               font=config.DEFAULT_FONT_TITLE)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, width=20)
        username_entry.grid(row=1, column=1, pady=5)
        username_entry.focus()
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, 
                                  show="*", width=20)
        password_entry.grid(row=2, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        root.bind('<Return>', lambda event: self.login())
        
        self.authenticated_user = None
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def login(self):
        """Handle login button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
            
        user = auth.authenticate_user(username, password)
        if user:
            self.authenticated_user = user
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password_var.set("")
            self.username_var.focus()
