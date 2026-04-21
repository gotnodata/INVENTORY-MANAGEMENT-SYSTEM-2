"""UI Theme and styling utilities"""
import tkinter as tk
from tkinter import ttk
import config


class Tooltip:
    """Tooltip widget for displaying help text"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip or not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", 
                      relief=tk.SOLID, borderwidth=1, font=("Arial", 9))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class ValidationFrame:
    """Frame for input validation"""
    
    def __init__(self, parent, label_text="", validation_func=None):
        self.frame = ttk.Frame(parent)
        self.validation_func = validation_func
        
        ttk.Label(self.frame, text=label_text).pack(anchor=tk.W)
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_var)
        self.entry.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(self.frame, text="", foreground="red")
        self.status_label.pack(anchor=tk.W)
        
        if validation_func:
            self.entry.bind("<KeyRelease>", self.validate)
    
    def validate(self, event=None):
        if self.validation_func:
            value = self.entry_var.get()
            is_valid, message = self.validation_func(value)
            self.status_label.config(text=message if not is_valid else "")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def get(self):
        return self.entry_var.get()
    
    def set(self, value):
        self.entry_var.set(value)


class StatusBadge:
    """Status badge widget"""
    
    def __init__(self, parent, text="", status="info"):
        self.frame = ttk.Frame(parent)
        
        self.label = ttk.Label(self.frame, text=text)
        self.label.pack()
        
        self.set_status(status)
    
    def set_status(self, status):
        colors = {
            "success": config.COLOR_SUCCESS,
            "warning": config.COLOR_WARNING,
            "danger": config.COLOR_DANGER,
            "info": config.COLOR_INFO
        }
        
        color = colors.get(status, config.COLOR_INFO)
        self.label.config(foreground=color)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def set_text(self, text):
        self.label.config(text=text)


class SearchBar:
    """Search bar widget with clear button"""
    
    def __init__(self, parent, placeholder="Search...", search_callback=None):
        self.frame = ttk.Frame(parent)
        
        self.search_var = tk.StringVar()
        self.search_var.set(placeholder)
        
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.clear_button = ttk.Button(self.frame, text="✕", width=3, 
                                   command=self.clear_search)
        self.clear_button.pack(side=tk.RIGHT)
        
        self.search_callback = search_callback
        
        # Bind search on key release
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Clear placeholder on focus
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
    
    def on_search(self, event=None):
        if self.search_callback:
            self.search_callback(self.search_var.get())
    
    def clear_search(self):
        self.search_var.set("")
        if self.search_callback:
            self.search_callback("")
    
    def clear_placeholder(self, event=None):
        if self.search_var.get() == self.search_var.get():  # placeholder text
            self.search_var.set("")
    
    def restore_placeholder(self, event=None):
        if not self.search_var.get():
            self.search_var.set("Search...")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def get(self):
        return self.search_var.get()
    
    def set(self, value):
        self.search_var.set(value)
