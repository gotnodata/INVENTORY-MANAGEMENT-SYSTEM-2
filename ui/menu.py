"""Menu management for the application"""
import tkinter as tk
from tkinter import messagebox
import config


class MenuManager:
    """Handles all menu creation and management"""
    
    def __init__(self, root, on_logout=None, on_about=None):
        """
        Initialize menu manager
        
        Args:
            root: tk.Tk root window
            on_logout: Callback function for logout action
            on_about: Callback function for about action
        """
        self.root = root
        self.on_logout = on_logout or self._default_logout
        self.on_about = on_about or self._default_about
        
        self.create_menu()
    
    def create_menu(self):
        """Create and setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self._handle_logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._handle_about)
    
    def _handle_logout(self):
        """Handle logout action"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout()
    
    def _handle_about(self):
        """Handle about action"""
        self.on_about()
    
    @staticmethod
    def _default_logout():
        """Default logout handler"""
        pass
    
    @staticmethod
    def _default_about():
        """Default about dialog"""
        about_text = """Inventory Management System v2.0
        
Features:
• Inventory Management
• Category Management  
• Supplier Management
• Transaction Tracking
• User Authentication
• Role-based Access Control

"""
        messagebox.showinfo("About", about_text)
