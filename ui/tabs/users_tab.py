"""Users management tab module"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from auth import auth
from database import models
from ui.dialogs import AddUserDialog
from ui.theme import SearchBar, Tooltip


class UsersTab:
    """Users management tab class (admin only)"""
    
    def __init__(self, notebook, status_bar_updater, current_user, root):
        self.notebook = notebook
        self.update_status_bar = status_bar_updater
        self.current_user = current_user
        self.root = root
        self.all_users = []  # Store all users for filtering
        
        # Create frame and add to notebook
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="👥 Users")
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.refresh_users()
    
    def create_ui(self):
        """Create users tab UI with enhanced layout"""
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="➕ New User", command=self._on_new_user, width=18).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_users, width=15).pack(side=tk.LEFT, padx=2)
        
        # Left panel for actions
        left_frame = ttk.LabelFrame(self.frame, text="👤 User Management", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Button(left_frame, text="➕ Add New User", command=self.add_user_dialog, width=20).pack(pady=10)
        
        # User info display
        info_frame = ttk.LabelFrame(left_frame, text="📊 Current Session", padding=10)
        info_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(info_frame, text="Logged in as:", font=config.DEFAULT_FONT_LABEL).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"{self.current_user['username']} ({self.current_user['role']})", 
                 font=config.DEFAULT_FONT_BODY).pack(anchor=tk.W, pady=5)
        
        # Right panel for list
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="👥 Users", font=config.DEFAULT_FONT_LABEL).pack(side=tk.LEFT)
        self.user_count_label = ttk.Label(header_frame, text="Users: 0", font=config.DEFAULT_FONT_BODY)
        self.user_count_label.pack(side=tk.RIGHT)
        
        # Search bar
        self.search_bar = ttk.Frame(right_frame)  # Simple search for users
        self.search_bar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.search_bar, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.search_bar, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self._on_search_change())
        
        ttk.Button(self.search_bar, text="Clear", command=self._clear_search).pack(side=tk.LEFT, padx=5)
        
        # Treeview for users
        columns = ('ID', 'Username', 'Email', 'Role', 'Created At')
        self.users_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Username', text='Username')
        self.users_tree.heading('Email', text='Email')
        self.users_tree.heading('Role', text='Role')
        self.users_tree.heading('Created At', text='Created At')
        
        self.users_tree.column('ID', width=40, anchor='center')
        self.users_tree.column('Username', width=100)
        self.users_tree.column('Email', width=150)
        self.users_tree.column('Role', width=80, anchor='center')
        self.users_tree.column('Created At', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.users_tree.bind('<Double-1>', self.on_double_click)
        self.users_tree.bind('<Button-3>', self._show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.users_tree, tearoff=0)
        self.context_menu.add_command(label="🔄 Reset Password", command=self._context_reset_password)
        self.context_menu.add_command(label="🗑️ Delete User", command=self._context_delete_user)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy ID", command=self._context_copy_id)
    
    def _on_new_user(self):
        """Handle new user"""
        self.add_user_dialog()
        self.update_status_bar("✎ Creating new user...")
    
    def _on_search_change(self):
        """Handle search input change"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.refresh_users()
            return
        
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        for user in self.all_users:
            user_id, username, email, role, created_at = user
            
            if (search_term in str(username).lower() or 
                search_term in str(email).lower() or
                search_term in str(role).lower() or
                search_term in str(created_at).lower() or
                search_term in str(user_id)):
                
                self.users_tree.insert('', 'end', values=user)
        
        self.user_count_label.config(text=f"Users: {len(self.users_tree.get_children())}")
    
    def _clear_search(self):
        """Clear search and refresh users"""
        self.search_var.set("")
        self.refresh_users()
    
    def _show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.users_tree.selection()
        if item:
            self.users_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def _context_reset_password(self):
        """Context menu: Reset user password"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user!")
            return
            
        user_values = self.users_tree.item(selected[0])['values']
        user_id = user_values[0]
        username = user_values[1]
        
        if messagebox.askyesno("Reset Password", f"Reset password for '{username}'?"):
            # For simplicity, set password to "password123"
            if auth.update_user_password(user_id, "password123"):
                messagebox.showinfo("Success", f"Password reset for '{username}'!\nNew password: password123")
                self.update_status_bar(f"🔑 Password reset for '{username}'")
            else:
                messagebox.showerror("Error", "Failed to reset password!")
    
    def _context_delete_user(self):
        """Context menu: Delete user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user!")
            return
            
        user_values = self.users_tree.item(selected[0])['values']
        user_id = user_values[0]
        username = user_values[1]
        
        if user_id == self.current_user['id']:
            messagebox.showerror("Error", "Cannot delete your own account!")
            return
        
        if messagebox.askyesno("Delete User", f"Delete user '{username}'? This cannot be undone."):
            if auth.delete_user(user_id):
                self.refresh_users()
                self.update_status_bar(f"🗑️ User '{username}' deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete user!")
    
    def _context_copy_id(self):
        """Context menu: Copy user ID"""
        selected = self.users_tree.selection()
        if selected:
            user_id = self.users_tree.item(selected[0])['values'][0]
            self.frame.clipboard_clear()
            self.frame.clipboard_append(str(user_id))
            self.update_status_bar(f"📋 User ID {user_id} copied to clipboard")
    
    def add_user_dialog(self):
        """Show add user dialog"""
        dialog = AddUserDialog(self.frame)
        self.root.wait_window(dialog)
        self.refresh_users()
        self.update_status_bar("✓ User management refreshed")
    
    def refresh_users(self):
        """Refresh users display"""
        # Clear existing users
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
            
        users = auth.get_all_users()
        self.all_users = users
        
        for user in users:
            self.users_tree.insert('', 'end', values=user)
        
        self.user_count_label.config(text=f"Users: {len(self.users_tree.get_children())}")
    
    def on_double_click(self, event):
        """Handle double click on user"""
        selected = self.users_tree.selection()
        if selected:
            user = self.users_tree.item(selected[0])['values']
            messagebox.showinfo("User Details", 
                f"ID: {user[0]}\n"
                f"Username: {user[1]}\n"
                f"Email: {user[2] or 'N/A'}\n"
                f"Role: {user[3]}\n"
                f"Created: {user[4]}")
